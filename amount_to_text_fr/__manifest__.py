{
    "name": "Amount to Text (French)",
    "summary": "Print the total amount in French words on invoices and quotations",
    "version": "17.0.1.0.0",
    "category": "Accounting/Localizations",
    "license": "LGPL-3",
    "author": "Koffi Modeste Junior",
    "website": "https://github.com/Junmodeste/odoo-amount-to-text-fr",
    "depends": ["account", "sale"],
    "external_dependencies": {"python": ["num2words"]},
    "data": [
        "report/report_invoice.xml",
        "report/report_saleorder.xml",
    ],
    "installable": True,
}
