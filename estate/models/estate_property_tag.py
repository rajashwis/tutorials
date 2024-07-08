from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('check_tag_name', 'unique(name)', 'The tag name should be unique.')
    ]