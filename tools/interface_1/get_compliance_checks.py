import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetComplianceChecks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: Optional[str] = None,
               entity_id: Optional[str] = None, status: Optional[str] = None,
               rule_id: Optional[str] = None) -> str:
        
        compliance_checks = data.get("compliance_checks", {})
        compliance_rules = data.get("compliance_rules", {})
        results = []
        
        # Validate entity type if provided
        if entity_type:
            valid_types = ["employee", "vendor", "payroll"]
            if entity_type not in valid_types:
                return json.dumps({"error": f"Invalid entity type. Must be one of: {', '.join(valid_types)}"})
        
        # Validate status if provided
        if status:
            valid_statuses = ["compliant", "violation"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        for check in compliance_checks.values():
            # Apply filters
            if entity_type and check.get("entity_type") != entity_type:
                continue
            if entity_id and check.get("entity_id") != entity_id:
                continue
            if status and check.get("status") != status:
                continue
            if rule_id and check.get("rule_id") != rule_id:
                continue
            
            # Enrich with rule information
            check_copy = check.copy()
            rule = compliance_rules.get(str(check.get("rule_id")))
            if rule:
                check_copy["rule_details"] = {
                    "category": rule.get("category"),
                    "jurisdiction": rule.get("jurisdiction"),
                    "effective_date": rule.get("effective_date")
                }
            
            results.append(check_copy)
        
        # Group by entity type for summary
        summary = {
            "total_checks": len(results),
            "compliant": sum(1 for r in results if r.get("status") == "compliant"),
            "violations": sum(1 for r in results if r.get("status") == "violation"),
            "by_entity_type": {},
            "checks": results
        }
        
        for check in results:
            etype = check.get("entity_type")
            if etype not in summary["by_entity_type"]:
                summary["by_entity_type"][etype] = {
                    "total": 0,
                    "compliant": 0,
                    "violations": 0
                }
            summary["by_entity_type"][etype]["total"] += 1
            if check.get("status") == "compliant":
                summary["by_entity_type"][etype]["compliant"] += 1
            else:
                summary["by_entity_type"][etype]["violations"] += 1
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_compliance_checks",
                "description": "Retrieve compliance check results by entity type and status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {"type": "string", "description": "Filter by entity type (employee, vendor, payroll)"},
                        "entity_id": {"type": "string", "description": "Filter by specific entity ID"},
                        "status": {"type": "string", "description": "Filter by status (compliant, violation)"},
                        "rule_id": {"type": "string", "description": "Filter by compliance rule ID"}
                    },
                    "required": []
                }
            }
        }
