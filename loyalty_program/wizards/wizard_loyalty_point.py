from odoo import fields, models
from odoo.exceptions import ValidationError


class WizardConfirmation(models.TransientModel):
    _name = 'wizard.loyalty.point'
    _description = 'Wizard loyalty point'

    order_id = fields.Many2one("sale.order", string="Order")
    partner_id = fields.Many2one("res.partner", string="Partner")
    partner_name = fields.Char('Customer', readonly=True)
    loyalty_point = fields.Float('Accumulated points', readonly=True)
    loyalty_level = fields.Char('Customer level',  readonly=True)
    points_to_use = fields.Float('Points to use')

    def use_loyalty_points(self):
        if self.loyalty_point < self.points_to_use:
            raise ValidationError("You don't have enough of points")

        if self.loyalty_point > float(self.order_id.amount_total):
            raise ValidationError("Point to use must be less than %s" % self.order_id.amount_total)

        line = self.env['sale.order.line'].search([
                ('order_id', '=', self.order_id.id),
                ('product_id', '=',  self.env.ref('loyalty_program.loyalty_product').id),
            ])
        if line:
            line.update({
                'price_unit': - self.points_to_use,
            })
        else:
            self.env['sale.order.line'].create({
                'order_id': self.order_id.id,
                'product_id': self.env.ref('loyalty_program.loyalty_product').id,
                'product_uom_qty': 1.0,
                'price_unit': - self.points_to_use,
            })

    def use_all_points(self):
        if self.loyalty_point < float(self.order_id.amount_total):
            self.points_to_use = self.loyalty_point
        else:
            self.points_to_use = self.order_id.amount_total

        self.use_loyalty_points()
