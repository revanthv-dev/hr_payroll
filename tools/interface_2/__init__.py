# Import all tool classes for interface_2

from .bulk_employee_update import BulkEmployeeUpdate
from .create_department import CreateDepartment
from .create_disciplinary_action import CreateDisciplinaryAction
from .create_employee_profile import CreateEmployeeProfile
from .create_role import CreateRole
from .generate_employee_report import GenerateEmployeeReport
from .get_access_controls_v2 import GetAccessControlsV2
from .get_attendance_records_v2 import GetAttendanceRecordsV2
from .get_audit_trails_v2 import GetAuditTrailsV2
from .get_compliance_checks_v2 import GetComplianceChecksV2
from .get_employee_details_v2 import GetEmployeeDetailsV2
from .get_employee_status_v2 import GetEmployeeStatusV2
from .get_leave_requests_v2 import GetLeaveRequestsV2
from .get_payroll_records_v2 import GetPayrollRecordsV2
from .get_payroll_summary_v2 import GetPayrollSummaryV2
from .get_vendor_details_v2 import GetVendorDetailsV2
from .get_vendor_invoices_v2 import GetVendorInvoicesV2
from .manage_employee_access import ManageEmployeeAccess
from .manage_employee_queries import ManageEmployeeQueries
from .manage_workflow_approval import ManageWorkflowApproval
from .process_employee_termination import ProcessEmployeeTermination
from .search_employees_v2 import SearchEmployeesV2
from .send_employee_notification import SendEmployeeNotification
from .transfer_employee_department import TransferEmployeeDepartment
from .update_employee_contact import UpdateEmployeeContact

__all__ = [
    'BulkEmployeeUpdate',
    'CreateDepartment',
    'CreateDisciplinaryAction',
    'CreateEmployeeProfile',
    'CreateRole',
    'GenerateEmployeeReport',
    'GetAccessControlsV2',
    'GetAttendanceRecordsV2',
    'GetAuditTrailsV2',
    'GetComplianceChecksV2',
    'GetEmployeeDetailsV2',
    'GetEmployeeStatusV2',
    'GetLeaveRequestsV2',
    'GetPayrollRecordsV2',
    'GetPayrollSummaryV2',
    'GetVendorDetailsV2',
    'GetVendorInvoicesV2',
    'ManageEmployeeAccess',
    'ManageEmployeeQueries',
    'ManageWorkflowApproval',
    'ProcessEmployeeTermination',
    'SearchEmployeesV2',
    'SendEmployeeNotification',
    'TransferEmployeeDepartment',
    'UpdateEmployeeContact',
]
