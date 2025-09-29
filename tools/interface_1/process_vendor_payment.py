import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ProcessVendorPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_method: str,
               payment_date: str, amount: str, advice_sent: bool = False) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        vendor_invoices = data.get("vendor_invoices", {})
        vendor_payments = data.get("vendor_payments", {})
        
        # Validate invoice exists
        if str(invoice_id) not in vendor_invoices:
            return json.dumps({"error": f"Invoice {invoice_id} not found"})
        
        # Validate payment method
        valid_methods = ["ACH", "wire", "check", "cash"]
        if payment_method not in valid_methods:
            return json.dumps({"error": f"Invalid payment method. Must be one of: {', '.join(valid_methods)}"})
        
        # Check if invoice already paid
        invoice = vendor_invoices[str(invoice_id)]
        if invoice.get("status") == "paid":
            return json.dumps({"error": f"Invoice {invoice_id} has already been paid"})
        
        payment_id = generate_id(vendor_payments)
        
        new_payment = {
            "id": payment_id,
            "invoice_id": invoice_id,
            "payment_method": payment_method,
            "payment_date": payment_date,
            "amount": amount,
            "advice_sent": advice_sent
        }
        
        vendor_payments[payment_id] = new_payment
        
        # Update invoice status to paid
        invoice["status"] = "paid"
        invoice["approved_date"] = payment_date
        
        return json.dumps(new_payment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_vendor_payment",
                "description": "Process and record vendor payments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice to pay"},
                        "payment_method": {"type": "string", "description": "Payment method (ACH, wire, check, cash)"},
                        "payment_date": {"type": "string", "description": "Date of payment (YYYY-MM-DD)"},
                        "amount": {"type": "string", "description": "Payment amount as string"},
                        "advice_sent": {"type": "boolean", "description": "Whether payment advice was sent (True/False), defaults to False"}
                    },
                    "required": ["invoice_id", "payment_method", "payment_date", "amount"]
                }
            }
        }
