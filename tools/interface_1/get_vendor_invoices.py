import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetVendorInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], vendor_id: Optional[str] = None,
               status: Optional[str] = None, date_from: Optional[str] = None,
               date_to: Optional[str] = None) -> str:
        
        vendor_invoices = data.get("vendor_invoices", {})
        vendor_payments = data.get("vendor_payments", {})
        results = []
        
        # Validate status if provided
        if status:
            valid_statuses = ["received", "verified", "approved", "paid", "disputed"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        for invoice in vendor_invoices.values():
            # Apply filters
            if vendor_id and invoice.get("vendor_id") != vendor_id:
                continue
            if status and invoice.get("status") != status:
                continue
            if date_from and invoice.get("received_date") < date_from:
                continue
            if date_to and invoice.get("received_date") > date_to:
                continue
            
            # Enrich with payment information
            invoice_copy = invoice.copy()
            payments = []
            
            for payment in vendor_payments.values():
                if payment.get("invoice_id") == invoice.get("id"):
                    payments.append({
                        "payment_date": payment.get("payment_date"),
                        "payment_method": payment.get("payment_method"),
                        "amount": payment.get("amount"),
                        "advice_sent": payment.get("advice_sent")
                    })
            
            invoice_copy["payments"] = payments
            
            results.append(invoice_copy)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_vendor_invoices",
                "description": "Get vendor invoices by status, date range, or vendor ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string", "description": "Filter by vendor ID"},
                        "status": {"type": "string", "description": "Filter by status (received, verified, approved, paid, disputed)"},
                        "date_from": {"type": "string", "description": "Filter from date (YYYY-MM-DD)"},
                        "date_to": {"type": "string", "description": "Filter to date (YYYY-MM-DD)"}
                    },
                    "required": []
                }
            }
        }
