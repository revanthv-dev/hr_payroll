import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class InvestigateSecurityIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, user_id: str, 
               system_module: str, access_level: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        access_controls = data.get("access_controls", {})
        
        # Validate user exists
        if str(user_id) not in employees:
            return json.dumps({"error": f"User {user_id} not found"})
        
        # Validate system module
        valid_modules = ["payroll", "vendor", "compliance"]
        if system_module not in valid_modules:
            return json.dumps({"error": f"Invalid system module. Must be one of: {', '.join(valid_modules)}"})
        
        if action == "grant" or action == "update":
            # Validate access level
            if not access_level:
                return json.dumps({"error": "Access level required for grant/update action"})
            
            valid_levels = ["read", "write", "admin"]
            if access_level not in valid_levels:
                return json.dumps({"error": f"Invalid access level. Must be one of: {', '.join(valid_levels)}"})
            
            # Check if access control already exists
            for control_id, control in access_controls.items():
                if control.get("user_id") == user_id and control.get("system_module") == system_module:
                    # Update existing
                    control["access_level"] = access_level
                    return json.dumps(control)
            
            # Create new access control
            control_id = generate_id(access_controls)
            
            new_control = {
                "id": control_id,
                "user_id": user_id,
                "system_module": system_module,
                "access_level": access_level
            }
            
            access_controls[control_id] = new_control
            return json.dumps(new_control)
            
        elif action == "revoke":
            # Find and remove access control
            for control_id, control in list(access_controls.items()):
                if control.get("user_id") == user_id and control.get("system_module") == system_module:
                    del access_controls[control_id]
                    return json.dumps({"message": f"Access revoked for user {user_id} on module {system_module}"})
            
            return json.dumps({"error": f"No access control found for user {user_id} on module {system_module}"})
        
        else:
            return json.dumps({"error": f"Invalid action. Must be 'grant', 'update', or 'revoke'"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "investigate_security_incident",
                "description": "Grant, update, or revoke system access",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "description": "Action to perform (grant, update, revoke)"},
                        "user_id": {"type": "string", "description": "ID of the user"},
                        "system_module": {"type": "string", "description": "System module (payroll, vendor, compliance)"},
                        "access_level": {"type": "string", "description": "Access level (read, write, admin) (required for grant/update)"}
                    },
                    "required": ["action", "user_id", "system_module"]
                }
            }
        }
