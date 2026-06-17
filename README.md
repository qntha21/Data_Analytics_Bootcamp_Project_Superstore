# Superstore Profitability & Discount Analysis

## Overview
Built 3 interactive Tableau dashboards to answer: where should Superstore focus to maximize profit? Covered regional performance, category profitability, and the quantified impact of discount levels with strategic recommendations per region.

## Problem Statement
Despite overall profitability, $156,131 is lost annually to excessive discounting. 1,871 orders (19.4%) generate a loss. Central region applies a 30% average discount on Furniture vs. West's 13%, a structural difference that explains most of the profitability gap between regions.

## Dataset
- **Source:** Sample Superstore dataset
- **Size:** 9,994 orders × 21 columns
- **Period:** 2014–2017, 4 US regions (West, East, Central, South)
- **Key columns:** Region/State/City, Category/Sub-Category, Sales, Profit, Discount

## Key Findings
- **KPIs:** $2.3M total sales · 12.47% profit margin · 15.62% avg discount · 1,871 loss orders
- **Discount impact per order:** 0% → +$66.90 · 1–10% → +$96.06 · 11–20% → +$24.74 · 21–30% → **-$45.68** · 31–50% → **-$156.28**
- **By region:** West leads (14.9% margin, 9.9% loss orders); Central is worst (7.9% margin, 31.9% loss orders)
- **By sub-category:** Tables is the biggest loss-maker (-$17,725); Copiers is most profitable (+$55,618)
- Texas and Illinois show high sales but negative profit, a pattern invisible without dashboard-level analysis

## Recommendations by Region
- **West (Star Performer):** Scale marketing budget 30–40%; replicate its 11% discount model company-wide
- **East (High Performer):** Hold discount rate at a 15% cap
- **South (Needs Attention):** Stop discount increases; prioritize efficiency over expansion
- **Central (Urgent):** Cap all discounts at 15% immediately; eliminate Furniture discounts entirely; shift focus from Consumer (3.4% margin) to Corporate (11.8%) and B2B

**Bottom line:** A 54% profit improvement opportunity exists — without acquiring a single new customer.

## Tools Used
Tableau Public · Python (EDA) · Calculated Fields · Heatmap · Scatter Plot · Slope Chart

---
*Part of the Data Analytics Bootcamp portfolio (2026)*
