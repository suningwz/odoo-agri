from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AgriField(models.Model):
    _name = 'agri.field'
    _description = 'Fields'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name, create_date desc'

    active = fields.Boolean('Active', default=True, tracking=True)
    area_ha = fields.Float('Hectares', tracking=True)
    boundary = fields.GeoPolygon('Boundary', srid=4326, gist_index=True)
    farm_id = fields.Many2one('agri.farm',
                              'Farm',
                              ondelete='cascade',
                              required=True)
    name = fields.Char('Name', required=True, tracking=True)
    established_date = fields.Date('Established Date', tracking=True)

    cropping_potential_id = fields.Many2one('agri.croppingpotential',
                                            'Cropping Potential',
                                            tracking=True)
    effective_depth_id = fields.Many2one('agri.effectivedepth',
                                         'Effective Depth',
                                         tracking=True)
    irrigated = fields.Boolean('Irrigated', default=False, tracking=True)
    irrigation_type_id = fields.Many2one('agri.irrigationtype',
                                         'Irrigation Type',
                                         tracking=True)
    land_class_id = fields.Many2one('agri.landclass',
                                    'Land Class',
                                    required=True,
                                    tracking=True)
    soil_texture_id = fields.Many2one('agri.soiltexture',
                                      'Soil Texture',
                                      tracking=True)
    water_source_id = fields.Many2one('agri.watersource',
                                      'Water Source',
                                      tracking=True)

    @api.constrains('name')
    def constrains_name(self):
        domain = [('farm_id', '=', self.farm_id.id), ('active', '=', True),
                  ('name', 'ilike', self.name)]
        if self.id:
            domain.append(('id', '!=', self.id))
        field = self.env['agri.field'].search(domain, limit=1)
        if field:
            raise ValidationError('Duplicate Field name')

    @api.onchange('irrigation_type_id')
    def onchange_irrigation_type(self):
        self.irrigated = True if self.irrigation_type_id else False
