# Business Memo: India Retail Demand Risk Monitor

**To:** VP of Merchandising / Retail Planning
**From:** [Your Name]
**Subject:** Early-Warning Signal for Consumer Demand Risk — Findings & Recommendation

---

## The Problem

General retail chains in India currently rely on lagging signals — sales dips, inventory pile-ups — to detect softening consumer demand. By the time these show up, the damage to margins and stock positioning has already happened. This project builds a forward-looking Retail Demand Risk Score using live macroeconomic data, so merchandising, pricing, and inventory teams can act *ahead* of demand shifts rather than reacting after the fact.

## The Approach

I built a composite Risk Score using five macroeconomic indicators sourced live from the Federal Reserve's FRED database for India: inflation (CPI), interbank interest rates, 10-year bond yields, the USD/INR exchange rate, and M3 money supply growth. Each indicator was converted to a year-over-year % change, normalized, and combined into a single weighted score — higher score signals higher risk of weakening consumer spending.

On top of the model, I built a repeatable AI-assisted analysis workflow: feeding the dataset to an AI assistant with a structured prompt lets the business ask plain-English questions ("why is risk rising?") and get grounded, data-backed answers in seconds — work that would otherwise take an analyst hours of manual cross-referencing.

## Key Findings

1. **Historical validation:** The model correctly flagged a sharp risk spike in 2021–2022 (risk score rising from ~25 to ~45), coinciding with the well-documented post-COVID global inflation shock — giving confidence the indicator selection and weighting are sound.

2. **Current risk level:** As of the latest data, the score sits at approximately 18–24, well below the 2021–22 peak, but the *composition* of the risk has shifted.

3. **What's driving risk today is different from what drove it historically.** Historically, interest rate momentum has been the strongest overall correlate of the risk score. But interest rates have actually been *cut* this year (5.75% → 5.50%), so rates are not today's culprit. Instead, **USD/INR depreciation is the standout current driver** — the rupee has weakened over 11% in the past year, with a sharp acceleration in the most recent months (+₹2.6 in the final month alone). Bond yields are a secondary contributor, but the FX move is larger in magnitude and tracks the recent risk climb most closely.

## Recommendation

Because this is an **FX-led risk rather than a rate-led one**, the sharpest lever available to the business is on the **cost side, not the customer-financing side**:

- **Renegotiate or hedge import-heavy supplier contracts** before further rupee depreciation compounds costs
- **Review pricing on categories with high imported-input content** proactively, before margin erosion shows up in quarterly numbers
- Continue monitoring the risk score monthly — if bond yields and inflation begin accelerating alongside the FX move, that would signal a broader, harder-to-manage demand shock is forming (similar to 2021–22), warranting a shift toward inventory caution as well.

## Limitations & Next Steps

- FRED lacks an India-specific consumer sentiment/retail sales series. A natural next iteration is to add RBI's Consumer Confidence Survey (Current Situation Index / Future Expectation Index), which would fill this gap but updates only bi-monthly and requires manual integration since it isn't available via API
- Risk score weights were set using directional economic reasoning, not a formally fitted statistical model — a natural next iteration would be to backtest weights against actual historical retail sales data if/when available
- Current AI layer is a manual, on-demand workflow rather than a live-connected application — a natural extension would be automating the data refresh and connecting the AI layer directly to the dashboard

---

*Data sources: FRED (Federal Reserve Bank of St. Louis). Dashboard built in Power BI; data pipeline in Python; AI-assisted analysis via Claude.*

*Data current as of: July 2026. This tool is designed to be refreshed periodically — re-run the data pipeline scripts to pull the latest available indicators.*
