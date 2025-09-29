import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetLeaveRequestsV3(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: Optional[str] = None,
               status: Optional[str] = None, leave_type: Optional[str] = None,
               date_from: Optional[str] = None, date_to: Optional[str] = None) -> str:
        
        leave_requests = data.get("leave_requests", {})
        employees = data.get("employees", {})
        results = []
        
        # Validate status if provided
        if status:
            valid_statuses = ["pending", "approved", "rejected"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        # Validate leave type if provided
        if leave_type:
            valid_types = ["sick", "casual", "paid", "unpaid"]
            if leave_type not in valid_types:
                return json.dumps({"error": f"Invalid leave type. Must be one of: {', '.join(valid_types)}"})
        
        for request in leave_requests.values():
            # Apply filters
            if employee_id and request.get("employee_id") != employee_id:
                continue
            if status and request.get("status") != status:
                continue
            if leave_type and request.get("leave_type") != leave_type:
                continue
            if date_from and request.get("start_date") < date_from:
                continue
            if date_to and request.get("end_date") > date_to:
                continue
            
            # Enrich with employee and approver names
            request_copy = request.copy()
            
            emp = employees.get(str(request.get("employee_id")))
            if emp:
                request_copy["employee_name"] = f"{emp.get('first_name')} {emp.get('last_name')}"
            
            if request.get("approved_by"):
                approver = employees.get(str(request.get("approved_by")))
                if approver:
                    request_copy["approver_name"] = f"{approver.get('first_name')} {approver.get('last_name')}"
            
            results.append(request_copy)
        
        # Sort by requested date
        results.sort(key=lambda x: x.get("requested_at", ""), reverse=True)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_leave_requests_v3",
                "description": "Get leave requests by employee, status, or date range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, approved, rejected)"},
                        "leave_type": {"type": "string", "description": "Filter by leave type (sick, casual, paid, unpaid)"},
                        "date_from": {"type": "string", "description": "Filter from date (YYYY-MM-DD)"},
                        "date_to": {"type": "string", "description": "Filter to date (YYYY-MM-DD)"}
                    },
                    "required": []
                }
            }
        }
