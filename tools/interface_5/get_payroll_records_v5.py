import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetPayrollRecordsV5(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: Optional[str] = None,
               period_start: Optional[str] = None, period_end: Optional[str] = None,
               disbursed: Optional[bool] = None) -> str:
        
        payroll_records = data.get("payroll_records", {})
        payroll_deductions = data.get("payroll_deductions", {})
        results = []
        
        for record in payroll_records.values():
            # Apply filters
            if employee_id and record.get("employee_id") != employee_id:
                continue
            if period_start and record.get("period_start") < period_start:
                continue
            if period_end and record.get("period_end") > period_end:
                continue
            if disbursed is not None and record.get("disbursed") != disbursed:
                continue
            
            # Enrich with deductions
            record_copy = record.copy()
            deductions_list = []
            total_deductions = 0
            
            for deduction in payroll_deductions.values():
                if deduction.get("payroll_id") == record.get("id"):
                    deductions_list.append({
                        "type": deduction.get("type"),
                        "amount": deduction.get("amount")
                    })
                    try:
                        total_deductions += float(deduction.get("amount", "0"))
                    except:
                        pass
            
            record_copy["deductions_breakdown"] = deductions_list
            record_copy["total_deductions_calculated"] = str(total_deductions)
            
            results.append(record_copy)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payroll_records_v5",
                "description": "Retrieve payroll records by employee, period, or status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "period_start": {"type": "string", "description": "Filter by period start date (YYYY-MM-DD)"},
                        "period_end": {"type": "string", "description": "Filter by period end date (YYYY-MM-DD)"},
                        "disbursed": {"type": "boolean", "description": "Filter by disbursement status (True/False)"}
                    },
                    "required": []
                }
            }
        }
