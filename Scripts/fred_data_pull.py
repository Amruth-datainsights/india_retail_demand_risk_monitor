# ============================================
# PHASE 2: Pull India Economic Data from FRED
# ============================================

# Step 1: Install the FRED API library (only needed once per Colab session)
!pip install fredapi --quiet

# Step 2: Import libraries
from fredapi import Fred
import pandas as pd

# Step 3: Connect to FRED using your API key
# ⚠️ REPLACE the text below with your actual FRED API key
API_KEY = "YOUR_API_KEY_HERE"
fred = Fred(api_key=API_KEY)

# Step 4: Define the indicators we want (series ID : friendly name)
series_dict = {
    "INDCPIALLMINMEI": "CPI (Inflation Level)",
    "IRSTCI01INM156N": "Interbank Interest Rate",
    "INDIRLTLT01STM": "10-Year Bond Yield",
    "CCUSMA02INM618N": "USD/INR Exchange Rate",
    "INDMABMM301GYSAM": "M3 Money Supply Growth",
}

# Step 5: Pull each series and store it
all_data = {}

for series_id, friendly_name in series_dict.items():
    try:
        data = fred.get_series(series_id)
        all_data[friendly_name] = data
        print(f"✅ Pulled: {friendly_name} ({len(data)} data points)")
    except Exception as e:
        print(f"❌ Failed to pull {friendly_name} ({series_id}): {e}")

# Step 6: Combine everything into one table
df = pd.DataFrame(all_data)
df.index.name = "Date"

# Step 7: Show a preview
print("\nPreview of your data:")
print(df.tail(10))

# Step 8: Save as CSV
df.to_csv("india_economic_data.csv")
print("\n✅ Saved as india_economic_data.csv")

# Step 9: Download the file to your computer
from google.colab import files
files.download("india_economic_data.csv")
