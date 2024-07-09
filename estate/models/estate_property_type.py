from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "sequence, name"

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")

    _sql_constraints = [
        ('check_type_name', 'unique(name)', 'The type name should be unique.')
    ]

    property_ids = fields.One2many('estate.property', 'property_type_id')