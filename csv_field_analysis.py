import pandas as pd


df = pd.read_csv("well_data.csv")

print("=== DATA LOADED SUCCESSFULLY ===")
print(f"Shape: {df.shape[0]} wells, "
      f"{df.shape[1]} columns\n")

# First look at the data
print("=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== COLUMN INFORMATION ===")
print(df.info())

print("\n=== STATISTICAL SUMMARY ===")
print(df.describe().round(2))

# ═══════════════════════════════════
# PRODUCTION ANALYSIS
# ═══════════════════════════════════

print("\n=== ACTIVE WELLS ONLY ===")
active = df[df["Status"] == "Active"]
print(active[["Well_Name", "Avg_Daily_Barrels",
              "Water_Cut"]])

print(f"\nActive wells: {len(active)}")
print(f"Total active production: "
      f"{active['Avg_Daily_Barrels'].sum():,} bbl/day")

# ═══════════════════════════════════
# WATER CUT ANALYSIS
# ═══════════════════════════════════

print("\n=== WATER CUT ANALYSIS ===")

# Sort by water cut — highest risk first
water_concern = df.sort_values("Water_Cut",
                               ascending=False)
print(water_concern[["Well_Name",
                      "Water_Cut",
                      "Status"]])

# Flag high water cut wells
high_water = df[df["Water_Cut"] > 0.40]
print(f"\nWells with >40% water cut "
      f"(requiring attention):")
print(high_water[["Well_Name",
                   "Water_Cut",
                   "Avg_Daily_Barrels",
                   "Status"]])

# ═══════════════════════════════════
# BLOCK PERFORMANCE
# Group wells by location block
# ═══════════════════════════════════

print("\n=== PERFORMANCE BY BLOCK ===")
block_summary = df.groupby("Location").agg(
    Total_Production=("Avg_Daily_Barrels", "sum"),
    Average_Production=("Avg_Daily_Barrels", "mean"),
    Well_Count=("Well_Name", "count"),
    Avg_Water_Cut=("Water_Cut", "mean")
).round(2)

print(block_summary)

# ═══════════════════════════════════
# TOTAL FIELD PRODUCTION REPORT
# ═══════════════════════════════════

print("\n" + "="*45)
print("  FIELD PRODUCTION SUMMARY REPORT")
print("="*45)
print(f"  Total wells        : {len(df)}")
print(f"  Active wells       : "
      f"{len(df[df['Status']=='Active'])}")
print(f"  Under review       : "
      f"{len(df[df['Status']=='Review needed'])}")
print(f"  Inactive           : "
      f"{len(df[df['Status']=='Inactive'])}")
print(f"  Total daily output : "
      f"{df['Avg_Daily_Barrels'].sum():,} bbl")
print(f"  Best performing    : "
      f"{df.loc[df['Avg_Daily_Barrels'].idxmax(),'Well_Name']}")
print(f"  Highest water cut  : "
      f"{df.loc[df['Water_Cut'].idxmax(),'Well_Name']}")
print("="*45)