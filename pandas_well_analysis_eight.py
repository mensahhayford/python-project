
import pandas as pd

# ═══════════════════════════════════
# CREATING MY FIRST DATAFRAME
# ═══════════════════════════════════

# Method 1: Create from a dictionary
well_data = {
    "Well_Name": ["Well_Alpha", "Well_Beta",
                  "Well_Gamma", "Well_Delta"],
    "Location": ["Northern Block", "Southern Block",
                 "Northern Block", "Eastern Block"],
    "Type": ["Oil", "Oil",
             "Gas condensate", "Oil"],
    "Avg_Daily_Barrels": [502, 303, 742, 179],
    "Days_Producing": [365, 280, 410, 190],
    "Status": ["Active", "Active",
               "Active", "Review needed"]
}

df = pd.DataFrame(well_data)

# ═══════════════════════════════════
# EXPLORING DATAFRAME
# ═══════════════════════════════════

print("=== FULL DATASET ===")
print(df)

print("\n=== FIRST 3 ROWS ===")
print(df.head(3))

print("\n=== DATASET SHAPE ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== BASIC STATISTICS ===")
print(df.describe())

# ═══════════════════════════════════
# SELECTING SPECIFIC COLUMNS
# ═══════════════════════════════════

# Single column — returns a Series
print("=== WELL NAMES ===")
print(df["Well_Name"])

# Multiple columns — returns a DataFrame
print("\n=== NAME AND PRODUCTION ===")
print(df[["Well_Name", "Avg_Daily_Barrels"]])

# ═══════════════════════════════════
# FILTERING ROWS BY CONDITION
# ═══════════════════════════════════

# Wells producing above 400 barrels/day
high_producers = df[df["Avg_Daily_Barrels"] > 400]
print("\n=== HIGH PRODUCING WELLS ===")
print(high_producers)

# Oil wells only
oil_wells = df[df["Type"] == "Oil"]
print("\n=== OIL WELLS ONLY ===")
print(oil_wells)

# Northern Block wells
northern = df[df["Location"] == "Northern Block"]
print("\n=== NORTHERN BLOCK ===")
print(northern)

# Combined filter: Oil AND high production
high_oil = df[
    (df["Type"] == "Oil") &
    (df["Avg_Daily_Barrels"] > 200)
]
print("\n=== HIGH PRODUCING OIL WELLS ===")
print(high_oil)

# ═══════════════════════════════════
# ADDING CALCULATED COLUMNS
# ═══════════════════════════════════

# Calculate total production per well
df["Total_Production"] = (df["Avg_Daily_Barrels"]
                          * df["Days_Producing"])

print("=== WITH TOTAL PRODUCTION ===")
print(df[["Well_Name", "Avg_Daily_Barrels",
          "Days_Producing", "Total_Production"]])

# ═══════════════════════════════════
# SUMMARY STATISTICS
# ═══════════════════════════════════

print("\n=== FIELD SUMMARY ===")
print(f"Total field production: "
      f"{df['Total_Production'].sum():,} barrels")
print(f"Average daily per well: "
      f"{df['Avg_Daily_Barrels'].mean():.1f} bbl")
print(f"Best performing well: "
      f"{df.loc[df['Avg_Daily_Barrels'].idxmax(), 'Well_Name']}")
print(f"Wells requiring review: "
      f"{len(df[df['Status'] == 'Review needed'])}")

# ═══════════════════════════════════
# SORTING DATA
# ═══════════════════════════════════

# Sort by production — highest first
sorted_df = df.sort_values("Avg_Daily_Barrels",
                           ascending=False)
print("\n=== WELLS BY PRODUCTION RANKING ===")
print(sorted_df[["Well_Name",
                  "Avg_Daily_Barrels",
                  "Status"]])