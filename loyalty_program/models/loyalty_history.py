from odoo import fields, models, api


class LoyaltyHistory(models.Model):
    _name = 'loyalty.history'
    _description = 'Description'

    partner_id = fields.Many2one(
        string='Customer name',
        comodel_name='res.partner'
    )

    loyalty_points = fields.Float(
        string='Total points'
    )

    money_spent = fields.Float(
        string='Total amount'
    )

    loyalty_point = fields.Float(
        string='Accumulated points'
    )

    date_order = fields.Datetime(
        string='Order confirmation date'
    )

    name = fields.Char(
        string='Order number'
    )

    def _default_loyalty_program(self):
        loyalty_id = int(self.env['ir.config_parameter'].sudo().get_param('loyalty_for_sale_id', False))
        loyalty = self.env['loyalty.program'].browse(loyalty_id)
        return loyalty if loyalty_id and loyalty.exists() else None

    @api.model
    def create(self, vals):
        if bool(self.env['ir.config_parameter'].sudo().get_param('loyalty_email_notify', False)):
            self.btn_send_email()
        return super(LoyaltyHistory, self).create(vals)

    def btn_send_email(self):
        template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Happy More Point')], limit=1)
        if template_obj:
            # receipt_list = ['abc@gmail.com', 'xyz@yahoo.com']
            # email_cc = ['test@gmail.com']

            body = template_obj.body_html
            body = body.replace('--department--', str(self.partner_id.name))

            mail_values = {
                'subject': template_obj.subject,
                'body_html': body,
                'email_to': template_obj.email_to,
                # 'email_cc': ';'.join(map(lambda x: x, email_cc)),
                'email_from': template_obj.email_from,
            }
            create_and_send_email = self.env['mail.mail'].create(mail_values).send()

