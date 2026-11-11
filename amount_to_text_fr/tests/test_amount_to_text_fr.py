from odoo.tests import tagged

from odoo.addons.sale.tests.common import TestSaleCommon


@tagged("post_install", "-at_install")
class TestAmountToTextFr(TestSaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.xof = cls.setup_other_currency("XOF")
        cls.eur = cls.setup_other_currency("EUR")
        # sale.order takes its currency from the pricelist.
        cls.pricelist_xof = cls.env["product.pricelist"].create({"name": "XOF", "currency_id": cls.xof.id})

    def test_xof_thousand(self):
        self.assertEqual(self.xof._amount_to_text_fr(1000), "Mille francs CFA")

    def test_xof_million(self):
        self.assertEqual(
            self.xof._amount_to_text_fr(1250000),
            "Un million deux cent cinquante mille francs CFA",
        )
        self.assertEqual(self.xof._amount_to_text_fr(2000000), "Deux millions de francs CFA")

    def test_xof_no_cents(self):
        # XOF has rounding 1: the decimals are rounded away, never written.
        self.assertEqual(self.xof._amount_to_text_fr(1000.4), "Mille francs CFA")

    def test_zero(self):
        self.assertEqual(self.xof._amount_to_text_fr(0), "Zéro franc CFA")

    def test_eur_with_cents(self):
        self.assertEqual(
            self.eur._amount_to_text_fr(1234.56),
            "Mille deux cent trente-quatre euros et cinquante-six cents",
        )
        self.assertEqual(self.eur._amount_to_text_fr(1.01), "Un euro et un cent")

    def test_invoice_report(self):
        invoice = self._create_invoice_one_line(price_unit=1000, currency_id=self.xof.id, post=True)
        self.assertEqual(invoice.amount_total_words_fr, "Mille francs CFA")
        html, _type = self.env["ir.actions.report"]._render_qweb_html("account.account_invoices", invoice.ids)
        self.assertIn("Mille francs CFA", html.decode())

    def test_sale_order_report(self):
        order = self.env["sale.order"].create({
            "partner_id": self.partner_a.id,
            "pricelist_id": self.pricelist_xof.id,
            "order_line": [(0, 0, {
                "product_id": self.company_data["product_order_no"].id,
                "product_uom_qty": 1,
                "price_unit": 1250000,
                "tax_ids": False,
            })],
        })
        self.assertEqual(order.amount_total_words_fr, "Un million deux cent cinquante mille francs CFA")
        html, _type = self.env["ir.actions.report"]._render_qweb_html("sale.action_report_saleorder", order.ids)
        self.assertIn("Un million deux cent cinquante mille francs CFA", html.decode())

    def test_payment_receipt_report(self):
        payment = self.init_payment(25000, post=True, currency=self.xof)
        self.assertEqual(payment.amount_words_fr, "Vingt-cinq mille francs CFA")
        html, _type = self.env["ir.actions.report"]._render_qweb_html(
            "account.action_report_payment_receipt", payment.ids
        )
        self.assertIn("Vingt-cinq mille francs CFA", html.decode())
