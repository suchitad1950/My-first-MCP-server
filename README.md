# My First MCP Server

A comprehensive Model Context Protocol (MCP) server implementation for employee leave management.

## 📁 Project Structure

This repository contains two MCP server implementations:

### 1. `mcp-employee-leave/` - Complete Employee Leave Management System
- **Purpose**: Full-featured HR leave management server
- **Features**: 
  - Employee information management
  - Leave balance calculations
  - Leave request approval workflow
  - Working days calculator
  - Pending requests tracking

### 2. `mcp_leave_server/` - Alternative Implementation
- **Purpose**: Alternative server structure with database integration
- **Features**: Database models and schemas for leave management

## 🌟 Main Features

### Employee Leave Management (`mcp-employee-leave/`)
- ✅ **7 MCP Tools**: Complete set of leave management tools
- ✅ **1 Resource**: Employee data access
- ✅ **Claude Desktop Integration**: Ready-to-use configuration
- ✅ **Sample Data**: 10 employees, 10 leave requests (6 approved, 4 pending)
- ✅ **Working Server**: All connection issues resolved

#### Available Tools:
1. `check_leave_balance` - Check employee leave balances
2. `get_employee_info` - View employee details
3. `list_employees` - List all employees
4. `get_leave_requests` - View leave request history
5. `approve_leave_request` - Approve/reject requests
6. `calculate_working_days` - Calculate business days
7. `get_pending_requests` - View pending approvals

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment
- Claude Desktop (for integration)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/suchitad1950/My-first-MCP-server.git
   cd My-first-MCP-server
   ```

2. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   cd mcp-employee-leave
   pip install -r requirements.txt
   ```

4. **Test the server**:
   ```bash
   python3 server.py
   ```

### Claude Desktop Integration

1. **Copy configuration**:
   ```bash
   cp mcp-employee-leave/claude_desktop_config_fixed.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Restart Claude Desktop**

3. **Test in Claude**:
   - "List all employees"
   - "Show me pending leave requests"
   - "Check EMP001's annual leave balance"

## 📊 Sample Data

The server comes with realistic sample data representing a modern Indian company:

### Employees (10):
- **EMP001**: Sachin Goswami (Senior Software Engineer, Engineering) - 25 annual, 10 sick days
- **EMP002**: Ravi Punekar (Marketing Manager, Marketing) - 28 annual, 12 sick days  
- **EMP003**: Rahul Deshpande (HR Director, HR) - 30 annual, 15 sick days
- **EMP004**: Archana Jadhav (Financial Analyst, Finance) - 22 annual, 10 sick days
- **EMP005**: Preeti Kulkarni (Sales Executive, Sales) - 25 annual, 12 sick days
- **EMP006**: Amit Sharma (Sales Manager, Sales) - 30 annual, 15 sick days
- **EMP007**: Priya Mehta (VP Marketing & Sales, Marketing) - 32 annual, 18 sick days
- **EMP008**: Vikram Singh (CFO, Finance) - 35 annual, 20 sick days
- **EMP009**: Neha Patil (Junior Developer, Engineering) - 20 annual, 8 sick days
- **EMP010**: Karan Joshi (Operations Coordinator, Operations) - 22 annual, 10 sick days

### Organizational Structure:
- **Leadership**: 3 C-level/VP executives (Rahul, Priya, Vikram)
- **Management**: 3 managers (Ravi, Amit, Sachin as senior engineer)
- **Staff**: 4 individual contributors (Archana, Preeti, Neha, Karan)
- **Departments**: Engineering (2), Marketing (2), Finance (2), Sales (2), HR (1), Operations (1)

### Leave Requests (10):
- **6 Approved**: 
  - Sachin's family vacation (5 days) & flu leave (3 days)
  - Ravi's holiday break (8 days)
  - Rahul's personal appointment (1 day, auto-approved)
  - Archana's medical procedure (3 days)
  - Priya's Diwali festival (3 days, auto-approved)
- **4 Pending**: 
  - Preeti's Thanksgiving week (5 days)
  - Amit's Christmas holidays (5 days)
  - Neha's wedding celebration (3 days)
  - Karan's doctor appointment (1 day)

## 🛠️ Development

### File Structure
```
mcp-employee-leave/
├── server.py                     # Main MCP server (WORKING VERSION)
├── employee_data.json           # Updated employee database
├── requirements.txt             # Python dependencies
├── README.md                    # Detailed documentation
├── test_tools.py               # Testing script
├── server_wrapper.py           # Alternative server wrapper
├── claude_desktop_config_fixed.json  # Claude Desktop configuration
├── mcp_config.yaml             # MCP server configuration
└── mcp_server.log              # Server logs
```

### Key Components
- **EmployeeLeaveManager**: Core business logic with enhanced data management
- **MCP Tools**: 7 interactive tools for Claude Desktop with full CRUD operations
- **Data Models**: Pydantic models with position and manager hierarchy support
- **Error Handling**: Comprehensive logging and debugging capabilities

## 🔧 Configuration Files

- `claude_desktop_config_fixed.json` - Working Claude Desktop configuration
- `mcp_config.yaml` - Alternative MCP configuration format
- `requirements.txt` - Python package dependencies

## 📈 Version History

- **v1.0.0** (Current): Complete working MCP server with Claude Desktop integration
  - Enhanced employee database with 10 employees and management hierarchy
  - Improved leave request workflow with realistic approval patterns
  - All connection issues resolved
  - Comprehensive testing completed
  - Full documentation provided

## 🤝 Contributing

This is a learning project demonstrating MCP server implementation. Feel free to:
- Fork the repository
- Submit issues
- Suggest improvements
- Add new features

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🎯 Next Steps

- [ ] Add database persistence (PostgreSQL/SQLite)
- [ ] Implement authentication and authorization
- [ ] Add email notifications for leave approvals
- [ ] Create web dashboard for HR management
- [ ] Add more leave types (maternity, paternity, bereavement)
- [ ] Implement leave policies and business rules
- [ ] Add reporting and analytics features

## 💡 Learning Outcomes

This project demonstrates:
- **Modern AI Integration**: Working with Claude Desktop and MCP protocol
- **Async Python Programming**: Using async/await for scalable server architecture  
- **Data Modeling**: Realistic HR data structures with hierarchical relationships
- **API Design**: RESTful-style tools with proper validation and error handling
- **Testing Strategy**: Comprehensive test coverage with realistic scenarios

---

**Created as part of learning Model Context Protocol (MCP) development** 🚀

