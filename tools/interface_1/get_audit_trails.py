import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetAuditTrails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: Optional[str] = None,
               entity_id: Optional[str] = None, action: Optional[str] = None,
               user_id: Optional[str] = None, date_from: Optional[str] = None,
               date_to: Optional[str] = None) -> str:
        
        audit_trails = data.get("audit_trails", {})
        employees = data.get("employees", {})
        results = []
        
        # Validate entity type if provided
        if entity_type:
            valid_types = ["payroll", "vendor", "compliance"]
            if entity_type not in valid_types:
                return json.dumps({"error": f"Invalid entity type. Must be one of: {', '.join(valid_types)}"})
        
        # Validate action if provided
        if action:
            valid_actions = ["create", "update", "delete", "approve", "reject", "view"]
            if action not in valid_actions:
                return json.dumps({"error": f"Invalid action. Must be one of: {', '.join(valid_actions)}"})
        
        for trail in audit_trails.values():
            # Apply filters
            if entity_type and trail.get("entity_type") != entity_type:
                continue
            if entity_id and trail.get("entity_id") != entity_id:
                continue
            if action and trail.get("action") != action:
                continue
            if user_id and trail.get("user_id") != user_id:
                continue
            if date_from and trail.get("timestamp") < date_from:
                continue
            if date_to and trail.get("timestamp") > date_to:
                continue
            
            # Enrich with user information
            trail_copy = trail.copy()
            user = employees.get(str(trail.get("user_id")))
            if user:
                trail_copy["user_name"] = f"{user.get('first_name')} {user.get('last_name')}"
                trail_copy["user_email"] = user.get("email")
            
            results.append(trail_copy)
        
        # Sort by timestamp (most recent first)
        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Create summary
        summary = {
            "total_trails": len(results),
            "by_action": {},
            "by_entity_type": {},
            "trails": results
        }
        
        for trail in results:
            # Count by action
            act = trail.get("action")
            if act not in summary["by_action"]:
                summary["by_action"][act] = 0
            summary["by_action"][act] += 1
            
            # Count by entity type
            etype = trail.get("entity_type")
            if etype not in summary["by_entity_type"]:
                summary["by_entity_type"][etype] = 0
            summary["by_entity_type"][etype] += 1
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_audit_trails",
                "description": "Get audit trail logs by entity, action, user, or time range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {"type": "string", "description": "Filter by entity type (payroll, vendor, compliance)"},
                        "entity_id": {"type": "string", "description": "Filter by specific entity ID"},
                        "action": {"type": "string", "description": "Filter by action (create, update, delete, approve, reject, view)"},
                        "user_id": {"type": "string", "description": "Filter by user ID who performed the action"},
                        "date_from": {"type": "string", "description": "Filter from date (YYYY-MM-DD)"},
                        "date_to": {"type": "string", "description": "Filter to date (YYYY-MM-DD)"}
                    },
                    "required": []
                }
            }
        }
