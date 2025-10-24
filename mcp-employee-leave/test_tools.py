#!/usr/bin/env python3
"""
Test script for MCP Employee Leave Server
Simulates MCP tool calls without running the actual MCP protocol
"""

import asyncio
import json
from server import handle_call_tool

async def test_mcp_tools():
    """Test all MCP tools with sample data"""
    
    print("🧪 Testing MCP Employee Leave Server Tools")
    print("=" * 60)
    
    # Test 1: List all employees
    print("\n1️⃣ Testing: list_employees")
    result = await handle_call_tool("list_employees", {})
    print(result[0].text[:200] + "...")
    
    # Test 2: Get employee info
    print("\n2️⃣ Testing: get_employee_info")
    result = await handle_call_tool("get_employee_info", {"employee_id": "EMP001"})
    print(result[0].text)
    
    # Test 3: Check leave balance
    print("\n3️⃣ Testing: check_leave_balance")
    result = await handle_call_tool("check_leave_balance", {
        "employee_id": "EMP001", 
        "leave_type": "annual"
    })
    print(result[0].text)
    
    # Test 4: Get pending requests
    print("\n4️⃣ Testing: get_pending_requests")
    result = await handle_call_tool("get_pending_requests", {})
    print(result[0].text)
    
    # Test 5: Calculate working days
    print("\n5️⃣ Testing: calculate_working_days")
    result = await handle_call_tool("calculate_working_days", {
        "start_date": "2025-12-20", 
        "end_date": "2025-12-31"
    })
    print(result[0].text)
    
    # Test 6: Approve a leave request
    print("\n6️⃣ Testing: approve_leave_request")
    result = await handle_call_tool("approve_leave_request", {
        "request_id": "REQ003",
        "status": "approved",
        "approved_by": "Test Manager",
        "comments": "Test approval"
    })
    print(result[0].text)
    
    print("\n✅ All MCP tool tests completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())