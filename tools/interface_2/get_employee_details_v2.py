import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetEmployeeDetailsV2(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: Optional[str] = None, 
               email: Optional[str] = None, first_name: Optional[str] = None,
               last_name: Optional[str] = None) -> str:
        
        employees = data.get("employees", {})
        departments = data.get("departments", {})
        roles = data.get("roles", {})
        
        # Find employee
        employee = None
        
        if employee_id:
            employee = employees.get(str(employee_id))
        elif email:
            for emp in employees.values():
                if emp.get("email", "").lower() == email.lower():
                    employee = emp
                    break
        elif first_name and last_name:
            for emp in employees.values():
                if (emp.get("first_name", "").lower() == first_name.lower() and 
                    emp.get("last_name", "").lower() == last_name.lower()):
                    employee = emp
                    break
        else:
            return json.dumps({"error": "Must provide employee_id, email, or both first_name and last_name"})
        
        if not employee:
            return json.dumps({"error": "Employee not found"})
        
        # Enrich with department and role information
        result = employee.copy()
        
        if employee.get("department_id"):
            department = departments.get(str(employee["department_id"]))
            if department:
                result["department_name"] = department.get("name")
        
        if employee.get("role_id"):
            role = roles.get(str(employee["role_id"]))
            if role:
                result["role_title"] = role.get("title")
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_details_v2",
                "description": "Retrieve employee information by ID, email, or name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "email": {"type": "string", "description": "Email address of the employee"},
                        "first_name": {"type": "string", "description": "First name of the employee"},
                        "last_name": {"type": "string", "description": "Last name of the employee"}
                    },
                    "required": []
                }
            }
        }
