from odoo import http
from odoo.http import request
from datetime import date, datetime
import logging

class EmployeeLeaveWebsite(http.Controller):

    @http.route('/leave/apply', type='http', auth='public', website=True, methods=['GET'])
    def leave_application_form(self):
        # Fetch all active leave types
        leave_types = request.env['hr.leave.type'].sudo().search([])
        return request.render('apply_leave.leave_application_template', {
            'leave_types': leave_types,
        })
    _logger = logging.getLogger(__name__)
    @http.route('/leave/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_leave_application(self, **kwargs):
        _logger.info("Received leave form data: %s", kwargs)

    @http.route('/leave/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_leave_application(self, **kwargs):
        id_number = kwargs.get('id_number')
        leave_date = kwargs.get('leave_date_from')
        leave_date_to = kwargs.get('leave_date_to')
        leave_type_id = kwargs.get('leave_type')  # Get the selected leave type ID

       

        try:
            leave_date = datetime.strptime(leave_date, '%Y-%m-%d')
            
        except ValueError:
            return request.render('employee_leave_app.leave_application_template', {
                 'error': "Invalid leave date format. Please use YYYY-MM-DD.",
        })

        # Search for the employee
        employee = request.env['hr.employee'].sudo().search([('identification_id', '=', id_number)], limit=1)

        if not employee:
            return request.render('apply_leave.leave_application_template', {
                'error': "Employee ID not found. Please try again.",
            })

        # Validate the leave type
        leave_type = request.env['hr.leave.type'].sudo().browse(int(leave_type_id))
        if not leave_type.exists():
            return request.render('apply_leave.leave_application_template', {
                'error': "Invalid leave type selected.",
            })

        # Create a leave record
        leave = request.env['hr.leave'].sudo().create({
            'employee_id': employee.id,
            'holiday_status_id': leave_type.id,
            'request_date_from': leave_date,
            'request_date_to': leave_date_to,
        })

        return request.render('apply_leave.leave_application_success', {
            'employee_name': employee.name,
        })

