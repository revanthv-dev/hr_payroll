import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ArchiveAuditRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_id: str, deduction_type: str, 
               amount: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        payroll_records = data.get("payroll_records", {})
        payroll_deductions = data.get("payroll_deductions", {})
        
        # Validate payroll record exists
        if str(payroll_id) not in payroll_records:
            return json.dumps({"error": f"Payroll record {payroll_id} not found"})
        
        # Validate deduction type
        valid_types = ["tax", "retirement", "insurance", "loan", "savings"]
        if deduction_type not in valid_types:
            return json.dumps({"error": f"Invalid deduction type. Must be one of: {', '.join(valid_types)}"})
        
        deduction_id = generate_id(payroll_deductions)
        
        new_deduction = {
            "id": deduction_id,
            "payroll_id": payroll_id,
            "type": deduction_type,
            "amount": amount
        }
        
        payroll_deductions[deduction_id] = new_deduction
        return json.dumps(new_deduction)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "archive_audit_records",
                "description": "Apply tax, insurance, and other deductions to payroll",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_id": {"type": "string", "description": "ID of the payroll record"},
                        "deduction_type": {"type": "string", "description": "Type of deduction (tax, retirement, insurance, loan, savings)"},
                        "amount": {"type": "string", "description": "Deduction amount as string"}
                    },
                    "required": ["payroll_id", "deduction_type", "amount"]
                }
            }
        }
