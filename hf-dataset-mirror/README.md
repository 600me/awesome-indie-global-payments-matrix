---
license: mit
task_categories:
  - tabular-classification
language:
  - en
tags:
  - saas
  - payments
  - merchant-of-record
  - stripe
  - paddle
  - lemon-squeezy
  - us-llc
  - firstbase
  - stripe-atlas
  - doola
  - tax
  - tco
  - indie-hacker
size_categories:
  - n<1K
pretty_name: "Global SaaS: MoR vs US LLC + Stripe 3-Year Net Fee Matrix (2026)"
---

# Global SaaS: MoR vs US LLC + Stripe 3-Year Net Fee Matrix (2026)

A flat "5% Merchant of Record" is not comparable to "2.9% + $0.30" plus a company. This dataset prices
both routes across MRR, AOV and international card mix, and reports **3-year net revenue retained**.

## Files

| File | Rows | Description |
|---|---|---|
| `data/saas_payments_mor_vs_us_llc_2026.csv` | 252 | 7 MRR x 4 AOV x 3 card mixes x 3 formation services |
| `data/saas_payments_mor_vs_us_llc_2026.jsonl` | 252 | Same records as newline-delimited JSON |

## Schema

| Column | Type | Meaning |
|---|---|---|
| `scenario_id` | string | Stable row id |
| `formation_service` | string | Firstbase ($399) / Stripe Atlas ($500) / Doola ($297) |
| `mrr_usd`, `aov_usd` | float | Revenue and average order value |
| `orders_per_month` | float | `MRR / AOV` |
| `intl_card_pct`, `fx_enabled` | int, bool | Card mix and 1% FX surcharge toggle |
| `mor_monthly_fee_usd` | float | `MRR * 5% + orders * $0.50` |
| `mor_3y_net_usd` | float | Retained revenue over 36 months via MoR |
| `stripe_blended_rate_pct` | float | `2.9% + intl*1.5% + (fx ? 1% : 0)` |
| `llc_monthly_total_usd` | float | Stripe processing + $1,000/yr compliance budget |
| `llc_3y_net_usd` | float | Retained revenue over 36 months, entity cost deducted |
| `llc_minus_mor_3y_usd` | float | Positive = LLC keeps more |
| `breakeven_mrr_usd` | float | MRR at which the LLC route overtakes MoR |

## Method

```
N             = MRR / AOV
MoR           = MRR*0.05 + N*0.50
stripe_rate   = 0.029 + intl*0.015 + (fx ? 0.01 : 0)
Stripe        = MRR*stripe_rate + N*0.30 + 1000/12
rate_delta    = (0.05 - stripe_rate) + 0.20/AOV
breakeven     = (1000/12) / rate_delta      (infinite when rate_delta <= 0)
3y_net        = 36*(MRR - monthly_fee) [- entity_3y_cost for the LLC route]
```

Entity 3-year costs (formation + franchise/agent/Form 5472 prep) are the published research figures:
Firstbase **$876**, Stripe Atlas **$1,600**, Doola **$6,177**. They exclude income tax, sales tax/VAT
registration and optional add-ons.

## Breakeven MRR (Firstbase route)

| AOV | 0% intl | 70% intl | 70% intl + 1% FX |
|---|---|---|---|
| $15 | $2,427 | $3,496 | $6,024 |
| $29 | $2,987 | $4,790 | $11,267 |
| $49 | $3,322 | $5,715 | $18,189 |
| $99 | $3,620 | $6,656 | $33,066 |

## Summary table ($49 AOV, 70% international cards, Firstbase)

| MRR | AOV | Intl % | FX | MoR fee/mo | LLC total/mo | LLC − MoR/mo |
|---|---|---|---|---|---|---|
| $1,000 | $49 | 70% | no | $60 | $129 | $69 |
| $2,500 | $49 | 70% | no | $151 | $197 | $47 |
| $5,000 | $49 | 70% | no | $301 | $311 | $10 |
| $8,000 | $49 | 70% | no | $482 | $448 | $-33 |
| $15,000 | $49 | 70% | no | $903 | $768 | $-135 |
| $25,000 | $49 | 70% | no | $1,505 | $1,224 | $-281 |
| $50,000 | $49 | 70% | no | $3,010 | $2,364 | $-646 |

## Use the calculator and mirror

- [Benchmark site](https://pay.mybskm.top/?utm_source=hf_dataset_pay)
- [HuggingFace Space](https://huggingface.co/spaces/600me/ai-saas-stripe-vs-mor-tax-calculator)

**Deep dives**
- [The 5% MoR illusion: exact US LLC + Stripe breakeven](https://pay.mybskm.top/blog/mor-vs-us-llc-breakeven.html)
- [Firstbase vs Stripe Atlas vs Doola: the 3-year bill](https://pay.mybskm.top/blog/firstbase-vs-stripe-atlas-vs-doola.html)


## The 4-calculator / 4-Space / 4-Dataset matrix

**Online calculators**
- [GPU cloud true TCO](https://gpu.mybskm.top/calculator/?utm_source=hf_dataset_matrix)
- [Scraping / anti-bot TCO](https://scrape.mybskm.top/calculator/?utm_source=hf_dataset_matrix)
- [Residential proxy sticky-session loss](https://proxy.mybskm.top/calculator/?utm_source=hf_dataset_matrix)
- [MoR vs US LLC breakeven](https://pay.mybskm.top/?utm_source=hf_dataset_matrix)

**HuggingFace Static Spaces**
- [gpu-cloud-h100-a100-pricing-benchmark](https://huggingface.co/spaces/600me/llm-gpu-cost-calculator)
- [web-scraping-anti-bot-api-benchmark](https://huggingface.co/spaces/600me/rag-web-scraping-cost-calculator)
- [residential-proxy-commercial-policy-matrix](https://huggingface.co/spaces/600me/residential-proxy-sticky-session-calculator)
- [global-saas-mor-vs-us-llc-fee-matrix](https://huggingface.co/spaces/600me/ai-saas-stripe-vs-mor-tax-calculator)

**HuggingFace Datasets**
- [gpu-cloud-h100-a100-pricing-benchmark](https://huggingface.co/datasets/600me/gpu-cloud-h100-a100-pricing-benchmark)
- [web-scraping-anti-bot-api-benchmark](https://huggingface.co/datasets/600me/web-scraping-anti-bot-api-benchmark)
- [residential-proxy-commercial-policy-matrix](https://huggingface.co/datasets/600me/residential-proxy-commercial-policy-matrix)


## Transparency & FTC affiliate disclosure

This dataset is published by the independent cost-research project at mybskm.top. Some outbound vendor links are affiliate links: if you open one and later buy, we may earn a commission at no extra cost to you. Commissions never change the measured numbers, the formula, or which vendor wins a scenario, and the free open-source baseline is included on purpose because it pays us nothing. Every price is a vendor-published list rate captured on the `observed_at` date; prices, trials, KYC rules and refund terms change without notice. Nothing here is a quote, a guarantee of eligibility, tax or legal advice, or a promise of results. Verify current pricing and terms with the vendor before purchasing.
