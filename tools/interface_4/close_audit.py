import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CloseAudit(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, entity_id: str,
               action: str, user_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        audit_trails = data.get("audit_trails", {})
        
        # Validate entity type
        valid_entity_types = ["payroll", "vendor", "compliance"]
        if entity_type not in valid_entity_types:
            return json.dumps({"error": f"Invalid entity type. Must be one of: {', '.join(valid_entity_types)}"})
        
        # Validate entity exists based on type
        if entity_type == "payroll":
            entities = data.get("payroll_records", {})
        elif entity_type == "vendor":
            entities = data.get("vendors", {})
        else:  # compliance
            entities = data.get("compliance_rules", {})
        
        if str(entity_id) not in entities:
            return json.dumps({"error": f"{entity_type.capitalize()} {entity_id} not found"})
        
        # Validate user exists
        if str(user_id) not in employees:
            return json.dumps({"error": f"User {user_id} not found"})
        
        # Validate action
        valid_actions = ["create", "update", "delete", "approve", "reject", "view"]
        if action not in valid_actions:
            return json.dumps({"error": f"Invalid action. Must be one of: {', '.join(valid_actions)}"})
        
        trail_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        new_trail = {
            "id": trail_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": action,
            "user_id": user_id,
            "timestamp": timestamp
        }
        
        audit_trails[trail_id] = new_trail
        return json.dumps(new_trail)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "close_audit",
                "description": "Log all system actions for audit purposes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {"type": "string", "description": "Type of entity (payroll, vendor, compliance)"},
                        "entity_id": {"type": "string", "description": "ID of the entity"},
                        "action": {"type": "string", "description": "Action performed (create, update, delete, approve, reject, view)"},
                        "user_id": {"type": "string", "description": "ID of the user performing the action"}
                    },
                    "required": ["entity_type", "entity_id", "action", "user_id"]
                }
            }
        }
