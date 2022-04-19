from odoo import fields, models, api


class LoyaltyProgram(models.Model):
    _name = 'loyalty.program'
    _description = 'Loyalty program'

    type = fields.Selection(
        [('fix', 'Fix'),
         ('var', 'Variant')],
        default='fix', string="Type")

    name = fields.Char(
        string='Name of the loyalty',
        required=True
    )

    points_fix = fields.Float(
        string='Points per order',
        required=True
    )

    points = fields.Float(
        string='% of points per order',
        required=True
    )

    active = fields.Boolean(
        string='Active',
        required=True,
        default=True
    )
