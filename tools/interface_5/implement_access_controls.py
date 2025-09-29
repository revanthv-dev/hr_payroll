import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ImplementAccessControls(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_id: str) -> str:
        
        payroll_records = data.get("payroll_records", {})
        
        # Validate payroll record exists
        if str(payroll_id) not in payroll_records:
            return json.dumps({"error": f"Payroll record {payroll_id} not found"})
        
        payroll_record = payroll_records[str(payroll_id)]
        
        # Check if already disbursed
        if payroll_record.get("disbursed", False):
            return json.dumps({"error": f"Payroll record {payroll_id} has already been disbursed"})
        
        # Update disbursement status
        payroll_record["disbursed"] = True
        
        return json.dumps(payroll_record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "implement_access_controls",
                "description": "Mark payroll as disbursed and update status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_id": {"type": "string", "description": "ID of the payroll record to disburse"}
                    },
                    "required": ["payroll_id"]
                }
            }
        }
