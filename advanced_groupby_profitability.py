import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your clean data
try:
    df = pd.read_csv("well_data_cleaned.csv")
except FileNotFoundError:
    data = {
        "Well_Name": ["Well_Alpha", "Well_Beta",
                      "Well_Gamma", "Well_Delta",
                      "Well_Epsilon", "Well_Zeta",
                      "Well_Eta", "Well_Theta"],
        "Location": ["Northern Block",
                     "Southern Block",
                     "Northern Block",
                     "Eastern Block",
                     "Southern Block",
                     "Eastern Block",
                     "Northern Block",
                     "Western Block"],
        "Type": ["Oil", "Oil",
                 "Gas Condensate", "Oil",
                 "Oil", "Gas Condensate",
                 "Oil", "Oil"],
        "Avg_Daily_Barrels": [520, 303, 742,
                              179, 634, 289,
                              891, 156],
        "Days_Active": [365, 280, 410, 190,
                        320, 245, 400, 180],
        "Water_Cut": [0.15, 0.22, 0.08, 0.45,
                      0.18, 0.35, 0.11, 0.67],
        "Status": ["Active", "Active",
                   "Active", "Review needed",
                   "Active", "Review needed",
                   "Active", "Inactive"]
    }
    df = pd.DataFrame(data)

print("Data loaded. Shape:", df.shape)

# ═══════════════════════════════════
# GROUPBY LEVEL 1: SINGLE AGGREGATION
# ═══════════════════════════════════

print("\n=== PRODUCTION BY LOCATION BLOCK ===")
by_location = df.groupby("Location")[
    "Avg_Daily_Barrels"
].sum().sort_values(ascending=False)
print(by_location)

print("\n=== AVERAGE WATER CUT BY TYPE ===")
by_type = df.groupby("Type")[
    "Water_Cut"
].mean().round(3) * 100
print(by_type.round(1).astype(str) + "%")

# ═══════════════════════════════════
# GROUPBY LEVEL 2: MULTIPLE AGGREGATIONS
# ═══════════════════════════════════

print("\n=== COMPREHENSIVE BLOCK ANALYSIS ===")
block_analysis = df.groupby("Location").agg(
    Well_Count=("Well_Name", "count"),
    Total_Production=("Avg_Daily_Barrels", "sum"),
    Avg_Production=("Avg_Daily_Barrels", "mean"),
    Max_Production=("Avg_Daily_Barrels", "max"),
    Min_Production=("Avg_Daily_Barrels", "min"),
    Avg_Water_Cut=("Water_Cut", "mean"),
    Total_Days=("Days_Active", "sum")
).round(2)

print(block_analysis.to_string())

# ═══════════════════════════════════
# GROUPBY LEVEL 3: CONDITIONAL GROUPBY
# ═══════════════════════════════════

print("\n=== ACTIVE WELLS BY BLOCK ===")
active_by_block = df[
    df["Status"] == "Active"
].groupby("Location").agg(
    Active_Wells=("Well_Name", "count"),
    Active_Production=("Avg_Daily_Barrels", "sum"),
    Avg_Water_Cut=("Water_Cut", "mean")
).round(3)

print(active_by_block)

# ═══════════════════════════════════
# GROUPBY LEVEL 4: TRANSFORM
# Adds group-level statistics back
# to the original dataframe
# ═══════════════════════════════════

# Add each well's production as % of
# its block's total production
df["Block_Total"] = df.groupby(
    "Location"
)["Avg_Daily_Barrels"].transform("sum")

df["Pct_of_Block"] = (
    df["Avg_Daily_Barrels"] / df["Block_Total"]
    * 100
).round(1)

print("\n=== EACH WELL'S SHARE OF ITS BLOCK ===")
print(df[[
    "Well_Name", "Location",
    "Avg_Daily_Barrels", "Pct_of_Block"
]].sort_values(
    ["Location", "Pct_of_Block"],
    ascending=[True, False]
).to_string())

# ═══════════════════════════════════
# CREATE A SECOND DATASET
# Financial performance by block
# ═══════════════════════════════════

financial_data = {
    "Location": ["Northern Block",
                 "Southern Block",
                 "Eastern Block",
                 "Western Block"],
    "Oil_Price_USD": [72.50, 72.50,
                      72.50, 72.50],
    "Operating_Cost_Per_Bbl": [18.20, 22.10,
                                31.50, 45.80],
    "Investment_USD_M": [125, 87, 43, 28],
    "Years_Producing": [3, 2, 1, 1]
}

df_financial = pd.DataFrame(financial_data)

print("=== FINANCIAL DATA ===")
print(df_financial)

# ═══════════════════════════════════
# MERGE THE TWO DATASETS
# Like a SQL JOIN in Python
# ═══════════════════════════════════

# Get production summary by block
prod_summary = df.groupby("Location").agg(
    Total_Daily_Bbl=("Avg_Daily_Barrels", "sum"),
    Well_Count=("Well_Name", "count")
).reset_index()

# Merge production with financial
combined = pd.merge(
    prod_summary,
    df_financial,
    on="Location",
    how="left"
)

print("\n=== MERGED DATASET ===")
print(combined.to_string())

# ═══════════════════════════════════
# CALCULATE PROFITABILITY
# ═══════════════════════════════════

combined["Daily_Revenue_USD"] = (
    combined["Total_Daily_Bbl"] *
    combined["Oil_Price_USD"]
)

combined["Daily_OpEx_USD"] = (
    combined["Total_Daily_Bbl"] *
    combined["Operating_Cost_Per_Bbl"]
)

combined["Daily_Profit_USD"] = (
    combined["Daily_Revenue_USD"] -
    combined["Daily_OpEx_USD"]
)

combined["Annual_Profit_USD_M"] = (
    combined["Daily_Profit_USD"] * 365 / 1_000_000
).round(2)

combined["ROI_Pct"] = (
    combined["Annual_Profit_USD_M"] /
    combined["Investment_USD_M"] * 100
).round(1)

# ═══════════════════════════════════
# PROFITABILITY REPORT
# ═══════════════════════════════════

print("\n" + "="*55)
print("  BLOCK PROFITABILITY ANALYSIS")
print("="*55)

for _, row in combined.sort_values(
    "ROI_Pct", ascending=False
).iterrows():
    print(f"\n  {row['Location']}")
    print(f"  Production   : "
          f"{row['Total_Daily_Bbl']:,.0f} bbl/day")
    print(f"  Daily Revenue: "
          f"${row['Daily_Revenue_USD']:,.0f}")
    print(f"  Daily OpEx   : "
          f"${row['Daily_OpEx_USD']:,.0f}")
    print(f"  Annual Profit: "
          f"${row['Annual_Profit_USD_M']:.1f}M")
    print(f"  ROI          : {row['ROI_Pct']:.1f}%")
    print(f"  Investment   : "
          f"${row['Investment_USD_M']}M")

print("\n" + "="*55)
print(f"  BEST ROI: "
      f"{combined.loc[combined['ROI_Pct'].idxmax(), 'Location']}")
print(f"  WORST ROI: "
      f"{combined.loc[combined['ROI_Pct'].idxmin(), 'Location']}")
print("="*55)

# ═══════════════════════════════════
# PROFITABILITY VISUALISATION
# ═══════════════════════════════════

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Annual Profit by Block
colors_profit = [
    "#4CAF50" if p > 0 else "#F44336"
    for p in combined["Annual_Profit_USD_M"]
]

axes[0].bar(
    combined["Location"],
    combined["Annual_Profit_USD_M"],
    color=colors_profit,
    edgecolor="black",
    linewidth=0.5
)
axes[0].set_title(
    "Annual Profit by Block (USD Millions)",
    fontweight="bold"
)
axes[0].set_xlabel("Block")
axes[0].set_ylabel("Annual Profit (USD M)")
axes[0].tick_params(axis="x", rotation=30)

for i, (_, row) in enumerate(combined.iterrows()):
    axes[0].text(
        i, row["Annual_Profit_USD_M"] + 0.5,
        f"${row['Annual_Profit_USD_M']:.1f}M",
        ha="center", fontsize=9
    )

# Chart 2: ROI comparison
axes[1].barh(
    combined["Location"],
    combined["ROI_Pct"],
    color=["#2196F3" if r > 50 else
           "#FF9800" if r > 20 else
           "#F44336"
           for r in combined["ROI_Pct"]],
    edgecolor="black",
    linewidth=0.5
)
axes[1].set_title(
    "Return on Investment by Block (%)",
    fontweight="bold"
)
axes[1].set_xlabel("ROI (%)")
axes[1].axvline(
    x=combined["ROI_Pct"].mean(),
    color="red", linestyle="--",
    label=f"Average: {combined['ROI_Pct'].mean():.1f}%"
)
axes[1].legend()

for i, (_, row) in enumerate(combined.iterrows()):
    axes[1].text(
        row["ROI_Pct"] + 1, i,
        f"{row['ROI_Pct']:.1f}%",
        va="center", fontsize=9
    )

plt.suptitle(
    "Field Financial Performance Dashboard",
    fontsize=14, fontweight="bold", y=1.02
)
plt.tight_layout()
plt.savefig(
    "block_profitability_dashboard.png",
    dpi=150, bbox_inches="tight"
)
plt.show()
print("Dashboard saved.")