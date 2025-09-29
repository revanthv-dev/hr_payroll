import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetAttendanceRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, 
               date_from: Optional[str] = None, date_to: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        employees = data.get("employees", {})
        attendance_records = data.get("attendance_records", {})
        
        # Validate employee exists
        if str(employee_id) not in employees:
            return json.dumps({"error": f"Employee {employee_id} not found"})
        
        # Validate status if provided
        if status:
            valid_statuses = ["present", "absent", "half-day", "leave"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        results = []
        
        for record in attendance_records.values():
            # Filter by employee
            if record.get("employee_id") != employee_id:
                continue
            
            # Apply date filters
            if date_from and record.get("date") < date_from:
                continue
            if date_to and record.get("date") > date_to:
                continue
            
            # Apply status filter
            if status and record.get("status") != status:
                continue
            
            results.append(record)
        
        # Sort by date
        results.sort(key=lambda x: x.get("date", ""))
        
        # Calculate summary statistics
        summary = {
            "employee_id": employee_id,
            "total_records": len(results),
            "present": sum(1 for r in results if r.get("status") == "present"),
            "absent": sum(1 for r in results if r.get("status") == "absent"),
            "half_day": sum(1 for r in results if r.get("status") == "half-day"),
            "leave": sum(1 for r in results if r.get("status") == "leave"),
            "records": results
        }
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attendance_records",
                "description": "Retrieve attendance records by employee and date range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "date_from": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                        "date_to": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                        "status": {"type": "string", "description": "Filter by status (present, absent, half-day, leave)"}
                    },
                    "required": ["employee_id"]
                }
            }
        }
