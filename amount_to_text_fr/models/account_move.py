from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_total_words_fr = fields.Char(
        string="Amount in Words (French)",
        compute="_compute_amount_total_words_fr",
    )

    @api.depends("amount_total", "currency_id")
    def _compute_amount_total_words_fr(self):
        for move in self:
            move.amount_total_words_fr = (
                move.currency_id._amount_to_text_fr(move.amount_total) if move.currency_id else False
            )
