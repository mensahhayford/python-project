import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


np.random.seed(42)
months = np.arange(1, 25)

initial_rate = 1000 
decline_rate = 0.08 

true_production = (
    initial_rate * np.exp(-decline_rate * months)
)
noise = np.random.normal(0, 20, len(months))
actual_production = true_production + noise
actual_production = np.maximum(
    actual_production, 0
)

df_decline = pd.DataFrame({
    "Month": months,
    "Production_bbl_day": actual_production.round(1)
})

print("=== WELL PRODUCTION HISTORY ===")
print(df_decline.to_string())

# ═══════════════════════════════════
# STEP 1: VISUALISE
# ═══════════════════════════════════

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(
    df_decline["Month"],
    df_decline["Production_bbl_day"],
    color="#2196F3",
    alpha=0.7,
    label="Actual production"
)
axes[0].set_title(
    "Well Production Decline History",
    fontweight="bold"
)
axes[0].set_xlabel("Month")
axes[0].set_ylabel("Production (bbl/day)")
axes[0].legend()

# ═══════════════════════════════════
# STEP 2: PREPARE DATA FOR ML
# ═══════════════════════════════════

df_decline["Log_Production"] = np.log(
    df_decline["Production_bbl_day"]
)

print("\n=== WITH LOG TRANSFORMATION ===")
print(df_decline[
    ["Month", "Production_bbl_day",
     "Log_Production"]
].head(10).round(3))

# ═══════════════════════════════════
# STEP 3: BUILD MY FIRST ML MODEL
# ═══════════════════════════════════

n = len(df_decline)
x = df_decline["Month"].values
y = df_decline["Log_Production"].values

x_mean = x.mean()
y_mean = y.mean()

slope = (
    np.sum((x - x_mean) * (y - y_mean)) /
    np.sum((x - x_mean) ** 2)
)
intercept = y_mean - slope * x_mean

print(f"\n=== LINEAR REGRESSION RESULTS ===")
print(f"Intercept (log scale): {intercept:.4f}")
print(f"Slope (decline rate) : {slope:.4f}")
print(f"Initial rate estimate: "
      f"{np.exp(intercept):.1f} bbl/day")
print(f"Monthly decline rate : "
      f"{abs(slope)*100:.2f}%")

# ═══════════════════════════════════
# STEP 4: MAKE PREDICTIONS
# ═══════════════════════════════════

future_months = np.arange(25, 37)
predicted_log = intercept + slope * future_months
predicted_production = np.exp(predicted_log)

df_future = pd.DataFrame({
    "Month": future_months,
    "Predicted_Production": predicted_production.round(1)
})

print("\n=== 12-MONTH PRODUCTION FORECAST ===")
print(df_future.to_string())
print(f"\nEstimated production at Month 36: "
      f"{predicted_production[-1]:.1f} bbl/day")

# ═══════════════════════════════════
# STEP 5: VISUALISE THE MODEL
# ═══════════════════════════════════

all_months = np.arange(1, 37)
model_line = np.exp(intercept + slope * all_months)

axes[1].scatter(
    df_decline["Month"],
    df_decline["Production_bbl_day"],
    color="#2196F3",
    alpha=0.7,
    label="Historical data",
    zorder=5
)
axes[1].plot(
    all_months[:24],
    model_line[:24],
    color="#FF9800",
    linewidth=2,
    label="Fitted decline curve"
)
axes[1].plot(
    all_months[23:],
    model_line[23:],
    color="#F44336",
    linewidth=2,
    linestyle="--",
    label="12-month forecast"
)
axes[1].axvline(
    x=24.5,
    color="grey",
    linestyle=":",
    alpha=0.7
)
axes[1].text(
    25, model_line[24] * 1.05,
    "FORECAST →",
    color="#F44336",
    fontsize=9
)
axes[1].set_title(
    "Decline Curve Analysis with 12-Month Forecast",
    fontweight="bold"
)
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Production (bbl/day)")
axes[1].legend()

plt.suptitle(
    "Well Production Decline Analysis — ML Approach",
    fontsize=13,
    fontweight="bold",
    y=1.02
)
plt.tight_layout()
plt.savefig(
    "decline_curve_analysis.png",
    dpi=150,
    bbox_inches="tight"
)
plt.show()
print("\nDecline curve chart saved.")

print("\n" + "="*55)
print("  COMPLETE FIELD INTELLIGENCE SYSTEM")
print("  Day 14 Capstone — [Your Name]")
print("="*55)

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

def calculate_score(row):
    """
    Composite well performance score.
    High production + low water cut = high score.
    This is original analysis logic —
    not from any template.
    """
    prod_score = min(
        row["Avg_Daily_Barrels"] / 1000 * 60, 60
    )
    wc_score = (1 - row["Water_Cut"]) * 40
    return round(prod_score + wc_score, 1)

df["Performance_Score"] = df.apply(
    calculate_score, axis=1
)


def classify_risk(row):
    if row["Water_Cut"] > 0.50:
        return "CRITICAL"
    elif (row["Water_Cut"] > 0.30 or
          row["Avg_Daily_Barrels"] < 200):
        return "HIGH"
    elif row["Water_Cut"] > 0.15:
        return "MEDIUM"
    else:
        return "LOW"

df["Risk_Level"] = df.apply(classify_risk, axis=1)

def recommend_action(row):
    if row["Risk_Level"] == "CRITICAL":
        return "Immediate intervention required"
    elif row["Risk_Level"] == "HIGH":
        return "Schedule review within 30 days"
    elif row["Performance_Score"] > 70:
        return "Monitor — performing well"
    else:
        return "Optimisation study recommended"

df["Recommended_Action"] = df.apply(
    recommend_action, axis=1
)

print("\n=== WELL PERFORMANCE INTELLIGENCE ===\n")
display_cols = [
    "Well_Name", "Avg_Daily_Barrels",
    "Water_Cut", "Performance_Score",
    "Risk_Level", "Recommended_Action"
]

for _, row in df.sort_values(
    "Performance_Score", ascending=False
).iterrows():
    risk_symbol = {
        "LOW": "✓",
        "MEDIUM": "~",
        "HIGH": "⚠",
        "CRITICAL": "✗"
    }[row["Risk_Level"]]

    print(f"{risk_symbol} {row['Well_Name']}")
    print(f"  Score: {row['Performance_Score']}/100 "
          f"| Production: {row['Avg_Daily_Barrels']} bbl/d "
          f"| Water Cut: {row['Water_Cut']*100:.0f}%")
    print(f"  Action: {row['Recommended_Action']}\n")


print("=== BLOCK SUMMARY ===")
block_summary = df.groupby("Location").agg(
    Wells=("Well_Name", "count"),
    Avg_Score=("Performance_Score", "mean"),
    Total_Production=("Avg_Daily_Barrels", "sum"),
    High_Risk=("Risk_Level", lambda x:
               sum(x.isin(["HIGH", "CRITICAL"])))
).round(1)
print(block_summary.to_string())

print("\n" + "="*55)
print("  System built by: [Your Name]")
print("  Program: Petroleum Data Analytics")
print("  Day 14 of 14 — Foundation Complete")
print("="*55)