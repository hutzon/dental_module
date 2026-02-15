from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string='Is a Patient', default=False)
    is_doctor = fields.Boolean(string='Is a Doctor', default=False)
    
    # History specific to patients
    patient_history_ids = fields.One2many(
        'dental.patient.history', 'patient_id', string='Medical History'
    )
    
    appointment_count = fields.Integer(compute='_compute_appointment_count', string="Appointment Count")

    def _compute_appointment_count(self):
        for partner in self:
            partner.appointment_count = self.env['dental.appointment'].search_count([
                '|', ('patient_id', '=', partner.id), ('doctor_id', '=', partner.id)
            ])

    next_appointment_id = fields.Many2one('dental.appointment', string='Next Appointment', compute='_compute_next_appointment')

    def _compute_next_appointment(self):
        for partner in self:
            next_app = self.env['dental.appointment'].search([
                ('patient_id', '=', partner.id),
                ('state', '=', 'confirmed'),
                ('date_start', '>=', fields.Datetime.now())
            ], order='date_start asc', limit=1)
            partner.next_appointment_id = next_app.id if next_app else False

    def action_view_appointments(self):
        self.ensure_one()
        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'res_model': 'dental.appointment',
            'view_mode': 'calendar,list,form',
            'domain': ['|', ('patient_id', '=', self.id), ('doctor_id', '=', self.id)],
            'context': {'default_patient_id': self.id} if self.is_patient else {'default_doctor_id': self.id},
        }
