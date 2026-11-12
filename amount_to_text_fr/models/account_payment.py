from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    amount_words_fr = fields.Char(
        string="Amount in Words (French)",
        compute="_compute_amount_words_fr",
    )

    @api.depends("amount", "currency_id")
    def _compute_amount_words_fr(self):
        for payment in self:
            payment.amount_words_fr = (
                payment.currency_id._amount_to_text_fr(payment.amount) if payment.currency_id else False
            )
