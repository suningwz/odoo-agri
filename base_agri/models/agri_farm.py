from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AgriFarm(models.Model):
    _name = 'agri.farm'
    _description = 'Farms'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name, create_date desc'

    active = fields.Boolean('Active', default=True, tracking=True)
    name = fields.Char('Name', required=True)
    area_ha = fields.Float('Hectares')
    boundary = fields.GeoPolygon('Boundary', srid=4326, gist_index=True)
    farmland_id = fields.Many2one('agri.farmland',
                                  'Farmland',
                                  ondelete='cascade',
                                  required=True)
    field_ids = fields.One2many(comodel_name='agri.field',
                                inverse_name='farm_id',
                                string='Fields',
                                copy=True)
    land_ids = fields.One2many(comodel_name='agri.land',
                               inverse_name='farm_id',
                               string='Land',
                               copy=True)

    @api.constrains('name')
    def constrains_name(self):
        domain = [('farmland_id', '=', self.farmland_id.id),
                  ('active', '=', True), ('name', 'ilike', self.name)]
        if self.id:
            domain.append(('id', '!=', self.id))
        farm = self.env['agri.farm'].search(domain, limit=1)
        if farm:
            raise ValidationError('Duplicate Farm name')
