#!/usr/bin/env python3
"""
MCP Employee Leave Server - WORKING VERSION
A Model Context Protocol server for managing employee leave requests and calculations
"""

import asyncio
import json
import os
from datetime import datetime, date, timedelta
from typing import Any, List, Dict, Optional
from pathlib import Path

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import BaseModel, AnyUrl
from enum import Enum

# Data Models
class LeaveType(str, Enum):
    ANNUAL = "annual"
    SICK = "sick"
    PERSONAL = "personal"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    EMERGENCY = "emergency"

class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class Employee(BaseModel):
    employee_id: str
    name: str
    email: str
    department: str
    hire_date: str
    annual_leave_entitlement: int
    sick_leave_entitlement: int
    is_active: bool = True

class LeaveRequest(BaseModel):
    request_id: str
    employee_id: str
    leave_type: LeaveType
    start_date: str
    end_date: str
    days_requested: int
    reason: str
    status: LeaveStatus
    submitted_date: str
    approved_by: Optional[str] = None
    approved_date: Optional[str] = None
    comments: Optional[str] = None

# Create server instance
server = Server("mcp-employee-leave-server")

class EmployeeLeaveManager:
    def __init__(self, data_file: str = "employee_data.json"):
        self.data_file = Path(__file__).parent / data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load employee data from JSON file"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"employees": [], "leave_requests": []}
    
    def _save_data(self):
        """Save employee data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """Get employee by ID"""
        for emp_data in self.data.get("employees", []):
            if emp_data["employee_id"] == employee_id:
                return Employee(**emp_data)
        return None
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return [Employee(**emp) for emp in self.data.get("employees", [])]
    
    def get_leave_requests(self, employee_id: str = None) -> List[LeaveRequest]:
        """Get leave requests, optionally filtered by employee"""
        requests = []
        for req_data in self.data.get("leave_requests", []):
            if employee_id is None or req_data["employee_id"] == employee_id:
                requests.append(LeaveRequest(**req_data))
        return requests
    
    def add_leave_request(self, request: LeaveRequest) -> str:
        """Add a new leave request"""
        request_dict = request.dict()
        self.data.setdefault("leave_requests", []).append(request_dict)
        self._save_data()
        return request.request_id
    
    def update_leave_status(self, request_id: str, status: LeaveStatus, 
                          approved_by: str = None, comments: str = None) -> bool:
        """Update leave request status"""
        for req in self.data.get("leave_requests", []):
            if req["request_id"] == request_id:
                req["status"] = status.value
                if approved_by:
                    req["approved_by"] = approved_by
                    req["approved_date"] = datetime.now().isoformat()
                if comments:
                    req["comments"] = comments
                self._save_data()
                return True
        return False
    
    def calculate_leave_balance(self, employee_id: str, leave_type: LeaveType, year: int = None):
        """Calculate leave balance for an employee"""
        if year is None:
            year = datetime.now().year
        
        employee = self.get_employee(employee_id)
        if not employee:
            return None
        
        # Convert string to LeaveType if needed
        if isinstance(leave_type, str):
            leave_type = LeaveType(leave_type)
        
        # Get entitlement
        if leave_type == LeaveType.ANNUAL:
            total_entitlement = employee.annual_leave_entitlement
        elif leave_type == LeaveType.SICK:
            total_entitlement = employee.sick_leave_entitlement
        else:
            total_entitlement = 0
        
        # Calculate used and pending days
        used_days = 0
        pending_days = 0
        
        for req in self.get_leave_requests(employee_id):
            if (req.leave_type == leave_type and 
                datetime.fromisoformat(req.start_date).year == year):
                if req.status == LeaveStatus.APPROVED:
                    used_days += req.days_requested
                elif req.status == LeaveStatus.PENDING:
                    pending_days += req.days_requested
        
        remaining_days = total_entitlement - used_days
        available_days = remaining_days - pending_days
        
        return {
            "employee_id": employee_id,
            "employee_name": employee.name,
            "leave_type": leave_type.value,
            "total_entitlement": total_entitlement,
            "used_days": used_days,
            "remaining_days": remaining_days,
            "pending_days": pending_days,
            "available_days": available_days,
            "year": year
        }

# Initialize manager
leave_manager = EmployeeLeaveManager()

def calculate_working_days(start_date: str, end_date: str, exclude_weekends: bool = True) -> int:
    """Calculate working days between dates"""
    start = datetime.fromisoformat(start_date).date()
    end = datetime.fromisoformat(end_date).date()
    
    if start > end:
        return 0
    
    total_days = (end - start).days + 1
    
    if not exclude_weekends:
        return total_days
    
    working_days = 0
    current_date = start
    
    while current_date <= end:
        if current_date.weekday() < 5:  # Mon-Fri
            working_days += 1
        current_date += timedelta(days=1)
    
    return working_days

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="check_leave_balance",
            description="Check an employee's leave balance",
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {"type": "string", "description": "Employee ID"},
                    "leave_type": {
                        "type": "string", 
                        "enum": ["annual", "sick", "personal", "maternity", "paternity", "emergency"],
                        "description": "Type of leave"
                    },
                    "year": {"type": "integer", "description": "Year (optional, defaults to current)"}
                },
                "required": ["employee_id", "leave_type"]
            }
        ),
        Tool(
            name="get_employee_info",
            description="Get employee information",
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {"type": "string", "description": "Employee ID"}
                },
                "required": ["employee_id"]
            }
        ),
        Tool(
            name="list_employees",
            description="List all employees",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_leave_requests",
            description="Get leave requests for an employee",
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {"type": "string", "description": "Employee ID"},
                    "status": {
                        "type": "string",
                        "enum": ["pending", "approved", "rejected", "cancelled"],
                        "description": "Filter by status (optional)"
                    }
                },
                "required": ["employee_id"]
            }
        ),
        Tool(
            name="approve_leave_request",
            description="Approve or reject a leave request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {"type": "string", "description": "Leave request ID"},
                    "status": {
                        "type": "string",
                        "enum": ["approved", "rejected"],
                        "description": "New status"
                    },
                    "approved_by": {"type": "string", "description": "Approver name"},
                    "comments": {"type": "string", "description": "Optional comments"}
                },
                "required": ["request_id", "status", "approved_by"]
            }
        ),
        Tool(
            name="calculate_working_days",
            description="Calculate working days between dates",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "format": "date", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "format": "date", "description": "End date (YYYY-MM-DD)"},
                    "exclude_weekends": {"type": "boolean", "description": "Exclude weekends (default: true)"}
                },
                "required": ["start_date", "end_date"]
            }
        ),
        Tool(
            name="get_pending_requests",
            description="Get all pending leave requests",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "check_leave_balance":
        employee_id = arguments.get("employee_id")
        leave_type = LeaveType(arguments.get("leave_type"))
        year = arguments.get("year", datetime.now().year)
        
        balance = leave_manager.calculate_leave_balance(employee_id, leave_type, year)
        
        if not balance:
            return [TextContent(type="text", text=f"❌ Employee {employee_id} not found")]
        
        result = f"""📊 **Leave Balance Report**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 **Employee:** {balance['employee_name']} ({balance['employee_id']})
📅 **Year:** {balance['year']}
🏷️ **Leave Type:** {balance['leave_type'].title()}

📈 **Balance Summary:**
• Total Entitlement: {balance['total_entitlement']} days
• Used Days: {balance['used_days']} days
• Remaining Days: {balance['remaining_days']} days
• Pending Requests: {balance['pending_days']} days
• **Available Days: {balance['available_days']} days**
"""
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_employee_info":
        employee_id = arguments.get("employee_id")
        employee = leave_manager.get_employee(employee_id)
        
        if not employee:
            return [TextContent(type="text", text=f"❌ Employee {employee_id} not found")]
        
        result = f"""👤 **Employee Information**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• **ID:** {employee.employee_id}
• **Name:** {employee.name}
• **Email:** {employee.email}
• **Department:** {employee.department}
• **Hire Date:** {employee.hire_date}
• **Annual Leave:** {employee.annual_leave_entitlement} days
• **Sick Leave:** {employee.sick_leave_entitlement} days
• **Status:** {'Active' if employee.is_active else 'Inactive'}
"""
        
        return [TextContent(type="text", text=result)]
    
    elif name == "list_employees":
        employees = leave_manager.get_all_employees()
        
        result = "👥 **All Employees**\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for emp in sorted(employees, key=lambda x: x.employee_id):
            result += f"🆔 **{emp.employee_id}** - {emp.name}\n"
            result += f"   📧 {emp.email} | 🏢 {emp.department}\n"
            result += f"   📅 Annual: {emp.annual_leave_entitlement} days, Sick: {emp.sick_leave_entitlement} days\n\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_leave_requests":
        employee_id = arguments.get("employee_id")
        status_filter = arguments.get("status")
        
        requests = leave_manager.get_leave_requests(employee_id)
        
        if status_filter:
            requests = [req for req in requests if req.status.value == status_filter]
        
        if not requests:
            return [TextContent(type="text", text=f"📋 No leave requests found for employee {employee_id}")]
        
        result = f"📋 **Leave Requests for {employee_id}**\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌", "cancelled": "🚫"}
        
        for req in sorted(requests, key=lambda x: x.submitted_date, reverse=True):
            result += f"""🆔 **{req.request_id}**
🏷️ {req.leave_type.value.title()} Leave
📅 {req.start_date} to {req.end_date} ({req.days_requested} days)
📝 Reason: {req.reason}
{status_emoji.get(req.status.value, '❓')} Status: {req.status.value.title()}
📤 Submitted: {req.submitted_date}
"""
            
            if req.approved_by:
                result += f"👤 Approved by: {req.approved_by} on {req.approved_date}\n"
            if req.comments:
                result += f"💬 Comments: {req.comments}\n"
            
            result += "\n" + "─" * 50 + "\n\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "approve_leave_request":
        request_id = arguments.get("request_id")
        status = LeaveStatus(arguments.get("status"))
        approved_by = arguments.get("approved_by")
        comments = arguments.get("comments")
        
        success = leave_manager.update_leave_status(request_id, status, approved_by, comments)
        
        if success:
            result = f"""✅ **Leave Request Updated**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 Request ID: {request_id}
📊 Status: {status.value.title()}
👤 Updated by: {approved_by}
📅 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
            if comments:
                result += f"💬 Comments: {comments}"
            
            return [TextContent(type="text", text=result)]
        else:
            return [TextContent(type="text", text=f"❌ Leave request {request_id} not found")]
    
    elif name == "calculate_working_days":
        start_date = arguments.get("start_date")
        end_date = arguments.get("end_date")
        exclude_weekends = arguments.get("exclude_weekends", True)
        
        working_days = calculate_working_days(start_date, end_date, exclude_weekends)
        
        result = f"""📅 **Working Days Calculation**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Start Date: {start_date}
📅 End Date: {end_date}
⚙️ Exclude Weekends: {'Yes' if exclude_weekends else 'No'}
💼 **Working Days: {working_days}**
"""
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_pending_requests":
        all_requests = leave_manager.get_leave_requests()
        pending_requests = [req for req in all_requests if req.status == LeaveStatus.PENDING]
        
        if not pending_requests:
            return [TextContent(type="text", text="✅ No pending leave requests")]
        
        result = "⏳ **Pending Leave Requests**\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for req in sorted(pending_requests, key=lambda x: x.submitted_date):
            employee = leave_manager.get_employee(req.employee_id)
            employee_name = employee.name if employee else req.employee_id
            
            result += f"""🆔 **{req.request_id}**
👤 {employee_name} ({req.employee_id})
🏷️ {req.leave_type.value.title()} Leave
📅 {req.start_date} to {req.end_date} ({req.days_requested} days)
📝 {req.reason}
📤 Submitted: {req.submitted_date}

"""
        
        result += f"📊 **Total Pending: {len(pending_requests)} requests**"
        
        return [TextContent(type="text", text=result)]
    
    else:
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources"""
    return [
        Resource(
            uri=AnyUrl("file://employee_data.json"),
            name="Employee Data",
            description="JSON file containing all employee and leave request data",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read resource content"""
    if str(uri) == "file://employee_data.json":
        return json.dumps(leave_manager.data, indent=2, default=str)
    else:
        raise ValueError(f"Unknown resource: {uri}")

async def main():
    """Main entry point - COMPLETELY FIXED VERSION"""
    try:
        # Add logging for debugging
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        logger.info("Starting HR Leave Management MCP Server...")
        
        async with stdio_server() as (read_stream, write_stream):
            logger.info("MCP Server connected successfully")
            
            # Create proper initialization options with minimal required fields
            from mcp.types import ServerCapabilities, Implementation
            
            # Create capabilities object manually to avoid validation issues
            capabilities = ServerCapabilities(
                resources={"subscribe": False, "listChanged": False},
                tools={"subscribe": False, "listChanged": False},
                prompts={"subscribe": False, "listChanged": False},
                logging={}
            )
            
            init_options = InitializationOptions(
                server_name="mcp-employee-leave-server",
                server_version="1.0.0",
                capabilities=capabilities
            )
            
            await server.run(read_stream, write_stream, init_options)
            
    except Exception as e:
        import logging
        logging.error(f"Error starting MCP server: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()