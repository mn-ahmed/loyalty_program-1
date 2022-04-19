from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    loyalty_email_notify = fields.Boolean(
        default=False,
        string='Email Notify',
        config_parameter = 'loyalty_email_notify'
    )

    loyalty_for_sale_id = fields.Many2one(
        comodel_name='loyalty.program',
        config_parameter='loyalty_for_sale_id',
    )
