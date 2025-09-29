import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class OnboardVendor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, tax_id: str, 
               bank_details: Optional[str] = "") -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        vendors = data.get("vendors", {})
        
        # Check for duplicate vendor by tax_id
        for vendor in vendors.values():
            if vendor.get("tax_id") == tax_id:
                return json.dumps({"error": f"Vendor with tax ID {tax_id} already exists"})
        
        vendor_id = generate_id(vendors)
        timestamp = "2025-10-01T00:00:00"
        
        new_vendor = {
            "id": vendor_id,
            "name": name,
            "tax_id": tax_id,
            "bank_details": bank_details,
            "created_at": timestamp
        }
        
        vendors[vendor_id] = new_vendor
        return json.dumps(new_vendor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "onboard_vendor",
                "description": "Register new vendors in system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the vendor"},
                        "tax_id": {"type": "string", "description": "Tax ID of the vendor (SSN format)"},
                        "bank_details": {"type": "string", "description": "Bank account details (optional)"}
                    },
                    "required": ["name", "tax_id"]
                }
            }
        }
