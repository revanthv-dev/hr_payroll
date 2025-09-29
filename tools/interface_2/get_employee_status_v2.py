import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetEmployeeStatusV2(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str) -> str:
        
        employees = data.get("employees", {})
        departments = data.get("departments", {})
        roles = data.get("roles", {})
        
        # Get employee
        employee = employees.get(str(employee_id))
        if not employee:
            return json.dumps({"error": f"Employee {employee_id} not found"})
        
        # Build status response
        status_info = {
            "employee_id": employee.get("id"),
            "name": f"{employee.get('first_name')} {employee.get('last_name')}",
            "email": employee.get("email"),
            "status": employee.get("status"),
            "hire_date": employee.get("hire_date")
        }
        
        # Add department info
        if employee.get("department_id"):
            department = departments.get(str(employee["department_id"]))
            if department:
                status_info["department"] = department.get("name")
        
        # Add role info
        if employee.get("role_id"):
            role = roles.get(str(employee["role_id"]))
            if role:
                status_info["role"] = role.get("title")
        
        # Add recent attendance summary
        attendance_records = data.get("attendance_records", {})
        recent_attendance = []
        for record in attendance_records.values():
            if record.get("employee_id") == employee_id:
                recent_attendance.append({
                    "date": record.get("date"),
                    "status": record.get("status")
                })
        
        # Sort by date and get last 5
        recent_attendance.sort(key=lambda x: x["date"], reverse=True)
        status_info["recent_attendance"] = recent_attendance[:5]
        
        # Add active leave requests
        leave_requests = data.get("leave_requests", {})
        active_leaves = []
        for request in leave_requests.values():
            if (request.get("employee_id") == employee_id and 
                request.get("status") in ["pending", "approved"]):
                active_leaves.append({
                    "type": request.get("leave_type"),
                    "start_date": request.get("start_date"),
                    "end_date": request.get("end_date"),
                    "status": request.get("status")
                })
        status_info["active_leave_requests"] = active_leaves
        
        return json.dumps(status_info)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_status_v2",
                "description": "Get current employment status and key details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"}
                    },
                    "required": ["employee_id"]
                }
            }
        }
