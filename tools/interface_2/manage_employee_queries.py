import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageEmployeeQueries(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, employee_id: Optional[str] = None,
               leave_type: Optional[str] = None, start_date: Optional[str] = None,
               end_date: Optional[str] = None, reason: Optional[str] = "",
               leave_request_id: Optional[str] = None, status: Optional[str] = None,
               approved_by: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        leave_requests = data.get("leave_requests", {})
        
        if action == "create":
            # Validate required fields for creation
            if not all([employee_id, leave_type, start_date, end_date]):
                return json.dumps({"error": "Missing required fields for creating leave request"})
            
            # Validate employee exists
            if str(employee_id) not in employees:
                return json.dumps({"error": f"Employee {employee_id} not found"})
            
            # Validate leave type
            valid_types = ["sick", "casual", "paid", "unpaid"]
            if leave_type not in valid_types:
                return json.dumps({"error": f"Invalid leave type. Must be one of: {', '.join(valid_types)}"})
            
            request_id = generate_id(leave_requests)
            timestamp = "2025-10-01T00:00:00"
            
            new_request = {
                "id": request_id,
                "employee_id": employee_id,
                "leave_type": leave_type,
                "start_date": start_date,
                "end_date": end_date,
                "reason": reason,
                "status": "pending",
                "approved_by": None,
                "requested_at": timestamp
            }
            
            leave_requests[request_id] = new_request
            return json.dumps(new_request)
            
        elif action == "update":
            # Validate leave request exists
            if not leave_request_id or str(leave_request_id) not in leave_requests:
                return json.dumps({"error": f"Leave request {leave_request_id} not found"})
            
            request = leave_requests[str(leave_request_id)]
            
            # Validate status if provided
            if status:
                valid_statuses = ["pending", "approved", "rejected"]
                if status not in valid_statuses:
                    return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
                
                # If approving/rejecting, validate approver
                if status in ["approved", "rejected"]:
                    if not approved_by:
                        return json.dumps({"error": "Approver ID required for approval/rejection"})
                    if str(approved_by) not in employees:
                        return json.dumps({"error": f"Approver {approved_by} not found"})
                    request["approved_by"] = approved_by
                
                request["status"] = status
            
            return json.dumps(request)
        
        else:
            return json.dumps({"error": f"Invalid action. Must be 'create' or 'update'"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_employee_queries",
                "description": "Create or update/approve leave requests",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "description": "Action to perform (create, update)"},
                        "employee_id": {"type": "string", "description": "ID of the employee (required for create)"},
                        "leave_type": {"type": "string", "description": "Type of leave (sick, casual, paid, unpaid) (required for create)"},
                        "start_date": {"type": "string", "description": "Start date of leave (YYYY-MM-DD) (required for create)"},
                        "end_date": {"type": "string", "description": "End date of leave (YYYY-MM-DD) (required for create)"},
                        "reason": {"type": "string", "description": "Reason for leave (optional)"},
                        "leave_request_id": {"type": "string", "description": "ID of leave request (required for update)"},
                        "status": {"type": "string", "description": "Status to update to (pending, approved, rejected)"},
                        "approved_by": {"type": "string", "description": "ID of approver (required when approving/rejecting)"}
                    },
                    "required": ["action"]
                }
            }
        }
