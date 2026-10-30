from num2words import num2words

from odoo import models

# Francs CFA (UEMOA / CEMAC) : libellé imposé, jamais de centimes.
CFA_CURRENCIES = ("XOF", "XAF")


def _upper_first(text):
    return text[:1].upper() + text[1:]


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def _amount_to_text_fr(self, amount):
        """Return ``amount`` written in French words.

        The native ``amount_to_text`` follows the user language and its
        "... and ..." sentence is not translated in French in Odoo 19,
        so num2words is called directly with ``lang="fr"``.
        """
        self.ensure_one()
        integral, _sep, fractional = f"{abs(amount):.{self.decimal_places}f}".partition(".")
        integral, fractional = int(integral), int(fractional or 0)

        if self.name in CFA_CURRENCIES:
            return _upper_first(self._fr_words(integral, "franc CFA", "francs CFA"))

        # Labels are translatable: read them in an active French language if any (fr_FR, fr_CI...).
        fr_lang = next((code for code, _name in self.env["res.lang"].get_installed() if code.startswith("fr")), None)
        currency = self.with_context(lang=fr_lang) if fr_lang else self
        unit = (currency.currency_unit_label or self.name).lower()
        text = self._fr_words(integral, unit, unit)
        if fractional:
            subunit = (currency.currency_subunit_label or "").lower()
            text += " et " + self._fr_words(fractional, subunit, subunit)
        return _upper_first(text)

    @staticmethod
    def _fr_words(number, singular, plural):
        """Number in words followed by its unit, with French agreement rules."""
        if number < 2:
            # shortcut: Odoo labels are plural ("Euros"), drop the final "s"; edit the label if a currency differs.
            unit = singular[:-1] if singular == plural and singular.endswith("s") else singular
        else:
            unit = plural
        # "un million de francs", "deux milliards d'euros"
        link = ""
        if number and number % 1_000_000 == 0:
            link = "d'" if unit[:1] in "aeiouyéh" else "de "
        return f"{num2words(number, lang='fr')} {link}{unit}".strip()
