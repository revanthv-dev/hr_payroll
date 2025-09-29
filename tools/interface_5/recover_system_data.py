import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class RecoverSystemData(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, date: str, 
               status: str, check_in: Optional[str] = None, 
               check_out: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        attendance_records = data.get("attendance_records", {})
        
        # Validate employee exists
        if str(employee_id) not in employees:
            return json.dumps({"error": f"Employee {employee_id} not found"})
        
        # Validate status
        valid_statuses = ["present", "absent", "half-day", "leave"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
        
        # Check for existing attendance record
        for record in attendance_records.values():
            if record.get("employee_id") == employee_id and record.get("date") == date:
                # Update existing record
                record["status"] = status
                record["check_in"] = check_in if status in ["present", "half-day"] else None
                record["check_out"] = check_out if status in ["present", "half-day"] else None
                return json.dumps(record)
        
        # Create new attendance record
        attendance_id = generate_id(attendance_records)
        
        new_attendance = {
            "id": attendance_id,
            "employee_id": employee_id,
            "date": date,
            "check_in": check_in if status in ["present", "half-day"] else None,
            "check_out": check_out if status in ["present", "half-day"] else None,
            "status": status
        }
        
        attendance_records[attendance_id] = new_attendance
        return json.dumps(new_attendance)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "recover_system_data",
                "description": "Record daily employee attendance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "date": {"type": "string", "description": "Date of attendance (YYYY-MM-DD)"},
                        "status": {"type": "string", "description": "Attendance status (present, absent, half-day, leave)"},
                        "check_in": {"type": "string", "description": "Check-in time (HH:MM:SS) (optional, only for present/half-day)"},
                        "check_out": {"type": "string", "description": "Check-out time (HH:MM:SS) (optional, only for present/half-day)"}
                    },
                    "required": ["employee_id", "date", "status"]
                }
            }
        }
