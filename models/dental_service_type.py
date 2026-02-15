from odoo import models, fields

class DentalServiceType(models.Model):
    _name = 'dental.service.type'
    _description = 'Dental Service Type'
    
    name = fields.Char(string='Type Name', required=True)
