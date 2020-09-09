from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AgriLand(models.Model):
    _name = 'agri.land'
    _description = 'Land'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name, create_date desc'

    name = fields.Char('Name', required=True)
    short_name = fields.Char('Short Name', required=True)
    code = fields.Char('Code', required=True)
    country_id = fields.Many2one('res.country', string='Country')
    area_ha = fields.Float('Hectares', digits='Hectare', tracking=True)
    boundary = fields.GeoPolygon('Boundary', srid=4326, gist_index=True)
    has_boundary = fields.Boolean('Has Boundary',
                                  computed='_compute_has_boundary',
                                  default=False)
    farm_id = fields.Many2one('agri.farm',
                              'Farm',
                              ondelete='cascade',
                              required=True)
    land_cover_ids = fields.One2many(comodel_name='agri.land.cover',
                                     inverse_name='land_id',
                                     string='Land Cover',
                                     copy=True)

    @api.onchange('boundary')
    def _compute_has_boundary(self):
        for land in self:
            land.has_boundary = True if land.boundary else False

    @api.constrains('code')
    def constrains_code(self):
        domain = [('farm_id', '=', self.farm_id.id),
                  ('code', 'ilike', self.code)]
        if self.id:
            domain.append(('id', '!=', self.id))
        land = self.env['agri.land'].search(domain, limit=1)
        if land:
            raise ValidationError(_('Duplicate Land'))

    def name_get(self):
        return [(land.id, "{} ({:.3f} ha)".format(land.name, land.area_ha))
                for land in self]
