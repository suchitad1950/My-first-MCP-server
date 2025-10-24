"""JSON schemas for MCP tool inputs and outputs"""

# Schema for checking employee leave balance
CHECK_LEAVE_BALANCE_SCHEMA = {
    "type": "object",
    "properties": {
        "employee_id": {
            "type": "string",
            "description": "Employee ID (e.g., EMP001)"
        },
        "leave_type": {
            "type": "string",
            "enum": ["annual", "sick", "personal", "maternity", "paternity", "emergency"],
            "description": "Type of leave to check"
        },
        "year": {
            "type": "integer",
            "description": "Year to check (defaults to current year)",
            "minimum": 2020,
            "maximum": 2030
        }
    },
    "required": ["employee_id", "leave_type"]
}

# Schema for getting employee information
GET_EMPLOYEE_INFO_SCHEMA = {
    "type": "object",
    "properties": {
        "employee_id": {
            "type": "string",
            "description": "Employee ID (e.g., EMP001)"
        }
    },
    "required": ["employee_id"]
}

# Schema for getting leave requests
GET_LEAVE_REQUESTS_SCHEMA = {
    "type": "object",
    "properties": {
        "employee_id": {
            "type": "string",
            "description": "Employee ID to get leave requests for"
        },
        "status": {
            "type": "string",
            "enum": ["pending", "approved", "rejected", "cancelled"],
            "description": "Filter by leave request status (optional)"
        }
    },
    "required": ["employee_id"]
}

# Schema for approving/rejecting leave requests
UPDATE_LEAVE_STATUS_SCHEMA = {
    "type": "object",
    "properties": {
        "request_id": {
            "type": "string",
            "description": "Leave request ID"
        },
        "status": {
            "type": "string",
            "enum": ["approved", "rejected"],
            "description": "New status for the leave request"
        },
        "approved_by": {
            "type": "string",
            "description": "Name of the person approving/rejecting"
        },
        "comments": {
            "type": "string",
            "description": "Optional comments about the decision"
        }
    },
    "required": ["request_id", "status", "approved_by"]
}

# Schema for creating new leave requests
CREATE_LEAVE_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "employee_id": {
            "type": "string",
            "description": "Employee ID"
        },
        "leave_type": {
            "type": "string",
            "enum": ["annual", "sick", "personal", "maternity", "paternity", "emergency"],
            "description": "Type of leave"
        },
        "start_date": {
            "type": "string",
            "format": "date",
            "description": "Start date of leave (YYYY-MM-DD)"
        },
        "end_date": {
            "type": "string",
            "format": "date",
            "description": "End date of leave (YYYY-MM-DD)"
        },
        "reason": {
            "type": "string",
            "description": "Reason for leave"
        }
    },
    "required": ["employee_id", "leave_type", "start_date", "end_date", "reason"]
}

# Schema for calculating working days
CALCULATE_WORKING_DAYS_SCHEMA = {
    "type": "object",
    "properties": {
        "start_date": {
            "type": "string",
            "format": "date",
            "description": "Start date (YYYY-MM-DD)"
        },
        "end_date": {
            "type": "string",
            "format": "date",
            "description": "End date (YYYY-MM-DD)"
        },
        "exclude_weekends": {
            "type": "boolean",
            "description": "Whether to exclude weekends (default: true)",
            "default": True
        }
    },
    "required": ["start_date", "end_date"]
}