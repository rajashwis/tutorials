from odoo import api, models, fields
from odoo.exceptions import UserError
from datetime import timedelta, datetime

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string = 'Status',
        selection = [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy = False
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_date_deadline', inverse = '_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for line in self:
            if line.create_date:
                line.date_deadline = line.create_date + timedelta(days=line.validity)
            else:
                line.date_deadline = datetime.now() + timedelta(days=line.validity)

    def _inverse_date_deadline(self):
        for line in self:
            if line.create_date:
                line.validity = (line.date_deadline - line.create_date.date()).days
            else:
                line.validity = (line.date_deadline - fields.Date.today()).days

    #ACCEPT BUTTON
    def action_accept(self):
        for record in self:
            if record.status != 'accepted':
                if record.property_id.selling_price == 0:
                    record.status = 'accepted'
                    record.property_id.selling_price = record.price
                    record.property_id.buyer_id = record.partner_id
                else:
                    raise UserError("Another Offer already accepted.")
        return True

    #REFUSE BUTTON
    def action_refuse(self):
        for record in self:
            if record.status != 'refused':
                if record.property_id.selling_price > 0:
                    record.status = 'refused'
                    record.property_id.selling_price = 0
                    record.property_id.buyer_id = ''