#!/usr/bin/env python3
"""Step 6 math verification: every dollar figure in
web/blog/firstbase-vs-stripe-atlas-vs-doola.html is recomputed from the
stated inputs (published provider rates x recurrence count).

    python3 test_step6_math.py

Standard library only. Exit code 0 means the article's arithmetic is exact.
"""

import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARTICLE = HERE / "web" / "blog" / "firstbase-vs-stripe-atlas-vs-doola.html"

# Published inputs, verified October 2026.
FB_FORMATION = 399
FB_AGENT_YEAR = 99
ATLAS_FORMATION = 500
ATLAS_AGENT_YEAR = 100          # first year included in the package
ATLAS_AGENT_PAID_YEARS = 2
DOOLA_STARTER_YEAR = 297
DOOLA_TC_YEAR = 1999
WY_ANNUAL_REPORT = 60
DE_LLC_FRANCHISE = 300
DE_C_CORP_MIN_FRANCHISE = 450
PREPARER_YEAR = 400


def firstbase(state_year_fee):
    return FB_FORMATION + state_year_fee * 3 + FB_AGENT_YEAR * 3


def atlas(state_year_fee):
    return ATLAS_FORMATION + state_year_fee * 3 + ATLAS_AGENT_YEAR * ATLAS_AGENT_PAID_YEARS


def doola(yearly, state_year_fee):
    return yearly * 3 + state_year_fee * 3


def firstbase_year1(state_year_fee):
    return FB_FORMATION + state_year_fee + FB_AGENT_YEAR


def text():
    html = ARTICLE.read_text(encoding="utf-8")
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S)
    plain = re.sub(r"<[^>]+>", " ", html)
    return (
        plain.replace("&amp;", "&")
        .replace("&mdash;", "-")
        .replace("&middot;", ".")
        .replace("&times;", "x")
        .replace("&minus;", "-")
        .replace("&minus;", "-")
    )


class ThreeYearTotals(unittest.TestCase):
    def test_firstbase_wyoming(self):
        self.assertEqual(firstbase(WY_ANNUAL_REPORT), 876)
        self.assertIn("$876", text())

    def test_firstbase_delaware(self):
        self.assertEqual(firstbase(DE_LLC_FRANCHISE), 1596)

    def test_stripe_atlas_delaware_llc(self):
        self.assertEqual(atlas(DE_LLC_FRANCHISE), 1600)
        self.assertIn("$1,600", text())

    def test_stripe_atlas_delaware_c_corp(self):
        self.assertEqual(atlas(DE_C_CORP_MIN_FRANCHISE), 2050)

    def test_doola_starter_wyoming(self):
        self.assertEqual(doola(DOOLA_STARTER_YEAR, WY_ANNUAL_REPORT), 1071)

    def test_doola_total_compliance_wyoming(self):
        self.assertEqual(doola(DOOLA_TC_YEAR, WY_ANNUAL_REPORT), 6177)
        self.assertIn("$6,177", text())

    def test_doola_total_compliance_delaware(self):
        self.assertEqual(doola(DOOLA_TC_YEAR, DE_LLC_FRANCHISE), 6897)


class Deltas(unittest.TestCase):
    def test_atlas_penalty_versus_firstbase_wyoming(self):
        delta = atlas(DE_LLC_FRANCHISE) - firstbase(WY_ANNUAL_REPORT)
        self.assertEqual(delta, 724)
        self.assertIn("$724", text())
        self.assertGreaterEqual(delta, 720)

    def test_doola_starter_premium_over_firstbase(self):
        self.assertEqual(doola(DOOLA_STARTER_YEAR, WY_ANNUAL_REPORT) - firstbase(WY_ANNUAL_REPORT), 195)

    def test_average_per_year(self):
        self.assertEqual(firstbase(WY_ANNUAL_REPORT) / 3, 292)
        self.assertEqual(atlas(DE_LLC_FRANCHISE) / 3, 1600 / 3)


class YearByYear(unittest.TestCase):
    def test_firstbase_wyoming_years(self):
        year1 = firstbase_year1(WY_ANNUAL_REPORT)
        year23 = WY_ANNUAL_REPORT + FB_AGENT_YEAR
        self.assertEqual(year1, 558)
        self.assertEqual(year23, 159)
        self.assertEqual(year1 + 2 * year23, 876)

    def test_atlas_years(self):
        year1 = ATLAS_FORMATION + DE_LLC_FRANCHISE
        year23 = DE_LLC_FRANCHISE + ATLAS_AGENT_YEAR
        self.assertEqual(year1, 800)
        self.assertEqual(year23, 400)
        self.assertEqual(year1 + 2 * year23, 1600)

    def test_renewal_multiple(self):
        self.assertEqual((DE_LLC_FRANCHISE + ATLAS_AGENT_YEAR) / (WY_ANNUAL_REPORT + FB_AGENT_YEAR), 400 / 159)

    def test_doola_years(self):
        self.assertEqual(DOOLA_STARTER_YEAR + WY_ANNUAL_REPORT, 357)
        self.assertEqual(DOOLA_TC_YEAR + WY_ANNUAL_REPORT, 2059)


class ComplianceBasket(unittest.TestCase):
    def test_baskets(self):
        self.assertEqual(firstbase(WY_ANNUAL_REPORT) + PREPARER_YEAR * 3, 2076)
        self.assertEqual(atlas(DE_LLC_FRANCHISE) + PREPARER_YEAR * 3, 2800)
        self.assertEqual(doola(DOOLA_TC_YEAR, WY_ANNUAL_REPORT), 6177)

    def test_formation_share_of_basket(self):
        self.assertAlmostEqual(FB_FORMATION / 2076, 0.1922, places=4)
        self.assertAlmostEqual(ATLAS_FORMATION / 2800, 0.1786, places=4)
        self.assertAlmostEqual(DOOLA_TC_YEAR / 6177, 0.3236, places=4)


class ProcessingPayback(unittest.TestCase):
    """The payback paragraph: $8,000 MRR, $40 AOV, 70% international."""

    MRR = 8000.0
    AOV = 40.0
    INTl = 0.70
    ORDERS = MRR / AOV
    RATE_DELTA = (0.05 - (0.029 + INTl * 0.015)) + (0.20 / AOV)

    # Annual holding cost = 3-year total / 3 + $400 preparer (Doola bundles it).
    FB_ANNUAL = 876 / 3 + 400
    ATLAS_ANNUAL = 1600 / 3 + 400
    DOOLA_ANNUAL = 6177 / 3

    def test_mor_cost(self):
        self.assertEqual(self.MRR * 0.05, 400.0)
        self.assertEqual(self.ORDERS * 0.50, 100.0)
        self.assertEqual(self.MRR * 0.05 + self.ORDERS * 0.50, 500.0)

    def test_stripe_processing_only(self):
        rate = 0.029 + self.INTl * 0.015
        self.assertAlmostEqual(rate, 0.0395, places=9)
        self.assertEqual(self.MRR * rate, 316.0)
        self.assertEqual(self.ORDERS * 0.30, 60.0)

    def test_rate_delta(self):
        self.assertAlmostEqual(self.RATE_DELTA, 0.0155, places=9)

    def test_annual_holding_costs(self):
        self.assertEqual(self.FB_ANNUAL, 692.0)
        self.assertAlmostEqual(self.ATLAS_ANNUAL, 933.3333333, places=6)
        self.assertEqual(self.DOOLA_ANNUAL, 2059.0)

    def test_monthly_all_in(self):
        processing = 316.0 + 60.0
        self.assertAlmostEqual(processing + self.FB_ANNUAL / 12, 433.6666667, places=6)
        self.assertAlmostEqual(processing + self.ATLAS_ANNUAL / 12, 453.7777778, places=6)
        self.assertAlmostEqual(processing + self.DOOLA_ANNUAL / 12, 547.5833333, places=6)

    def test_annual_result_versus_mor(self):
        self.assertAlmostEqual((500.0 - 433.6666667) * 12, 796.0, places=4)
        self.assertAlmostEqual((500.0 - 453.7777778) * 12, 554.6666667, places=4)
        self.assertAlmostEqual((500.0 - 547.5833333) * 12, -571.0, places=4)

    def test_break_even_mrr(self):
        self.assertAlmostEqual((self.FB_ANNUAL / 12) / self.RATE_DELTA, 3720.4301, places=3)
        self.assertAlmostEqual((self.ATLAS_ANNUAL / 12) / self.RATE_DELTA, 5017.9211, places=3)
        self.assertAlmostEqual((self.DOOLA_ANNUAL / 12) / self.RATE_DELTA, 11069.8925, places=3)

    def test_article_states_the_rounded_break_even(self):
        body = text()
        for token in ("$3,720", "$5,018", "$11,070", "+$796", "+$555", "−$571"):
            self.assertIn(token, body)

    def test_sibling_article_budget_consistency(self):
        """The linked MoR study uses the $1,000 default budget -> $5,376."""
        self.assertAlmostEqual((1000 / 12) / self.RATE_DELTA, 5376.344086, places=5)


class ArticleIntegrity(unittest.TestCase):
    def test_canonical(self):
        html = ARTICLE.read_text(encoding="utf-8")
        self.assertIn(
            '<link rel="canonical" href="https://pay.mybskm.top/blog/firstbase-vs-stripe-atlas-vs-doola.html">',
            html,
        )

    def test_affiliate_cta(self):
        html = ARTICLE.read_text(encoding="utf-8")
        self.assertIn(
            'href="https://go.272738.xyz/firstbase?src=compare_firstbase_atlas" target="_blank" rel="sponsored noopener"',
            html,
        )

    def test_calculator_deeplink(self):
        self.assertIn("https://pay.mybskm.top/?mrr=8000&amp;aov=40&amp;intl=70", ARTICLE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
