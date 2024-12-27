from odoo import models, fields, api, exceptions

class EmployeeLeave(models.Model):
    _name = 'apply.leave'
    _description = 'Employee Leave Application'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True)
    id_number = fields.Char(string="Employee ID", required=True)
    leave_date_from = fields.Date(string="From", required=True)
    leave_date_to = fields.Date(string="To", required=True)

    @api.onchange('id_number')
    def _onchange_id_number(self):
        if self.id_number:
            employee = self.env['hr.employee'].search([('identification_id', '=', self.id_number)], limit=1)
            if employee:
                self.employee_id = employee.id
            else:
                self.employee_id = False
                return {
                    'warning': {
                        'title': "ID Not Found",
                        'message': "No employee found with the entered ID number."
                    }
                }

    def action_submit(self):
        # Logic to process leave submission
        if not self.leave_date_from or not self.leave_date_to:
            raise exceptions.UserError("Please fill in all required fields.")
        # Create leave record or notify HR
        # ...
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_cancel(self):
        pass