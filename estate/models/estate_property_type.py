from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('check_type_name', 'unique(name)', 'The type name should be unique.')
    ]