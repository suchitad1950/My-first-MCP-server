#!/usr/bin/env python3
"""
HR Leave Management MCP Server
A Model Context Protocol server for HR managers to calculate and manage employee leave
"""

import asyncio
import json
from datetime import datetime, date, timedelta
from typing import Any, List
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
from pydantic import AnyUrl

from .database import db
from .models import LeaveType, LeaveStatus, LeaveRequest
from .schemas import (
    CHECK_LEAVE_BALANCE_SCHEMA,
    GET_EMPLOYEE_INFO_SCHEMA,
    GET_LEAVE_REQUESTS_SCHEMA,
    UPDATE_LEAVE_STATUS_SCHEMA,
    CREATE_LEAVE_REQUEST_SCHEMA,
    CALCULATE_WORKING_DAYS_SCHEMA
)

# Create server instance
server = Server("hr-leave-management-server")

def calculate_working_days(start_date: date, end_date: date, exclude_weekends: bool = True) -> int:
    """Calculate number of working days between two dates"""
    if start_date > end_date:
        return 0
    
    total_days = (end_date - start_date).days + 1
    
    if not exclude_weekends:
        return total_days
    
    # Count working days (exclude weekends)
    working_days = 0
    current_date = start_date
    
    while current_date <= end_date:
        # Monday = 0, Sunday = 6
        if current_date.weekday() < 5:  # Mon-Fri
            working_days += 1
        current_date += timedelta(days=1)
    
    return working_days

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available HR leave management tools"""
    return [
        Tool(
            name="check_leave_balance",
            description="Check an employee's leave balance and availability",
            inputSchema=CHECK_LEAVE_BALANCE_SCHEMA
        ),
        Tool(
            name="get_employee_info",
            description="Get detailed information about an employee",
            inputSchema=GET_EMPLOYEE_INFO_SCHEMA
        ),
        Tool(
            name="get_leave_requests",
            description="Get leave requests for an employee",
            inputSchema=GET_LEAVE_REQUESTS_SCHEMA
        ),
        Tool(
            name="update_leave_status",
            description="Approve or reject a leave request",
            inputSchema=UPDATE_LEAVE_STATUS_SCHEMA
        ),
        Tool(
            name="create_leave_request",
            description="Create a new leave request for an employee",
            inputSchema=CREATE_LEAVE_REQUEST_SCHEMA
        ),
        Tool(
            name="calculate_working_days",
            description="Calculate working days between two dates",
            inputSchema=CALCULATE_WORKING_DAYS_SCHEMA
        ),
        Tool(
            name="list_all_employees",
            description="List all employees in the system",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_pending_requests",
            description="Get all pending leave requests that need approval",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> List[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls for HR leave management"""
    
    if name == "check_leave_balance":
        employee_id = arguments.get("employee_id")
        leave_type = LeaveType(arguments.get("leave_type"))
        year = arguments.get("year", datetime.now().year)
        
        balance = db.calculate_leave_balance(employee_id, leave_type, year)
        
        if not balance:
            return [TextContent(type="text", text=f"Employee {employee_id} not found")]
        
        result = f"""
📊 **Leave Balance Report for {balance.employee_name}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 **Employee ID:** {balance.employee_id}
📅 **Year:** {balance.year}
🏷️ **Leave Type:** {balance.leave_type.value.title()}

📈 **Balance Summary:**
• Total Entitlement: {balance.total_entitlement} days
• Used Days: {balance.used_days} days
• Remaining Days: {balance.remaining_days} days
• Pending Requests: {balance.pending_days} days
• **Available Days: {balance.available_days} days**

💡 Available days = Remaining days - Pending requests
        """
        
        return [TextContent(type="text", text=result.strip())]
    
    elif name == "get_employee_info":
        employee_id = arguments.get("employee_id")
        employee = db.get_employee(employee_id)
        
        if not employee:
            return [TextContent(type="text", text=f"Employee {employee_id} not found")]
        
        result = f"""
👤 **Employee Information**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• **ID:** {employee.employee_id}
• **Name:** {employee.name}
• **Email:** {employee.email}
• **Department:** {employee.department}
• **Hire Date:** {employee.hire_date.strftime('%B %d, %Y')}
• **Annual Leave Entitlement:** {employee.annual_leave_entitlement} days
• **Sick Leave Entitlement:** {employee.sick_leave_entitlement} days
• **Status:** {'Active' if employee.is_active else 'Inactive'}
        """
        
        return [TextContent(type="text", text=result.strip())]
    
    elif name == "get_leave_requests":
        employee_id = arguments.get("employee_id")
        status_filter = arguments.get("status")
        
        requests = db.get_employee_leave_requests(employee_id)
        
        if status_filter:
            requests = [req for req in requests if req.status.value == status_filter]
        
        if not requests:
            return [TextContent(type="text", text=f"No leave requests found for employee {employee_id}")]
        
        result = f"📋 **Leave Requests for Employee {employee_id}**\n"
        result += "━" * 50 + "\n\n"
        
        for req in sorted(requests, key=lambda x: x.submitted_date, reverse=True):
            status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌", "cancelled": "🚫"}
            
            result += f"""
🆔 **Request ID:** {req.request_id}
🏷️ **Type:** {req.leave_type.value.title()}
📅 **Dates:** {req.start_date} to {req.end_date} ({req.days_requested} days)
📝 **Reason:** {req.reason}
{status_emoji.get(req.status.value, '❓')} **Status:** {req.status.value.title()}
📤 **Submitted:** {req.submitted_date.strftime('%Y-%m-%d %H:%M')}
"""
            
            if req.approved_by:
                result += f"👤 **Approved by:** {req.approved_by}\n"
                result += f"📅 **Approved on:** {req.approved_date.strftime('%Y-%m-%d %H:%M')}\n"
            
            if req.comments:
                result += f"💬 **Comments:** {req.comments}\n"
            
            result += "\n" + "─" * 30 + "\n"
        
        return [TextContent(type="text", text=result.strip())]
    
    elif name == "update_leave_status":
        request_id = arguments.get("request_id")
        status = LeaveStatus(arguments.get("status"))
        approved_by = arguments.get("approved_by")
        comments = arguments.get("comments")
        
        success = db.update_leave_request_status(request_id, status, approved_by, comments)
        
        if success:
            request = db.get_leave_request(request_id)
            result = f"""
✅ **Leave Request Updated Successfully**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 **Request ID:** {request_id}
📊 **New Status:** {status.value.title()}
👤 **Updated by:** {approved_by}
📅 **Updated on:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
            if comments:
                result += f"💬 **Comments:** {comments}\n"
            
            return [TextContent(type="text", text=result.strip())]
        else:
            return [TextContent(type="text", text=f"❌ Leave request {request_id} not found")]
    
    elif name == "create_leave_request":
        employee_id = arguments.get("employee_id")
        leave_type = LeaveType(arguments.get("leave_type"))
        start_date = date.fromisoformat(arguments.get("start_date"))
        end_date = date.fromisoformat(arguments.get("end_date"))
        reason = arguments.get("reason")
        
        # Calculate working days
        days_requested = calculate_working_days(start_date, end_date)
        
        # Create new leave request
        new_request = LeaveRequest(
            request_id="",  # Will be generated by database
            employee_id=employee_id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            days_requested=days_requested,
            reason=reason,
            submitted_date=datetime.now()
        )
        
        request_id = db.add_leave_request(new_request)
        
        result = f"""
✅ **Leave Request Created Successfully**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 **Request ID:** {request_id}
👤 **Employee ID:** {employee_id}
🏷️ **Leave Type:** {leave_type.value.title()}
📅 **Dates:** {start_date} to {end_date}
📊 **Days Requested:** {days_requested} working days
📝 **Reason:** {reason}
⏳ **Status:** Pending
📤 **Submitted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """
        
        return [TextContent(type="text", text=result.strip())]
    
    elif name == "calculate_working_days":
        start_date = date.fromisoformat(arguments.get("start_date"))
        end_date = date.fromisoformat(arguments.get("end_date"))
        exclude_weekends = arguments.get("exclude_weekends", True)
        
        working_days = calculate_working_days(start_date, end_date, exclude_weekends)
        
        result = f"""
📅 **Working Days Calculation**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 **Start Date:** {start_date}
📅 **End Date:** {end_date}
🔢 **Total Days:** {(end_date - start_date).days + 1}
⚙️ **Exclude Weekends:** {'Yes' if exclude_weekends else 'No'}
**💼 Working Days:** {working_days}
        """
        
        return [TextContent(type="text", text=result.strip())]
    
    elif name == "list_all_employees":
        employees = db.get_all_employees()
        
        result = "👥 **All Employees**\n"
        result += "━" * 40 + "\n\n"
        
        for emp in sorted(employees, key=lambda x: x.employee_id):
            result += f"🆔 **{emp.employee_id}** - {emp.name}\n"
            result += f"   📧 {emp.email}\n"
            result += f"   🏢 {emp.department}\n"
            result += f"   📅 Annual: {emp.annual_leave_entitlement} days, Sick: {emp.sick_leave_entitlement} days\n\n"
        
        return [TextContent(type="text", text=result.strip())]
    
    elif name == "get_pending_requests":
        all_requests = []
        for requests in db.leave_requests.values():
            if requests.status == LeaveStatus.PENDING:
                all_requests.append(requests)
        
        if not all_requests:
            return [TextContent(type="text", text="✅ No pending leave requests requiring approval")]
        
        result = "⏳ **Pending Leave Requests**\n"
        result += "━" * 40 + "\n\n"
        
        for req in sorted(all_requests, key=lambda x: x.submitted_date):
            employee = db.get_employee(req.employee_id)
            result += f"""
🆔 **{req.request_id}**
👤 {employee.name if employee else req.employee_id} ({req.employee_id})
🏷️ {req.leave_type.value.title()} Leave
📅 {req.start_date} to {req.end_date} ({req.days_requested} days)
📝 {req.reason}
📤 Submitted: {req.submitted_date.strftime('%Y-%m-%d %H:%M')}

"""
        
        result += f"\n📊 **Total Pending Requests:** {len(all_requests)}"
        
        return [TextContent(type="text", text=result.strip())]
    
    else:
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available HR resources"""
    return [
        Resource(
            uri=AnyUrl("hr://employees"),
            name="Employee Directory",
            description="Directory of all employees with their leave entitlements",
            mimeType="application/json"
        ),
        Resource(
            uri=AnyUrl("hr://leave-policies"),
            name="Leave Policies",
            description="Company leave policies and guidelines",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read HR resources"""
    if str(uri) == "hr://employees":
        employees = db.get_all_employees()
        return json.dumps([emp.dict() for emp in employees], default=str, indent=2)
    
    elif str(uri) == "hr://leave-policies":
        return """
📋 COMPANY LEAVE POLICIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏖️ ANNUAL LEAVE
• Standard entitlement: 25 days per year
• Senior employees (5+ years): 28-30 days
• Must be approved in advance
• Maximum 10 consecutive days without director approval

🤒 SICK LEAVE
• Standard entitlement: 10-15 days per year
• Medical certificate required for 3+ consecutive days
• Can be used for medical appointments

👨‍👩‍👧‍👦 FAMILY LEAVE
• Maternity leave: Up to 26 weeks
• Paternity leave: Up to 4 weeks
• Emergency family leave: Up to 5 days per year

📝 APPROVAL PROCESS
• Submit requests at least 2 weeks in advance
• HR manager approval required
• Department head approval for extended leave

⚠️ IMPORTANT NOTES
• Leave cannot be carried over without approval
• Unused sick leave expires at year end
• All leave subject to business requirements
        """
    
    else:
        raise ValueError(f"Unknown resource: {uri}")

async def main():
    """Main entry point for the HR Leave Management MCP Server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hr-leave-management-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities()
            )
        )

if __name__ == "__main__":
    asyncio.run(main())