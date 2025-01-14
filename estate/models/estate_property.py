from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties"
    _order = "id desc"

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

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Integer('Total Area (sqm)', compute = '_compute_total_area')

    best_offer = fields.Float(compute = '_compute_best_price')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price should be greater than 0.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price should be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for line in self:
            if line.offer_ids:
                if(line.state != 'offer_received'):
                    line.state="offer_received"
                line.best_offer = max(line.offer_ids.mapped('price'))
            else:
                line.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
    
    #SOLD BUTTON
    def action_sold_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Cancelled Products cannot be sold.")
            else:
                record.state = 'sold'
        return True
    
    #CANCEL BUTTON
    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold products cannot be cancelled.")
            else:
                record.state = 'canceled'
        return True

    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            check_selling_price = (90/100) * record.expected_price
            if float_is_zero(record.selling_price, 4):
                return True
            if float_compare(record.selling_price, check_selling_price, 4) < 0:
                raise ValidationError(f'Selling price cannot be lower than 90% of the expected price!!')