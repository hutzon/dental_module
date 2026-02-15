from odoo import models, fields

class DentalService(models.Model):
    _name = 'dental.service'
    _description = 'Dental Service'
    
    name = fields.Char(string='Service Name', required=True)
    service_type_id = fields.Many2one('dental.service.type', string='Service Type')
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    price = fields.Float(string='Price', required=True, default=0.0)
    duration_minutes = fields.Integer(string='Default Duration (Minutes)', default=30)
