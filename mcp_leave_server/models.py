from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

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
    hire_date: date
    annual_leave_entitlement: int = 25  # days per year
    sick_leave_entitlement: int = 10    # days per year
    is_active: bool = True

class LeaveRequest(BaseModel):
    request_id: str
    employee_id: str
    leave_type: LeaveType
    start_date: date
    end_date: date
    days_requested: int
    reason: str
    status: LeaveStatus = LeaveStatus.PENDING
    submitted_date: datetime
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None
    comments: Optional[str] = None

class LeaveBalance(BaseModel):
    employee_id: str
    leave_type: LeaveType
    total_entitlement: int
    used_days: int
    remaining_days: int
    year: int

class LeaveCalculation(BaseModel):
    employee_id: str
    employee_name: str
    leave_type: LeaveType
    total_entitlement: int
    used_days: int
    remaining_days: int
    pending_days: int
    available_days: int
    year: int