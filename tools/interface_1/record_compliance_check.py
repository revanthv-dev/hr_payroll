import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class RecordComplianceCheck(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], rule_id: str, entity_type: str,
               entity_id: str, status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        compliance_rules = data.get("compliance_rules", {})
        compliance_checks = data.get("compliance_checks", {})
        
        # Validate rule exists
        if str(rule_id) not in compliance_rules:
            return json.dumps({"error": f"Compliance rule {rule_id} not found"})
        
        # Validate entity type
        valid_entity_types = ["employee", "vendor", "payroll"]
        if entity_type not in valid_entity_types:
            return json.dumps({"error": f"Invalid entity type. Must be one of: {', '.join(valid_entity_types)}"})
        
        # Validate entity exists based on type
        if entity_type == "employee":
            entities = data.get("employees", {})
        elif entity_type == "vendor":
            entities = data.get("vendors", {})
        else:  # payroll
            entities = data.get("payroll_records", {})
        
        if str(entity_id) not in entities:
            return json.dumps({"error": f"{entity_type.capitalize()} {entity_id} not found"})
        
        # Validate status
        valid_statuses = ["compliant", "violation"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        check_id = generate_id(compliance_checks)
        timestamp = "2025-10-01T00:00:00"
        
        new_check = {
            "id": check_id,
            "rule_id": rule_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "status": status,
            "checked_at": timestamp
        }
        
        compliance_checks[check_id] = new_check
        return json.dumps(new_check)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_compliance_check",
                "description": "Record compliance check results",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string", "description": "ID of the compliance rule"},
                        "entity_type": {"type": "string", "description": "Type of entity being checked (employee, vendor, payroll)"},
                        "entity_id": {"type": "string", "description": "ID of the entity being checked"},
                        "status": {"type": "string", "description": "Compliance status (compliant, violation)"}
                    },
                    "required": ["rule_id", "entity_type", "entity_id", "status"]
                }
            }
        }
