import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateVendorInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], vendor_id: str, invoice_number: str,
               amount: str, received_date: str, status: str = "received") -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        vendors = data.get("vendors", {})
        vendor_invoices = data.get("vendor_invoices", {})
        
        # Validate vendor exists
        if str(vendor_id) not in vendors:
            return json.dumps({"error": f"Vendor {vendor_id} not found"})
        
        # Validate status
        valid_statuses = ["received", "verified", "approved", "paid", "disputed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        # Check for duplicate invoice number
        for invoice in vendor_invoices.values():
            if invoice.get("invoice_number") == invoice_number:
                return json.dumps({"error": f"Invoice number {invoice_number} already exists"})
        
        invoice_id = generate_id(vendor_invoices)
        
        new_invoice = {
            "id": invoice_id,
            "vendor_id": vendor_id,
            "invoice_number": invoice_number,
            "amount": amount,
            "status": status,
            "received_date": received_date,
            "approved_date": None
        }
        
        vendor_invoices[invoice_id] = new_invoice
        return json.dumps(new_invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_vendor_invoice",
                "description": "Record received vendor invoices",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string", "description": "ID of the vendor"},
                        "invoice_number": {"type": "string", "description": "Invoice number (format: INV-XXXXX)"},
                        "amount": {"type": "string", "description": "Invoice amount as string"},
                        "received_date": {"type": "string", "description": "Date invoice was received (YYYY-MM-DD)"},
                        "status": {"type": "string", "description": "Invoice status (received, verified, approved, paid, disputed), defaults to received"}
                    },
                    "required": ["vendor_id", "invoice_number", "amount", "received_date"]
                }
            }
        }
