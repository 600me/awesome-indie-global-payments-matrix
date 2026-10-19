---
title: MoR vs US LLC + Stripe Breakeven Calculator
emoji: 💳
colorFrom: green
colorTo: blue
sdk: static
app_file: index.html
pinned: false
license: mit
short_description: Non-US SaaS payments — MoR vs US LLC + Stripe breakeven math
---

# MoR vs US LLC + Stripe Breakeven Calculator

A single-file, zero-dependency Static Space for non-US SaaS founders deciding between a **5%
Merchant of Record** (Paddle, Lemon Squeezy) and a **US LLC plus Stripe**.

A flat 5% looks simple until a 70% international card mix, a 1% FX conversion and the annual
compliance bill land on the same invoice. Formation fees — $297, $399, $500 — are not the price of
holding the company. Three years of franchise tax, registered agent renewals, bookkeeping and the
IRS Form 5472 filing (a **$25,000 penalty** when missed) are.

## What it computes

```text
N                = MRR / AOV
MoR              = MRR × 0.05 + N × $0.50
StripeRate       = 2.9% + (intl% / 100) × 1.5% + (FX ? 1% : 0)
Stripe           = MRR × StripeRate + N × $0.30 + annual_budget / 12
Net difference   = MoR − Stripe
RateDelta        = (5% − StripeRate) + (0.20 / AOV)
Break-even MRR   = RateDelta > 0 ? (annual_budget / 12) / RateDelta : Infinity
```

- Monthly and annualized totals for **Paddle**, **Lemon Squeezy** and **US LLC + Stripe**, side by
  side, on the same revenue.
- **Editable annual compliance budget** (default $1,000/year) covering franchise tax, registered
  agent renewal, bookkeeping and the Form 5472 filing. Formation fees are deliberately excluded and
  treated as sunk.
- **Break-even MRR** for each structure — the exact revenue level at which the LLC overtakes a
  Merchant of Record.
- **Two card-mix controls** (international share, FX enabled) that move the answer: defaults give
  $3,205/mo, a 70% international mix gives $5,376/mo, and adding 1% FX gives $15,152/mo at $8,000 MRR.
- **Share link** that round-trips MRR, AOV, budget mix and card mix through URL parameters. Every
  input recomputes live in the browser; nothing is uploaded.

## Why static

`sdk: static` serves this Space as plain HTML/CSS/JS: no container, no Python server, no cold start.
`index.html` is the complete page with no external scripts, stylesheets, fonts or tracking pixels.

## Files

- `index.html` — the complete calculator, styles and vanilla JavaScript.
- `README.md` — this Space card and static SDK metadata.

## Links

- Full calculator: https://pay.mybskm.top/
- The 5% MoR illusion (exact breakeven): https://pay.mybskm.top/blog/mor-vs-us-llc-breakeven.html
- Firstbase vs Stripe Atlas vs Doola, 3-year bill: https://pay.mybskm.top/blog/firstbase-vs-stripe-atlas-vs-doola.html
- Decision matrix repository: https://github.com/600me/awesome-indie-global-payments-matrix

## The four Hugging Face Static Spaces in this matrix

1. [GPU Fit & Cost Calculator](https://huggingface.co/spaces/600me/llm-gpu-cost-calculator) — VRAM sizing, NVLink topology and GPU rental TCO.
2. [LLM/RAG Web Scraping TCO Calculator](https://huggingface.co/spaces/600me/rag-web-scraping-cost-calculator) — cost per 1,000 clean Markdown pages.
3. [Residential Proxy Sticky-Session Calculator](https://huggingface.co/spaces/600me/residential-proxy-sticky-session-calculator) — the `cf_clearance` re-run tax.
4. **This Space** — cross-border SaaS payment and US LLC compliance math.

Full-size sites: [gpu.mybskm.top](https://gpu.mybskm.top/) · [scrape.mybskm.top](https://scrape.mybskm.top/) · [proxy.mybskm.top](https://proxy.mybskm.top/) · [pay.mybskm.top](https://pay.mybskm.top/)

## Disclosure and scope

The Firstbase button is an affiliate link (`src=hf_space_pay_winner` / `src=hf_space_pay_resources`).
We may earn a commission at no additional cost to the visitor, and the decision rule is arithmetic,
not commission. The calculator core is cross-checked against an independent Python implementation
(`test_payments_calculator_math.py`) in the main repository.

This is a planning model for budgeting, **not tax, legal or accounting advice**, and not a
recommendation to form an entity. Fees, franchise rules and IRS requirements change, and eligibility
for any payment provider is decided by that provider. Confirm current pricing and obligations with
the provider and a qualified professional before acting.
