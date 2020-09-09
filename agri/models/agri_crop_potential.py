from odoo import api, fields, models


class AgriCropPotential(models.Model):
    _name = 'agri.crop.potential'
    _description = 'Crop Potential'

    name = fields.Char('Name', required=True)
