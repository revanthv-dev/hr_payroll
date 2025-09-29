import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GenerateSecurityReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None,
               system_module: Optional[str] = None) -> str:
        
        access_controls = data.get("access_controls", {})
        employees = data.get("employees", {})
        results = []
        
        # Validate system module if provided
        if system_module:
            valid_modules = ["payroll", "vendor", "compliance"]
            if system_module not in valid_modules:
                return json.dumps({"error": f"Invalid system module. Must be one of: {', '.join(valid_modules)}"})
        
        for control in access_controls.values():
            # Apply filters
            if user_id and control.get("user_id") != user_id:
                continue
            if system_module and control.get("system_module") != system_module:
                continue
            
            # Enrich with user information
            control_copy = control.copy()
            user = employees.get(str(control.get("user_id")))
            if user:
                control_copy["user_name"] = f"{user.get('first_name')} {user.get('last_name')}"
                control_copy["user_email"] = user.get("email")
                control_copy["user_status"] = user.get("status")
            
            results.append(control_copy)
        
        # If querying for specific user, organize by module
        if user_id and not system_module:
            user_access = {
                "user_id": user_id,
                "access_by_module": {},
                "details": results
            }
            
            user = employees.get(str(user_id))
            if user:
                user_access["user_name"] = f"{user.get('first_name')} {user.get('last_name')}"
                user_access["user_email"] = user.get("email")
            
            for control in results:
                module = control.get("system_module")
                user_access["access_by_module"][module] = control.get("access_level")
            
            return json.dumps(user_access)
        
        # If querying for specific module, organize by access level
        if system_module and not user_id:
            module_access = {
                "system_module": system_module,
                "by_access_level": {
                    "admin": [],
                    "write": [],
                    "read": []
                },
                "total_users": len(results),
                "details": results
            }
            
            for control in results:
                level = control.get("access_level")
                if level in module_access["by_access_level"]:
                    module_access["by_access_level"][level].append({
                        "user_id": control.get("user_id"),
                        "user_name": control.get("user_name", ""),
                        "user_email": control.get("user_email", "")
                    })
            
            return json.dumps(module_access)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_security_report",
                "description": "Retrieve user access permissions by user or module",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "system_module": {"type": "string", "description": "Filter by system module (payroll, vendor, compliance)"}
                    },
                    "required": []
                }
            }
        }
