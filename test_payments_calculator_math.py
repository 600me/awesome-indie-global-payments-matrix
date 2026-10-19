#!/usr/bin/env python3
"""Independent verification for the pay.mybskm.top payments calculator.

The test executes the exact ``calculate`` function shipped in ``web/index.html``
inside Node.js, compares it with an independent Python implementation, and then
checks the published-page contract (markup, canonical URLs, JSON-LD, sitemap and
the research article numbers).

Run: python3 test_payments_calculator_math.py
Exit code 0 means every assertion passed.
"""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "web" / "index.html"
BLOG_INDEX = ROOT / "web" / "blog" / "index.html"
ARTICLE = ROOT / "web" / "blog" / "mor-vs-us-llc-breakeven.html"
SITEMAP = ROOT / "web" / "sitemap.xml"

CANONICAL_HOME = "https://pay.mybskm.top/"
CANONICAL_BLOG = "https://pay.mybskm.top/blog/"
CANONICAL_ARTICLE = "https://pay.mybskm.top/blog/mor-vs-us-llc-breakeven.html"

PASSED = 0


def expect(condition: bool, message: str) -> None:
    global PASSED
    if not condition:
        raise AssertionError(message)
    PASSED += 1


def close(actual: float, expected: float, label: str, tolerance: float = 1e-9) -> None:
    expect(
        math.isclose(actual, expected, rel_tol=tolerance, abs_tol=1e-9),
        f"{label}: expected {expected!r}, got {actual!r}",
    )


def read(path: Path) -> str:
    expect(path.is_file(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def reference(mrr: float, aov: float, annual: float, intl: float, fx: bool) -> dict:
    """Literal transcription of the directive's formulas, independent of the page JS."""
    orders = mrr / aov
    mor_percent = mrr * 0.05
    mor_fixed = orders * 0.50
    mor = mor_percent + mor_fixed
    stripe_rate = 0.029 + (intl / 100) * 0.015 + (0.01 if fx else 0)
    stripe_percent = mrr * stripe_rate
    stripe_fixed = orders * 0.30
    compliance = annual / 12
    stripe = stripe_percent + stripe_fixed + compliance
    delta = mor - stripe
    rate_delta = (0.05 - stripe_rate) + (0.20 / aov)
    breakeven = compliance / rate_delta if rate_delta > 0 else math.inf
    return {
        "orders": orders,
        "morPercent": mor_percent,
        "morFixed": mor_fixed,
        "mor": mor,
        "stripeRate": stripe_rate,
        "stripePercent": stripe_percent,
        "stripeFixed": stripe_fixed,
        "compliance": compliance,
        "stripe": stripe,
        "delta": delta,
        "rateDelta": rate_delta,
        "breakeven": breakeven,
    }


def extract_function(script: str, name: str) -> str:
    start = script.index(f"function {name}(")
    brace = script.index("{", start)
    depth = 0
    for offset in range(brace, len(script)):
        char = script[offset]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return script[start : offset + 1]
    raise AssertionError(f"could not extract function {name}")


def run_page_calculator(cases: list[list[float]]) -> list[dict]:
    node = shutil.which("node")
    expect(node is not None, "Node.js is required to execute the page calculator")
    html = read(INDEX)
    script = re.search(r"<script>\n(.*?)\n</script>", html, re.S)
    expect(script is not None, "calculator script block not found")
    function = extract_function(script.group(1), "calculate")

    with tempfile.TemporaryDirectory() as tmp:
        harness = Path(tmp) / "harness.js"
        payload = Path(tmp) / "cases.json"
        harness.write_text(
            function
            + "\nconst fs = require('fs');"
            + "\nconst cases = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));"
            + "\nconst out = cases.map(c => { const r = calculate(c[0], c[1], c[2], c[3], !!c[4]);"
            + " return {...r, breakeven: Number.isFinite(r.breakeven) ? r.breakeven : null}; });"
            + "\nprocess.stdout.write(JSON.stringify(out));",
            encoding="utf-8",
        )
        payload.write_text(json.dumps(cases), encoding="utf-8")
        result = subprocess.run(
            [node, str(harness), str(payload)],
            capture_output=True,
            text=True,
            timeout=120,
        )
    expect(
        result.returncode == 0,
        f"node execution failed ({result.returncode}): {result.stderr[:800]}",
    )
    return json.loads(result.stdout)


def verify_formula_matches_page() -> None:
    cases = []
    for mrr in (500, 1000, 3205.13, 5376.34, 8000, 15151.52, 20000, 50000):
        for aov in (5, 10, 40, 100, 500):
            for annual in (0, 399, 1000, 1999, 100000):
                for intl in (0, 35, 70, 100):
                    for fx in (0, 1):
                        cases.append([mrr, aov, annual, intl, fx])

    actual = run_page_calculator(cases)
    expect(len(actual) == len(cases), "node returned the wrong number of results")
    for case, got in zip(cases, actual):
        want = reference(*case)
        label = f"calculate{tuple(case)}"
        for key in (
            "orders",
            "morPercent",
            "morFixed",
            "mor",
            "stripeRate",
            "stripePercent",
            "stripeFixed",
            "compliance",
            "stripe",
            "delta",
            "rateDelta",
        ):
            close(got[key], want[key], f"{label}.{key}")
        if math.isinf(want["breakeven"]):
            expect(got["breakeven"] is None, f"{label}.breakeven should be Infinity")
        else:
            close(got["breakeven"], want["breakeven"], f"{label}.breakeven")


def verify_published_numbers() -> None:
    tier1 = reference(8000, 40, 1000, 0, False)
    close(tier1["mor"], 500.00, "tier1 mor")
    close(tier1["stripe"], 375.3333333333333, "tier1 stripe")
    close(tier1["delta"], 124.66666666666669, "tier1 delta")
    close(tier1["delta"] * 12, 1496.00, "tier1 annual saving")
    close(tier1["breakeven"], 3205.1282051282046, "tier1 breakeven")
    expect(round(tier1["breakeven"]) == 3205, "tier1 breakeven must round to $3,205")

    tier2 = reference(8000, 40, 1000, 70, False)
    close(tier2["stripeRate"], 0.0395, "tier2 rate")
    close(tier2["stripe"], 459.3333333333333, "tier2 stripe")
    close(tier2["delta"], 40.666666666666686, "tier2 delta")
    close(tier2["delta"] * 12, 488.00, "tier2 annual saving")
    close(tier2["breakeven"], 5376.344086021504, "tier2 breakeven")
    expect(round(tier2["breakeven"]) == 5376, "tier2 breakeven must round to $5,376")

    tier2_20k = reference(20000, 40, 1000, 70, False)
    close(tier2_20k["delta"] * 12, 2720.00, "tier2 $20k annual saving")

    tier3 = reference(8000, 40, 1000, 70, True)
    close(tier3["stripeRate"], 0.0495, "tier3 rate")
    close(tier3["stripe"], 539.3333333333334, "tier3 stripe")
    close(tier3["delta"], -39.33333333333337, "tier3 delta")
    close(tier3["breakeven"], 15151.515151515148, "tier3 breakeven")
    expect(round(tier3["breakeven"]) == 15152, "tier3 breakeven must round to $15,152")
    expect(tier3["delta"] < 0, "tier3 must make the MoR cheaper at $8k MRR")
    close(-tier3["delta"], 39.33333333333337, "tier3 MoR saving")

    zero = reference(1234, 40, 0, 0, False)
    expect(zero["breakeven"] == 0, "zero compliance budget must yield zero break-even")

    never = reference(8000, 500, 1000, 100, True)
    expect(math.isinf(never["breakeven"]), "negative rate delta must yield Infinity break-even")


def verify_home_markup() -> None:
    html = read(INDEX)

    expect(
        '<link rel="canonical" href="https://pay.mybskm.top/">' in html,
        "home canonical is missing or wrong",
    )
    expect(
        '<p class="sub">Company formation through Firstbase ($399) + Stripe.</p>' in html,
        "Firstbase subtitle is missing",
    )
    expect(
        '<a class="cta" href="https://go.272738.xyz/firstbase?src=pay_calc_winner" rel="sponsored noopener">Launch US LLC with Firstbase ↗</a>'
        in html,
        "Firstbase primary CTA is missing",
    )
    expect(
        '<a href="https://go.272738.xyz/firstbase?src=pay_resources" rel="sponsored noopener">Form US LLC with Firstbase ($399) ↗</a>'
        in html,
        "Firstbase resources link is missing",
    )

    stripe_card = re.search(r'<article class="card" id="stripe-card">.*?</article>', html, re.S)
    expect(stripe_card is not None, "stripe card block not found")
    block = stripe_card.group(0)
    expect("go.272738.xyz/doola" not in block, "stripe card must not point at the Doola link")
    expect(
        "go.272738.xyz/firstbase?src=pay_calc_winner" in block,
        "stripe card CTA must be the Firstbase relay",
    )

    resources = re.search(r'<div class="resources">(.*?)</div>', html, re.S)
    expect(resources is not None, "resources block not found")
    first_link = re.search(r"<a\b[^>]*>", resources.group(1))
    expect(first_link is not None, "resources block has no links")
    expect(
        "go.272738.xyz/firstbase?src=pay_resources" in first_link.group(0),
        "Firstbase must be the first resources link",
    )

    expect('href="/blog/"' in html, "top nav must link to /blog/")
    expect(
        'href="/blog/mor-vs-us-llc-breakeven.html"' in html,
        "top nav must link to the new research article",
    )
    expect(
        html.count('href="/blog/mor-vs-us-llc-breakeven.html"') >= 2,
        "article entry must appear in the nav and in the mid-page research block",
    )

    expect(
        '<input id="intl" type="range" min="0" max="100" step="5" value="0"' in html,
        "intl range control must default to 0 with step 5",
    )
    expect(
        '<input id="fx" type="checkbox" role="switch"' in html,
        "fx toggle must be a checkbox switch",
    )
    fx_tag = re.search(r'<input id="fx"[^>]*>', html)
    expect(fx_tag is not None, "fx input not found")
    expect("checked" not in fx_tag.group(0), "fx must default to off")

    presets = re.findall(r'<button type="button" class="pill-btn"([^>]*)>([^<]+)</button>', html)
    expect(len(presets) == 3, "exactly three preset pills are required")
    expected_presets = {
        "US Domestic Cards (0% Intl)": ("0", "0"),
        "Global SaaS Typical (70% Intl)": ("70", "0"),
        "Non-USD Checkout (70% Intl + 1% FX)": ("70", "1"),
    }
    for attrs, label in presets:
        data_intl = re.search(r'data-intl="(\d+)"', attrs)
        data_fx = re.search(r'data-fx="(\d)"', attrs)
        expect(data_intl is not None and data_fx is not None, f"preset {label} missing data attributes")
        expect(label in expected_presets, f"unexpected preset label: {label}")
        expect(
            (data_intl.group(1), data_fx.group(1)) == expected_presets[label],
            f"preset {label} has wrong parameters",
        )

    for snippet in (
        "query.get('intl')",
        "query.get('fx')",
        "url.searchParams.set('intl'",
        "url.searchParams.set('fx'",
        "0.029 + (intl / 100) * 0.015 + (fx ? 0.01 : 0)",
        "const rateDelta = (0.05 - stripeRate) + (0.20 / aov);",
        "const breakeven = rateDelta > 0 ? (compliance / rateDelta) : Infinity;",
        "const delta = mor - stripe;",
    ):
        expect(snippet in html, f"calculator JS is missing: {snippet}")


def visible_text(fragment: str) -> str:
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    fragment = fragment.replace("&amp;", "&").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", fragment).strip()


def verify_article() -> None:
    html = read(ARTICLE)

    expect(
        f'<link rel="canonical" href="{CANONICAL_ARTICLE}">' in html,
        "article canonical is missing or not self-referential",
    )
    expect(
        "<title>The 5% MoR Illusion: Exact US LLC + Stripe Breakeven for Non-US SaaS Founders (2026)</title>"
        in html,
        "article title is wrong",
    )
    h1 = re.search(r"<h1>(.*?)</h1>", html, re.S)
    expect(h1 is not None, "article h1 missing")
    expect(
        visible_text(h1.group(1))
        == "The 5% MoR Illusion: Exact US LLC + Stripe Breakeven for Non-US SaaS Founders (2026)",
        "article h1 does not match the required title",
    )

    body = re.search(r'<div class="content">(.*?)</div>\s*<div class="cta-panel">', html, re.S)
    expect(body is not None, "article content container not found")
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", visible_text(body.group(1)))
    expect(len(words) >= 1700, f"article body has only {len(words)} English words; 1700 required")

    lower = html.lower()
    expect("ftc" in lower and "affiliate" in lower and "commission" in lower, "FTC affiliate disclosure is missing")

    schemas = re.findall(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S
    )
    expect(schemas, "article JSON-LD is missing")
    article_schema = None
    for raw in schemas:
        data = json.loads(raw)
        if data.get("@type") == "Article":
            article_schema = data
            break
    expect(article_schema is not None, "Article JSON-LD not found")
    for field in ("headline", "description", "author", "publisher", "datePublished", "dateModified", "mainEntityOfPage"):
        expect(bool(article_schema.get(field)), f"Article JSON-LD missing {field}")
    expect(
        article_schema["headline"] == visible_text(h1.group(1)),
        "Article headline must match the visible h1",
    )
    expect(article_schema["author"].get("@type") == "Person", "Article author must be a Person")
    expect(article_schema["publisher"].get("@type") == "Organization", "Article publisher must be an Organization")
    expect(
        article_schema["mainEntityOfPage"].get("@id") == CANONICAL_ARTICLE,
        "Article mainEntityOfPage must equal the canonical URL",
    )

    for link in (
        "https://pay.mybskm.top/?mrr=8000&aov=40&intl=70",
        "https://pay.mybskm.top/?mrr=20000&aov=40&intl=70",
        "https://go.272738.xyz/firstbase?src=article_mor_breakeven",
    ):
        expect(link in html, f"article is missing link: {link}")
    firstbase = re.search(
        r'<a\b[^>]*href="https://go\.272738\.xyz/firstbase\?src=article_mor_breakeven"[^>]*>',
        html,
    )
    expect(firstbase is not None, "Firstbase article CTA anchor not found")
    expect(
        'rel="sponsored noopener"' in firstbase.group(0),
        "Firstbase article CTA must carry rel=sponsored noopener",
    )

    for token in (
        "$375.33",
        "$500.00",
        "$459.33",
        "$539.33",
        "$3,205",
        "$5,376",
        "$15,152",
        "$1,496",
        "$488",
        "$2,720",
        "$39.33",
        "$25,000",
        "IRS Form 5472",
        "Firstbase",
    ):
        expect(token in html, f"article is missing required figure/prose token: {token}")


def verify_blog_index_and_sitemap() -> None:
    html = read(BLOG_INDEX)
    expect(
        f'<link rel="canonical" href="{CANONICAL_BLOG}">' in html,
        "blog index canonical is missing or wrong",
    )
    schemas = re.findall(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S
    )
    expect(schemas, "blog index JSON-LD is missing")
    collection = None
    for raw in schemas:
        data = json.loads(raw)
        if data.get("@type") == "CollectionPage":
            collection = data
            break
    expect(collection is not None, "CollectionPage JSON-LD not found")
    expect(collection.get("url") == CANONICAL_BLOG, "CollectionPage url mismatch")
    parts = collection.get("hasPart") or []
    expect(
        any(part.get("url") == CANONICAL_ARTICLE for part in parts),
        "CollectionPage hasPart must list the research article",
    )
    expect(
        'href="/blog/mor-vs-us-llc-breakeven.html"' in html
        or f'href="{CANONICAL_ARTICLE}"' in html,
        "blog index must link to the research article",
    )
    expect(
        'href="https://pay.mybskm.top/"' in html,
        "blog index must navigate back to the calculator",
    )
    expect(
        'href="https://pay.mybskm.top/blog/mor-vs-us-llc-breakeven.html"' in html,
        "blog index must expose the absolute article URL",
    )

    sitemap = read(SITEMAP)
    expect(CANONICAL_BLOG in sitemap, "sitemap is missing the blog index")
    expect(CANONICAL_ARTICLE in sitemap, "sitemap is missing the research article")
    expect("<urlset" in sitemap and "</urlset>" in sitemap, "sitemap is malformed")


def main() -> int:
    verify_formula_matches_page()
    print(f"PASS formula parity: 1,600 cases, page JS == independent Python reference ({PASSED} checks)")
    verify_published_numbers()
    print("PASS published numbers: $3,205 / $5,376 / $15,152 breakeven, $1,496 / $488 / $2,720 savings, -$39.33 tier 3")
    verify_home_markup()
    print("PASS home markup: Firstbase CTA, resources, nav, intl/fx controls and presets")
    verify_article()
    print("PASS article: canonical, Article JSON-LD, FTC disclosure, 1,700+ words, figures and links")
    verify_blog_index_and_sitemap()
    print(f"PASS blog index, CollectionPage JSON-LD and sitemap ({PASSED} total checks)")
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
