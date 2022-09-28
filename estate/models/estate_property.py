from importlib.abc import ResourceReader
from calendar import month
from odoo import fields, models, api


class Estate_property(models.Model):
    _name = "estate.property"
    _description = 'Propiedades inmobiliarias'

    name = fields.Char(required=True)
    description = fields.Text(default = 'when duplicated, status and date are not copied')
    postcode = fields.Char()
    date_availability = fields.Date(copy=False , default=lambda self:fields.Date.add(fields.Date.today(),months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True , copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [('north','North'),('south','South'),('east','East'),('west','West')])
    active = fields.Boolean(default=True)
    state = fields.Selection([('new','New'),('offer_received','Offer Received'),
     ('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')])
    property_type_id = fields.Many2one('estate.property.type', required=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area","garden_area","garden")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange("garden","garden_area","garden_orientation")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False