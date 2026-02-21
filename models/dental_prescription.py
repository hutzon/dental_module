from odoo import models, fields, api, _

class DentalPrescription(models.Model):
    _name = 'dental.prescription'
    _description = 'Medical Prescription'
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    appointment_id = fields.Many2one('dental.appointment', string='Appointment', ondelete='set null')
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, domain=[('is_patient', '=', True)])
    doctor_id = fields.Many2one('res.partner', string='Doctor', required=True, domain=[('is_doctor', '=', True)])
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    notes = fields.Text(string='General Notes / Instructions')
    
    line_ids = fields.One2many('dental.prescription.line', 'prescription_id', string='Prescription Lines')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('dental.prescription') or _('New')
        return super().create(vals_list)

    @api.onchange('appointment_id')
    def _onchange_appointment_id(self):
        if self.appointment_id:
            self.patient_id = self.appointment_id.patient_id
            self.doctor_id = self.appointment_id.doctor_id


class DentalPrescriptionLine(models.Model):
    _name = 'dental.prescription.line'
    _description = 'Prescription Line'

    prescription_id = fields.Many2one('dental.prescription', string='Prescription', required=True, ondelete='cascade')
    medication = fields.Char(string='Medication', required=True)
    dosage = fields.Char(string='Dosage', help="e.g., 500mg, 1 tablet")
    frequency = fields.Char(string='Frequency', help="e.g., Every 8 hours, Twice a day")
    duration = fields.Char(string='Duration', help="e.g., 5 days, 1 week")
    instructions = fields.Char(string='Specific Instructions', help="e.g., Take after meals")
