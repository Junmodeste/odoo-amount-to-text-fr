{
    "name": "Amount to Text (French) - Purchase",
    "summary": "Print the total amount in French words on purchase orders",
    "version": "19.0.1.0.0",
    "category": "Inventory/Purchase",
    "license": "LGPL-3",
    "author": "Koffi Modeste Junior",
    "website": "https://github.com/Junmodeste/odoo-amount-to-text-fr",
    "depends": ["amount_to_text_fr", "purchase"],
    "data": [
        "report/report_purchaseorder.xml",
    ],
    "auto_install": True,
    "installable": True,
}
