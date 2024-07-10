from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "sequence, name"

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer('Offers', compute='_compute_offer_count')

    _sql_constraints = [
        ('check_type_name', 'unique(name)', 'The type name should be unique.')
    ]

    property_ids = fields.One2many('estate.property', 'property_type_id')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            