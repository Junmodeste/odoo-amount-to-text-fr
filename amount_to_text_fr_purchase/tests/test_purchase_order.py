from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAmountToTextFrPurchase(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.xof = cls.setup_other_currency("XOF")

    def test_purchase_order_report(self):
        order = self.env["purchase.order"].create({
            "partner_id": self.partner_a.id,
            "currency_id": self.xof.id,
            "order_line": [(0, 0, {
                "product_id": self.product_a.id,
                "product_qty": 2,
                "price_unit": 1000000,
                "tax_ids": False,
            })],
        })
        self.assertEqual(order.amount_total_words_fr, "Deux millions de francs CFA")
        html, _type = self.env["ir.actions.report"]._render_qweb_html(
            "purchase.action_report_purchase_order", order.ids
        )
        self.assertIn("Deux millions de francs CFA", html.decode())
