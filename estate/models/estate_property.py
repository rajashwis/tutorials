from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy = False, default = fields.Date.today() + relativedelta(months=+3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly = True, copy = False)
    bedrooms = fields.Integer('Bedrooms', default = 2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation of the Garden")
    state = fields.Selection(
        string = 'State',
        selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default = 'new',
        required = True,
        copy = False
    )
    active = fields.Boolean(default = True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', copy = False, default=lambda self: self.env.uid)

    tag_ids = fields.Many2many('estate.property.tag', string='Taxes')

    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Integer('Total Area (sqm)', compute = '_compute_total_area')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    best_offer = fields.Float(compute = '_compute_best_price')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for line in self:
            if line.offer_ids:
                line.best_offer = max(line.offer_ids.mapped('price'))
            else:
                line.best_offer = 0