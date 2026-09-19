import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("well_data.csv")

# ═══════════════════════════════════
# CHART 1: BAR CHART
# Production comparison across wells
# ═══════════════════════════════════

plt.figure(figsize=(10, 6))

# Create bars
bars = plt.bar(
    df["Well_Name"],
    df["Avg_Daily_Barrels"],
    color=["#2196F3" if status == "Active"
           else "#FF5722" if status == "Review needed"
           else "#9E9E9E"
           for status in df["Status"]],
    edgecolor="black",
    linewidth=0.5
)

# Labels and title
plt.title("Daily Production by Well\n(Blue=Active, Orange=Review, Grey=Inactive)",
          fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Well Name", fontsize=12)
plt.ylabel("Average Daily Production (Barrels)", fontsize=12)

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 10,
        f"{int(height):,}",
        ha="center",
        va="bottom",
        fontsize=10
    )

# Rotate x-axis labels for readability
plt.xticks(rotation=45, ha="right")

# Add a horizontal line showing field average
field_avg = df["Avg_Daily_Barrels"].mean()
plt.axhline(y=field_avg,
            color="green",
            linestyle="--",
            linewidth=1.5,
            label=f"Field Average: {field_avg:.0f} bbl/day")

plt.legend()
plt.tight_layout()
plt.savefig("chart_production_by_well.png",
            dpi=150, bbox_inches="tight")
plt.show()
print("Chart 1 saved.")

# ═══════════════════════════════════
# CHART 2: HORIZONTAL BAR CHART
# Water cut by well — ranked by risk
# ═══════════════════════════════════

# Sort by water cut — highest risk first
df_sorted = df.sort_values("Water_Cut",
                           ascending=True)

plt.figure(figsize=(10, 6))

# Colour code by water cut severity
colors = []
for wc in df_sorted["Water_Cut"]:
    if wc >= 0.50:
        colors.append("#F44336")  # Red — critical
    elif wc >= 0.30:
        colors.append("#FF9800")  # Orange — concern
    else:
        colors.append("#4CAF50")  # Green — acceptable

bars = plt.barh(
    df_sorted["Well_Name"],
    df_sorted["Water_Cut"] * 100,
    color=colors,
    edgecolor="black",
    linewidth=0.5
)

# Add percentage labels
for bar, wc in zip(bars, df_sorted["Water_Cut"]):
    plt.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{wc*100:.0f}%",
        va="center",
        fontsize=10
    )

# Add threshold lines
plt.axvline(x=30, color="orange",
            linestyle="--", linewidth=1.5,
            label="Concern threshold (30%)")
plt.axvline(x=50, color="red",
            linestyle="--", linewidth=1.5,
            label="Critical threshold (50%)")

plt.title("Water Cut Analysis by Well\n"
          "Green=Acceptable, Orange=Concern, Red=Critical",
          fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Water Cut (%)", fontsize=12)
plt.ylabel("Well Name", fontsize=12)
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("chart_water_cut_analysis.png",
            dpi=150, bbox_inches="tight")
plt.show()
print("Chart 2 saved.")
# ═══════════════════════════════════
# CHART 3: SCATTER PLOT
# ═══════════════════════════════════

plt.figure(figsize=(10, 8))

# Plot each well as a point
for _, row in df.iterrows():
    
    size = row["Days_Producing"] / 2

    
    if row["Status"] == "Active":
        color = "#2196F3"
    elif row["Status"] == "Review needed":
        color = "#FF9800"
    else:
        color = "#9E9E9E"

    plt.scatter(
        row["Water_Cut"] * 100,
        row["Avg_Daily_Barrels"],
        s=size,
        color=color,
        alpha=0.7,
        edgecolors="black",
        linewidth=0.5
    )

    # Label each point with well name
    plt.annotate(
        row["Well_Name"],
        (row["Water_Cut"] * 100,
         row["Avg_Daily_Barrels"]),
        textcoords="offset points",
        xytext=(8, 4),
        fontsize=9
    )

# Add threshold lines
plt.axvline(x=40, color="red",
            linestyle="--", alpha=0.5,
            label="High water cut threshold (40%)")
plt.axhline(y=400, color="green",
            linestyle="--", alpha=0.5,
            label="High production threshold (400 bbl)")

plt.title("Production vs Water Cut\n"
          "Ideal wells: high production, low water cut (top-left)",
          fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Water Cut (%)", fontsize=12)
plt.ylabel("Average Daily Production (Barrels)", fontsize=12)
plt.legend()

# Add quadrant labels
plt.text(5, 850,
         "IDEAL\n(High prod, low water)",
         fontsize=9, color="green",
         alpha=0.7)
plt.text(55, 850,
         "CONCERN\n(High prod, high water)",
         fontsize=9, color="orange",
         alpha=0.7)
plt.text(5, 50,
         "MONITOR\n(Low prod, low water)",
         fontsize=9, color="blue",
         alpha=0.7)
plt.text(55, 50,
         "REVIEW\n(Low prod, high water)",
         fontsize=9, color="red",
         alpha=0.7)

plt.tight_layout()
plt.savefig("chart_production_vs_watercut.png",
            dpi=150, bbox_inches="tight")
plt.show()
print("Chart 3 saved.")