from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_point = fields.Float(
        string='Accumulated points',
        default=0
    )

    loyalty_level = fields.Many2one(
        comodel_name='loyalty.program.partner.level',
        string='Customer level',
        compute='loyalty_level_compute'
    )

    @api.depends('loyalty_point')
    def loyalty_level_compute(self):
        for rec in self:
            levels = self.env['loyalty.program.partner.level'].sudo().search([])
            x = 0
            for level in levels:
                if (level.loyalty_points >= x) and (rec.loyalty_point >= level.loyalty_points):
                    rec.loyalty_level = level

                    x = level.loyalty_points
