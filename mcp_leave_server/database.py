from datetime import datetime, date, timedelta
from typing import List, Optional
from .models import Employee, LeaveRequest, LeaveType, LeaveStatus, LeaveBalance, LeaveCalculation
import uuid

class LeaveDatabase:
    def __init__(self):
        self.employees = {}
        self.leave_requests = {}
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialize with sample employee and leave data"""
        # Sample employees
        employees = [
            Employee(
                employee_id="EMP001",
                name="Sachin Goswami",
                email="Sachin.goswami@company.com",
                department="Engineering",
                hire_date=date(2022, 1, 15),
                annual_leave_entitlement=25,
                sick_leave_entitlement=10
            ),
            Employee(
                employee_id="EMP002",
                name="Ravi Punekar",
                email="Ravi.punekar@company.com",
                department="Marketing",
                hire_date=date(2021, 3, 10),
                annual_leave_entitlement=28,
                sick_leave_entitlement=12
            ),
            Employee(
                employee_id="EMP003",
                name="Rahul Deshpande",
                email="Rahul.deshpande@company.com",
                department="HR",
                hire_date=date(2020, 6, 5),
                annual_leave_entitlement=30,
                sick_leave_entitlement=15
            ),
            Employee(
                employee_id="EMP004",
                name="Archana Jadhav",
                email="Archana.jadhav@company.com",
                department="Finance",
                hire_date=date(2023, 2, 20),
                annual_leave_entitlement=22,
                sick_leave_entitlement=10
            ),
            Employee(
                employee_id= "EMP005",
                name= "Preeti Kulkarni",
                email= "Preeti.kulkarni@company.com",
                department="Sales",
                hire_date= "2021-09-12",
                annual_leave_entitlement= 25,
                sick_leave_entitlement= 12
            )
            
           
            
      
    
        ]
        
        for emp in employees:
            self.employees[emp.employee_id] = emp
        
        # Sample leave requests
        leave_requests = [
            LeaveRequest(
                request_id="REQ001",
                employee_id="EMP001",
                leave_type=LeaveType.ANNUAL,
                start_date=date(2025, 11, 1),
                end_date=date(2025, 11, 5),
                days_requested=5,
                reason="Family vacation",
                status=LeaveStatus.APPROVED,
                submitted_date=datetime(2025, 10, 1, 9, 0),
                approved_by="HR Manager",
                approved_date=datetime(2025, 10, 2, 14, 30)
            ),
            LeaveRequest(
                request_id="REQ002",
                employee_id="EMP001",
                leave_type=LeaveType.SICK,
                start_date=date(2025, 9, 15),
                end_date=date(2025, 9, 17),
                days_requested=3,
                reason="Flu symptoms",
                status=LeaveStatus.APPROVED,
                submitted_date=datetime(2025, 9, 15, 8, 30),
                approved_by="HR Manager",
                approved_date=datetime(2025, 9, 15, 10, 0)
            ),
            LeaveRequest(
                request_id="REQ003",
                employee_id="EMP002",
                leave_type=LeaveType.ANNUAL,
                start_date=date(2025, 12, 20),
                end_date=date(2025, 12, 31),
                days_requested=8,
                reason="Holiday break",
                status=LeaveStatus.PENDING,
                submitted_date=datetime(2025, 10, 20, 11, 15)
            )
        ]
        
        for req in leave_requests:
            self.leave_requests[req.request_id] = req
    
    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """Get employee by ID"""
        return self.employees.get(employee_id)
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return list(self.employees.values())
    
    def get_employee_leave_requests(self, employee_id: str) -> List[LeaveRequest]:
        """Get all leave requests for an employee"""
        return [req for req in self.leave_requests.values() if req.employee_id == employee_id]
    
    def get_leave_request(self, request_id: str) -> Optional[LeaveRequest]:
        """Get leave request by ID"""
        return self.leave_requests.get(request_id)
    
    def add_leave_request(self, leave_request: LeaveRequest) -> str:
        """Add a new leave request"""
        if not leave_request.request_id:
            leave_request.request_id = str(uuid.uuid4())
        self.leave_requests[leave_request.request_id] = leave_request
        return leave_request.request_id
    
    def update_leave_request_status(self, request_id: str, status: LeaveStatus, 
                                  approved_by: str = None, comments: str = None) -> bool:
        """Update leave request status"""
        if request_id in self.leave_requests:
            self.leave_requests[request_id].status = status
            if approved_by:
                self.leave_requests[request_id].approved_by = approved_by
                self.leave_requests[request_id].approved_date = datetime.now()
            if comments:
                self.leave_requests[request_id].comments = comments
            return True
        return False
    
    def calculate_leave_balance(self, employee_id: str, leave_type: LeaveType, year: int = None) -> Optional[LeaveCalculation]:
        """Calculate leave balance for an employee"""
        if year is None:
            year = datetime.now().year
            
        employee = self.get_employee(employee_id)
        if not employee:
            return None
        
        # Get entitlement based on leave type
        if leave_type == LeaveType.ANNUAL:
            total_entitlement = employee.annual_leave_entitlement
        elif leave_type == LeaveType.SICK:
            total_entitlement = employee.sick_leave_entitlement
        else:
            total_entitlement = 0  # Other leave types don't have annual entitlements
        
        # Calculate used days (approved requests in the year)
        used_days = 0
        pending_days = 0
        
        for req in self.get_employee_leave_requests(employee_id):
            if (req.leave_type == leave_type and 
                req.start_date.year == year):
                if req.status == LeaveStatus.APPROVED:
                    used_days += req.days_requested
                elif req.status == LeaveStatus.PENDING:
                    pending_days += req.days_requested
        
        remaining_days = total_entitlement - used_days
        available_days = remaining_days - pending_days
        
        return LeaveCalculation(
            employee_id=employee_id,
            employee_name=employee.name,
            leave_type=leave_type,
            total_entitlement=total_entitlement,
            used_days=used_days,
            remaining_days=remaining_days,
            pending_days=pending_days,
            available_days=available_days,
            year=year
        )

# Global database instance
db = LeaveDatabase()