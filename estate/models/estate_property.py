from odoo import fields, models, api

class EstateProperty(models.Model):

    _name = 'estate.property'
    _description = 'Real Estate Property Model'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True,)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [('north','North'),('south', 'South'), ('east', 'East'), ('west','West')])
    active = fields.Boolean(default=True)
    state = fields.Selection([('new', 'New'), ('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),('canceled', 'Canceled')],required=True, copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type')
    tag_ids = fields.Many2many('estate.property.tag')
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    offer_ids = fields.One2many('estate.property.offer','property_id')
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')
    

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.living_area + record.garden_area
            
            
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
                record.best_price = max(record.offer_ids.mapped('price') or [0])

    @api.onchange('garden')
    def _onchange_garden(self):
            if self.garden:
                self.garden_area = 10
                self.garden_orientation = 'north'
            else:
                self.garden_area = False
                self.garden_orientation = False
                 