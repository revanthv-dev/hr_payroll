import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetPayrollSummaryV4(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], period_start: str, period_end: str) -> str:
        
        payroll_records = data.get("payroll_records", {})
        payroll_deductions = data.get("payroll_deductions", {})
        
        summary = {
            "period_start": period_start,
            "period_end": period_end,
            "total_employees": 0,
            "total_gross_pay": 0.0,
            "total_deductions": 0.0,
            "total_net_pay": 0.0,
            "disbursed_count": 0,
            "pending_count": 0,
            "deductions_by_type": {}
        }
        
        processed_employees = set()
        
        for record in payroll_records.values():
            # Check if record is within period
            if (record.get("period_start") >= period_start and 
                record.get("period_end") <= period_end):
                
                processed_employees.add(record.get("employee_id"))
                
                try:
                    summary["total_gross_pay"] += float(record.get("gross_pay", "0"))
                    summary["total_deductions"] += float(record.get("deductions", "0"))
                    summary["total_net_pay"] += float(record.get("net_pay", "0"))
                except:
                    pass
                
                if record.get("disbursed"):
                    summary["disbursed_count"] += 1
                else:
                    summary["pending_count"] += 1
                
                # Process deductions for this payroll
                for deduction in payroll_deductions.values():
                    if deduction.get("payroll_id") == record.get("id"):
                        deduction_type = deduction.get("type")
                        if deduction_type not in summary["deductions_by_type"]:
                            summary["deductions_by_type"][deduction_type] = 0.0
                        try:
                            summary["deductions_by_type"][deduction_type] += float(deduction.get("amount", "0"))
                        except:
                            pass
        
        summary["total_employees"] = len(processed_employees)
        
        # Convert numeric values to strings
        summary["total_gross_pay"] = str(summary["total_gross_pay"])
        summary["total_deductions"] = str(summary["total_deductions"])
        summary["total_net_pay"] = str(summary["total_net_pay"])
        summary["deductions_by_type"] = {k: str(v) for k, v in summary["deductions_by_type"].items()}
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payroll_summary_v4",
                "description": "Get payroll summary for a period (gross, deductions, net pay)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "period_start": {"type": "string", "description": "Start date of period (YYYY-MM-DD)"},
                        "period_end": {"type": "string", "description": "End date of period (YYYY-MM-DD)"}
                    },
                    "required": ["period_start", "period_end"]
                }
            }
        }
