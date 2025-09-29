import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetVendorDetailsV2(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], vendor_id: Optional[str] = None,
               name: Optional[str] = None, tax_id: Optional[str] = None) -> str:
        
        vendors = data.get("vendors", {})
        vendor_contracts = data.get("vendor_contracts", {})
        
        # Find vendor
        vendor = None
        
        if vendor_id:
            vendor = vendors.get(str(vendor_id))
        elif name:
            for v in vendors.values():
                if v.get("name", "").lower() == name.lower():
                    vendor = v
                    break
        elif tax_id:
            for v in vendors.values():
                if v.get("tax_id") == tax_id:
                    vendor = v
                    break
        else:
            return json.dumps({"error": "Must provide vendor_id, name, or tax_id"})
        
        if not vendor:
            return json.dumps({"error": "Vendor not found"})
        
        # Enrich with contract information
        result = vendor.copy()
        contracts = []
        
        for contract in vendor_contracts.values():
            if contract.get("vendor_id") == vendor.get("id"):
                contracts.append({
                    "contract_number": contract.get("contract_number"),
                    "po_number": contract.get("po_number"),
                    "start_date": contract.get("start_date"),
                    "end_date": contract.get("end_date"),
                    "compliance_check": contract.get("compliance_check")
                })
        
        result["contracts"] = contracts
        
        # Add invoice summary
        vendor_invoices = data.get("vendor_invoices", {})
        invoice_summary = {
            "total_invoices": 0,
            "received": 0,
            "verified": 0,
            "approved": 0,
            "paid": 0,
            "disputed": 0,
            "total_amount": 0.0
        }
        
        for invoice in vendor_invoices.values():
            if invoice.get("vendor_id") == vendor.get("id"):
                invoice_summary["total_invoices"] += 1
                status = invoice.get("status")
                if status in invoice_summary:
                    invoice_summary[status] += 1
                try:
                    invoice_summary["total_amount"] += float(invoice.get("amount", "0"))
                except:
                    pass
        
        invoice_summary["total_amount"] = str(invoice_summary["total_amount"])
        result["invoice_summary"] = invoice_summary
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_vendor_details_v2",
                "description": "Retrieve vendor information by ID, name, or tax ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string", "description": "ID of the vendor"},
                        "name": {"type": "string", "description": "Name of the vendor"},
                        "tax_id": {"type": "string", "description": "Tax ID of the vendor"}
                    },
                    "required": []
                }
            }
        }
