import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CheckPayrollCompliance(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_id: Optional[str] = None,
               filing_type: Optional[str] = None, status: Optional[str] = None) -> str:
        
        payroll_compliance = data.get("payroll_compliance", {})
        payroll_records = data.get("payroll_records", {})
        results = []
        
        # Validate filing type if provided
        if filing_type:
            valid_types = ["W-2", "tax remittance"]
            if filing_type not in valid_types:
                return json.dumps({"error": f"Invalid filing type. Must be one of: {', '.join(valid_types)}"})
        
        # Validate status if provided
        if status:
            valid_statuses = ["filed", "pending", "delayed"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        for compliance in payroll_compliance.values():
            # Apply filters
            if payroll_id and compliance.get("payroll_id") != payroll_id:
                continue
            if filing_type and compliance.get("filing_type") != filing_type:
                continue
            if status and compliance.get("status") != status:
                continue
            
            # Enrich with payroll info
            compliance_copy = compliance.copy()
            payroll = payroll_records.get(str(compliance.get("payroll_id")))
            if payroll:
                compliance_copy["payroll_period"] = {
                    "start": payroll.get("period_start"),
                    "end": payroll.get("period_end"),
                    "employee_id": payroll.get("employee_id")
                }
            
            results.append(compliance_copy)
        
        # If specific payroll_id provided, also check if it needs compliance filings
        if payroll_id and str(payroll_id) in payroll_records:
            payroll = payroll_records[str(payroll_id)]
            if payroll.get("disbursed"):
                # Check if all required filings exist
                has_w2 = False
                has_tax_remittance = False
                
                for compliance in results:
                    if compliance.get("filing_type") == "W-2":
                        has_w2 = True
                    if compliance.get("filing_type") == "tax remittance":
                        has_tax_remittance = True
                
                compliance_status = {
                    "payroll_id": payroll_id,
                    "W-2_filed": has_w2,
                    "tax_remittance_filed": has_tax_remittance,
                    "compliance_records": results
                }
                
                return json.dumps(compliance_status)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_payroll_compliance",
                "description": "Check compliance status for payroll records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_id": {"type": "string", "description": "Filter by payroll record ID"},
                        "filing_type": {"type": "string", "description": "Filter by filing type (W-2, tax remittance)"},
                        "status": {"type": "string", "description": "Filter by status (filed, pending, delayed)"}
                    },
                    "required": []
                }
            }
        }
