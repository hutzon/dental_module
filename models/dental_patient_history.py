from odoo import models, fields, api

class DentalPatientHistory(models.Model):
    _name = 'dental.patient.history'
    _description = 'Dental Patient History'
    _order = 'date desc'

    patient_id = fields.Many2one('res.partner', string='Patient', required=True, domain=[('is_patient', '=', True)])
    doctor_id = fields.Many2one('res.partner', string='Doctor', domain=[('is_doctor', '=', True)])
    appointment_id = fields.Many2one('dental.appointment', string='Related Appointment')
    
    date = fields.Date(string='Date', default=fields.Date.context_today)
    description = fields.Char(string='Description', required=True)
    treatment_notes = fields.Html(string='Treatment Notes')
    service_ids = fields.Many2many('dental.service', string='Services Performed')
