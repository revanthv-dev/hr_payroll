import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class SubmitBonusRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, period_start: str, 
               period_end: str, gross_pay: str, deductions: str, 
               net_pay: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        payroll_records = data.get("payroll_records", {})
        
        # Validate employee exists
        if str(employee_id) not in employees:
            return json.dumps({"error": f"Employee {employee_id} not found"})
        
        # Check for duplicate payroll record
        for record in payroll_records.values():
            if (record.get("employee_id") == employee_id and 
                record.get("period_start") == period_start and
                record.get("period_end") == period_end):
                return json.dumps({"error": f"Payroll record already exists for employee {employee_id} for period {period_start} to {period_end}"})
        
        payroll_id = generate_id(payroll_records)
        timestamp = "2025-10-01T00:00:00"
        
        new_payroll = {
            "id": payroll_id,
            "employee_id": employee_id,
            "period_start": period_start,
            "period_end": period_end,
            "gross_pay": gross_pay,
            "deductions": deductions,
            "net_pay": net_pay,
            "disbursed": False,
            "created_at": timestamp
        }
        
        payroll_records[payroll_id] = new_payroll
        return json.dumps(new_payroll)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_bonus_request",
                "description": "Process complete payroll for employees",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "period_start": {"type": "string", "description": "Start date of payroll period (YYYY-MM-DD)"},
                        "period_end": {"type": "string", "description": "End date of payroll period (YYYY-MM-DD)"},
                        "gross_pay": {"type": "string", "description": "Gross pay amount as string"},
                        "deductions": {"type": "string", "description": "Total deductions amount as string"},
                        "net_pay": {"type": "string", "description": "Net pay amount as string"}
                    },
                    "required": ["employee_id", "period_start", "period_end", "gross_pay", "deductions", "net_pay"]
                }
            }
        }
