from odoo import models, fields, api
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Properties'

    name = fields.Char(required =True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active =fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'),('east', 'East'),('west', 'West')])
    state = fields.Selection(
        [('new', 'New'), ('sold', 'Sold'),('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted')],
         required=True,copy=False,default='new')
    property_type_id = fields.Many2one('estate.property.type')
    salesman = fields.Many2one('res.users')
    buyer = fields.Many2one('res.partner',copy=False)
    tags_ids = fields.Many2many('estate.property.tag')
    offer_ids= fields.One2many('estate.property.offer','property_id')
    total_area=fields.Float(compute ='_compute_total_area')
    best_price = fields.Float(compute = '_compute_best_price')



    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.garden_area + rec.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offer_ids.mapped('price') or [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation='north'
            self.garden_area= 10
        else:
            self.garden_orientation=''
            self.garden_area= 0