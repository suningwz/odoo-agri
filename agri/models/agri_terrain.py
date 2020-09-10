from odoo import api, fields, models


class Terrain(models.Model):
    _name = 'agri.terrain'
    _description = 'Terrain'
    _order = 'name asc'

    name = fields.Char('Name', required=True)
