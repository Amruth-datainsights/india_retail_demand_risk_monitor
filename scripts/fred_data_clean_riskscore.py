# ============================================
# PHASE 3: Clean Data & Build a Risk Score
# ============================================

# Step 1: Import libraries
import pandas as pd

# Step 2: Upload your CSV from Phase 2
# Run this cell, then click "Choose Files" and select india_economic_data.csv
from google.colab import files
uploaded = files.upload()

# Step 3: Load the CSV into a table
df = pd.read_csv("india_economic_data.csv", index_col="Date", parse_dates=True)
df = df.sort_index()

print("Raw data preview:")
print(df.tail())
print(f"\nTotal rows: {len(df)}")
print(f"\nMissing values per column:\n{df.isna().sum()}")

# ============================================
# Step 4: Handle missing values
# ============================================
# Some indicators update monthly, some quarterly, so there will be gaps.
# We "forward fill" — carry the last known value forward until a new one arrives.
# This is standard practice for economic time series.
df_filled = df.ffill()

# Drop any remaining rows at the very start where we have no data yet
df_filled = df_filled.dropna()

print("\n✅ Missing values handled. New shape:", df_filled.shape)

# ============================================
# Step 5: Calculate % change (Year-over-Year)
# ============================================
# Raw numbers like "CPI = 189" don't mean much on their own.
# We care about the RATE OF CHANGE — is it rising fast or slow?
# 12 months back = year-over-year change (standard in economics)

yoy_change = df_filled.pct_change(periods=12) * 100
yoy_change = yoy_change.add_suffix(" (YoY % change)")

print("\nYear-over-year % change preview:")
print(yoy_change.tail())

# ============================================
# Step 6: Build a simple composite Risk Score
# ============================================
# Logic: rising inflation, rising interest rates, weakening rupee (INR) all
# signal LOWER consumer demand ahead = HIGHER risk.
# Rising money supply growth signals MORE liquidity = LOWER risk (offsetting).
#
# We'll normalize each YoY % change to a comparable scale, then combine.
# This is a simple weighted average — a very typical BA approach for a first version.

# Pick the columns we'll use in the score (must match names from Step 5 output)
score_inputs = pd.DataFrame({
    "inflation": yoy_change["CPI (Inflation Level) (YoY % change)"],
    "interest_rate": yoy_change["Interbank Interest Rate (YoY % change)"],
    "bond_yield": yoy_change["10-Year Bond Yield (YoY % change)"],
    "fx_weakness": yoy_change["USD/INR Exchange Rate (YoY % change)"],  # INR rising = rupee weaker
    "money_supply": yoy_change["M3 Money Supply Growth (YoY % change)"],
})

# Normalize each column to a 0-100 scale so they're comparable
def normalize(series):
    return (series - series.min()) / (series.max() - series.min()) * 100

normalized = score_inputs.apply(normalize)

# Weights: how much each factor matters (adjust these based on your judgment!)
weights = {
    "inflation": 0.30,       # higher weight = matters more to consumer demand
    "interest_rate": 0.25,
    "bond_yield": 0.15,
    "fx_weakness": 0.15,
    "money_supply": -0.15,   # negative weight = more money supply LOWERS risk
}

risk_score = sum(normalized[col] * w for col, w in weights.items())
risk_score = risk_score.rename("Retail Demand Risk Score")

print("\nRisk Score preview (higher = more risk of weaker consumer demand):")
print(risk_score.tail(10))

# ============================================
# Step 7: Combine everything into one final table
# ============================================
final_table = df_filled.join(yoy_change).join(risk_score)

print("\n✅ Final combined table shape:", final_table.shape)
print(final_table.tail())

# ============================================
# Step 8: Save and download
# ============================================
final_table.to_csv("india_risk_dashboard_data.csv")
print("\n✅ Saved as india_risk_dashboard_data.csv")

files.download("india_risk_dashboard_data.csv")
