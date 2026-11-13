from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    amount_total_words_fr = fields.Char(
        string="Amount in Words (French)",
        compute="_compute_amount_total_words_fr",
    )

    @api.depends("amount_total", "currency_id")
    def _compute_amount_total_words_fr(self):
        for order in self:
            order.amount_total_words_fr = (
                order.currency_id._amount_to_text_fr(order.amount_total) if order.currency_id else False
            )
