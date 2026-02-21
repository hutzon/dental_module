from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DentalAppointment(models.Model):
    _name = 'dental.appointment'
    _description = 'Dental Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Appointment ID', readonly=True, default=lambda self: _('New'))
    
    patient_id = fields.Many2one(
        'res.partner', string='Patient', required=True, tracking=True,
        domain=[('is_patient', '=', True)]
    )
    doctor_id = fields.Many2one(
        'res.partner', string='Doctor', required=True, tracking=True,
        domain=[('is_doctor', '=', True)]
    )
    
    date_start = fields.Datetime(string='Date', required=True, tracking=True)
    date_end = fields.Datetime(string='End Date', compute='_compute_date_end', store=True, readonly=False)
    duration = fields.Float(string='Duration (Hours)', default=0.5)
    
    note = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], string='Status', default='draft', tracking=True)
    
    # For color coding in calendar and kanban views
    color = fields.Integer(string='Color', compute='_compute_color', store=True)

    @api.depends('state')
    def _compute_color(self):
        for record in self:
            if record.state in ['draft', 'confirmed']:
                record.color = 4 # Blue
            elif record.state == 'done':
                record.color = 10 # Green
            elif record.state == 'canceled':
                record.color = 1 # Red
            else:
                record.color = 0
    
    service_ids = fields.Many2many('dental.service', string='Services')

    prescription_count = fields.Integer(compute='_compute_prescription_count', string="Prescription Count")

    def _compute_prescription_count(self):
        for app in self:
            app.prescription_count = self.env['dental.prescription'].search_count([('appointment_id', '=', app.id)])

    def action_view_prescriptions(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("dental_management.action_dental_prescription")
        action['domain'] = [('appointment_id', '=', self.id)]
        action['context'] = {
            'default_appointment_id': self.id,
            'default_patient_id': self.patient_id.id,
            'default_doctor_id': self.doctor_id.id,
        }
        return action

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('dental.appointment') or _('New')
        return super(DentalAppointment, self).create(vals)

    @api.depends('date_start', 'duration')
    def _compute_date_end(self):
        for record in self:
            if record.date_start and record.duration:
                record.date_end = fields.Datetime.add(record.date_start, minutes=int(record.duration * 60))
            else:
                record.date_end = record.date_start
                
    @api.onchange('service_ids')
    def _onchange_service_ids(self):
        if self.service_ids:
            total_duration = sum(service.duration_minutes for service in self.service_ids)
            if total_duration > 0:
                self.duration = total_duration / 60.0

    @api.constrains('doctor_id', 'date_start', 'date_end')
    def _check_double_booking(self):
        for appointment in self:
            domain = [
                ('doctor_id', '=', appointment.doctor_id.id),
                ('date_start', '<', appointment.date_end),
                ('date_end', '>', appointment.date_start),
                ('id', '!=', appointment.id),
                ('state', '!=', 'canceled')
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(_("The doctor is already booked for this time slot!"))

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_done(self):
        history_model = self.env['dental.patient.history']
        for record in self:
            record.state = 'done'
            # Auto-create history
            if record.patient_id:
                history_vals = {
                    'patient_id': record.patient_id.id,
                    'doctor_id': record.doctor_id.id,
                    'appointment_id': record.id,
                    'date': record.date_start.date(),
                    'service_ids': [(6, 0, record.service_ids.ids)],
                    'description': f"Appointment Completed. {record.note or ''}",
                }
                history_model.create(history_vals)

    def action_cancel(self):
        for record in self:
            record.state = 'canceled'
