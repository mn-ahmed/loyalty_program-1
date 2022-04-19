from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_loyalty_program(self):
        loyalty_id = int(self.env['ir.config_parameter'].sudo().get_param('loyalty_for_sale_id', False))
        loyalty = self.env['loyalty.program'].browse(loyalty_id)
        return loyalty if loyalty_id and loyalty.exists() else None

    loyalty_program_id = fields.Many2one(
        comodel_name='loyalty.program',
        string='Loyalty program',
        default=_default_loyalty_program
    )

    point_accum = fields.Float(
        string='Points obtained',
        compute='count_point',
        store=True,
    )

    @api.depends('amount_total')
    def count_point(self):
        for rec in self:
            if rec.amount_total and rec.loyalty_program_id:
                bill = float(rec.amount_total)
                if rec.loyalty_program_id.type == 'fix':
                    rec.point_accum = rec.loyalty_program_id.points_fix
                else:
                    rec.point_accum = bill * rec.loyalty_program_id.points / 100

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        line = self.env['sale.order.line'].search([
                ('order_id', '=', self.id),
                ('product_id', '=',  self.env.ref('loyalty_program.loyalty_product').id),
            ])
        if line:
            if self.state == 'sale':
                vals = {
                    'partner_id': self.partner_id.id,
                    'loyalty_points': line.price_unit,
                    'money_spent': float(self.amount_total),
                    'date_order': self.date_order,
                    'name': self.name

                }
                self.env['loyalty.history'].create(vals)
                self.point_accum = 0
                self.partner_id.update({
                    'loyalty_point': self.partner_id.loyalty_point + line.price_unit
                })
        else:
            if self.state == 'sale':
                vals = {
                    'partner_id': self.partner_id.id,
                    'loyalty_points': self.point_accum,
                    'money_spent': float(self.amount_total),
                    'date_order': self.date_order,
                    'name': self.name

                }
                self.env['loyalty.history'].create(vals)
                self.partner_id.update({
                    'loyalty_point': self.partner_id.loyalty_point + self.point_accum
                })
        return result

    def recompute_Loyalty_lines(self):
        return {
            'name': 'Use loyalty point',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard.loyalty.point',
            'target': 'new',
            'context': {'default_partner_id': self.partner_id.id,
                        'default_order_id': self.id,
                        'default_partner_name': self.partner_id.name,
                        'default_loyalty_point': self.partner_id.loyalty_point,
                        'default_loyalty_level': self.partner_id.loyalty_level.name,
                        }
        }