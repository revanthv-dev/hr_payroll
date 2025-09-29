import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ApproveOvertimeRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, adjustment_type: str,
               amount: str, effective_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        payroll_adjustments = data.get("payroll_adjustments", {})
        
        # Validate employee exists
        if str(employee_id) not in employees:
            return json.dumps({"error": f"Employee {employee_id} not found"})
        
        # Validate adjustment type
        valid_types = ["retro pay", "error correction", "advance", "final settlement"]
        if adjustment_type not in valid_types:
            return json.dumps({"error": f"Invalid adjustment type. Must be one of: {', '.join(valid_types)}"})
        
        adjustment_id = generate_id(payroll_adjustments)
        
        new_adjustment = {
            "id": adjustment_id,
            "employee_id": employee_id,
            "adjustment_type": adjustment_type,
            "amount": amount,
            "effective_date": effective_date
        }
        
        payroll_adjustments[adjustment_id] = new_adjustment
        return json.dumps(new_adjustment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "approve_overtime_request",
                "description": "Create payroll adjustments for corrections, advances, retro pay",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "adjustment_type": {"type": "string", "description": "Type of adjustment (retro pay, error correction, advance, final settlement)"},
                        "amount": {"type": "string", "description": "Adjustment amount as string"},
                        "effective_date": {"type": "string", "description": "Effective date of adjustment (YYYY-MM-DD)"}
                    },
                    "required": ["employee_id", "adjustment_type", "amount", "effective_date"]
                }
            }
        }
