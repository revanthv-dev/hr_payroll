import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class SearchEmployees(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: Optional[str] = None,
               department_id: Optional[str] = None, role_id: Optional[str] = None,
               hire_date_from: Optional[str] = None, 
               hire_date_to: Optional[str] = None) -> str:
        
        employees = data.get("employees", {})
        results = []
        
        # Validate status if provided
        if status:
            valid_statuses = ["active", "probation", "resigned", "retired", "terminated"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        for employee in employees.values():
            # Apply filters
            if status and employee.get("status") != status:
                continue
            if department_id and employee.get("department_id") != department_id:
                continue
            if role_id and employee.get("role_id") != role_id:
                continue
            if hire_date_from and employee.get("hire_date") < hire_date_from:
                continue
            if hire_date_to and employee.get("hire_date") > hire_date_to:
                continue
            
            results.append(employee)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_employees",
                "description": "Search employees with filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Employment status (active, probation, resigned, retired, terminated)"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "role_id": {"type": "string", "description": "Filter by role ID"},
                        "hire_date_from": {"type": "string", "description": "Hire date from (YYYY-MM-DD)"},
                        "hire_date_to": {"type": "string", "description": "Hire date to (YYYY-MM-DD)"}
                    },
                    "required": []
                }
            }
        }
