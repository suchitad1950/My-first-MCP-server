# MCP Employee Leave Server

A streamlined Model Context Protocol (MCP) server for managing employee leave requests and calculations. This server provides HR managers with tools to check leave balances, approve requests, and manage employee leave data efficiently.

## 📁 Project Structure

```
mcp-employee-leave/
├── server.py                # Main MCP server implementation
├── employee_data.json       # Employee leave data (JSON format)
├── mcp_config.yaml          # MCP configuration for Claude Desktop
├── requirements.txt         # Python dependencies
└── README.md                # This documentation
```

## 🌟 Features

### Core Functionality
- **📊 Leave Balance Calculation**: Real-time leave balance tracking
- **👥 Employee Management**: Complete employee information access
- **📋 Leave Request Processing**: Approve/reject leave requests
- **⏳ Pending Requests**: View all requests awaiting approval
- **📅 Working Days Calculator**: Accurate business day calculations
- **🔍 Leave History**: Complete leave request history per employee

### Supported Leave Types
- Annual Leave
- Sick Leave
- Personal Leave
- Maternity Leave
- Paternity Leave
- Emergency Leave

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd mcp-employee-leave

# Install required packages
pip install -r requirements.txt

# Or install manually
pip install mcp pydantic
```

### 2. Test the Server

```bash
# Run the server directly
python3 server.py

# The server will start and listen for MCP connections via stdio
```

### 3. Configure with Claude Desktop

Copy the configuration from `mcp_config.yaml` to your Claude Desktop MCP settings:

```yaml
mcpServers:
  employee-leave:
    command: python3
    args:
      - "/path/to/your/mcp-employee-leave/server.py"
    env:
      PYTHONPATH: "/path/to/your/venv/lib/python3.13/site-packages"
    description: "Employee Leave Management MCP Server"
```

## 🛠️ Available Tools

### 1. `check_leave_balance`
Check an employee's current leave balance.

**Parameters:**
- `employee_id` (string): Employee ID (e.g., "EMP001")
- `leave_type` (string): "annual", "sick", "personal", "maternity", "paternity", "emergency"
- `year` (integer, optional): Year to check (defaults to current year)

**Example:**
```json
{
  "name": "check_leave_balance",
  "arguments": {
    "employee_id": "EMP001",
    "leave_type": "annual",
    "year": 2025
  }
}
```

### 2. `get_employee_info`
Get detailed employee information.

**Parameters:**
- `employee_id` (string): Employee ID

### 3. `list_employees`
List all employees in the system.

### 4. `get_leave_requests`
Get leave requests for a specific employee.

**Parameters:**
- `employee_id` (string): Employee ID
- `status` (string, optional): Filter by "pending", "approved", "rejected", "cancelled"

### 5. `approve_leave_request`
Approve or reject a leave request.

**Parameters:**
- `request_id` (string): Leave request ID
- `status` (string): "approved" or "rejected"
- `approved_by` (string): Name of the approver
- `comments` (string, optional): Comments about the decision

### 6. `calculate_working_days`
Calculate working days between two dates.

**Parameters:**
- `start_date` (string): Start date (YYYY-MM-DD format)
- `end_date` (string): End date (YYYY-MM-DD format)
- `exclude_weekends` (boolean, optional): Exclude weekends (default: true)

### 7. `get_pending_requests`
Get all pending leave requests across the organization.

## 📊 Sample Data

The server comes with realistic sample data:

### Employees (5 total):
- **EMP001**: John Smith (Engineering) - 25 annual, 10 sick days
- **EMP002**: Sarah Johnson (Marketing) - 28 annual, 12 sick days
- **EMP003**: Mike Wilson (HR) - 30 annual, 15 sick days
- **EMP004**: Emily Davis (Finance) - 22 annual, 10 sick days
- **EMP005**: David Brown (Sales) - 25 annual, 12 sick days

### Leave Requests (6 total):
- **3 Approved requests** (John's vacation & sick leave, Emily's medical leave)
- **3 Pending requests** (Sarah's holiday break, Mike's personal day, David's Thanksgiving)

## 💡 Usage Examples

### Check Leave Balance
```bash
# Check John Smith's annual leave balance
{
  "name": "check_leave_balance",
  "arguments": {
    "employee_id": "EMP001",
    "leave_type": "annual"
  }
}
```

### Approve Pending Request
```bash
# Approve Sarah's holiday request
{
  "name": "approve_leave_request",
  "arguments": {
    "request_id": "REQ003",
    "status": "approved",
    "approved_by": "HR Director",
    "comments": "Approved for holiday period"
  }
}
```

### Get All Pending Requests
```bash
# View all requests needing approval
{
  "name": "get_pending_requests",
  "arguments": {}
}
```

## 🔧 Configuration

### Data Persistence
- Employee and leave data is stored in `employee_data.json`
- Changes are automatically saved when leave requests are updated
- The JSON file serves as a simple database for this demonstration

### Customization
- **Add employees**: Edit `employee_data.json` to add new employees
- **Modify entitlements**: Update annual/sick leave entitlements per employee
- **Add leave types**: Extend the `LeaveType` enum in `server.py`

## 📝 Data Format

### Employee Structure
```json
{
  "employee_id": "EMP001",
  "name": "John Smith",
  "email": "john.smith@company.com",
  "department": "Engineering",
  "hire_date": "2022-01-15",
  "annual_leave_entitlement": 25,
  "sick_leave_entitlement": 10,
  "is_active": true
}
```

### Leave Request Structure
```json
{
  "request_id": "REQ001",
  "employee_id": "EMP001",
  "leave_type": "annual",
  "start_date": "2025-11-01",
  "end_date": "2025-11-05",
  "days_requested": 5,
  "reason": "Family vacation",
  "status": "approved",
  "submitted_date": "2025-10-01T09:00:00",
  "approved_by": "HR Manager",
  "approved_date": "2025-10-02T14:30:00",
  "comments": "Approved for family time"
}
```

## 🏢 Business Logic

### Leave Calculation Rules
- **Annual Leave**: Based on employee entitlement (22-30 days typical)
- **Sick Leave**: Based on employee entitlement (10-15 days typical)
- **Working Days**: Excludes weekends by default
- **Availability**: Total entitlement - used days - pending requests

### Status Workflow
1. **Pending**: Newly submitted requests
2. **Approved**: Approved by HR/manager
3. **Rejected**: Declined with comments
4. **Cancelled**: Cancelled by employee or admin

## 🚀 Integration

### With Claude Desktop
1. Add the server configuration to your Claude Desktop MCP settings
2. Restart Claude Desktop
3. Start using leave management commands in your conversations

### With Other MCP Clients
The server implements the standard MCP protocol and works with any MCP-compatible client.

## 📈 Version & Compatibility

- **Version**: 1.0.0
- **Python**: 3.8+
- **MCP Protocol**: 1.0+
- **Dependencies**: `mcp`, `pydantic`

## 🔒 Security Notes

- This is a demonstration server with file-based storage
- For production use, consider:
  - Database integration (PostgreSQL, MySQL)
  - Authentication and authorization
  - Audit logging
  - Data encryption
  - API rate limiting

---

**Ready to streamline your HR leave management!** 🎯

For support or questions, refer to the MCP documentation or check the server logs for debugging information.