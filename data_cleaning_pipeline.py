import pandas as pd
import numpy as np

# sample messy dataset

messy_data = {
    "Well_Name": ["Well_Alpha", "well_alpha",
                  "Well_Beta", "Well_Beta",
                  "WELL_GAMMA", "Well_Delta",
                  "Well_Epsilon", None,
                  "Well_Zeta", "Well_Eta"],

    "Production": [520, 520, 303, 303,
                   742, "179", None, 634,
                   289, -50],
    # Problems: duplicate rows, string where
    # number expected, missing value,
    # impossible negative value

    "Water_Cut": [0.15, 0.15, 0.22, 0.22,
                  0.08, 0.45, 0.18, None,
                  1.35, 0.11],
    # Problems: duplicates, missing,
    # impossible value over 1.0

    "Location": ["Northern Block",
                 "Northern Block",
                 "Southern Block ",
                 "Southern Block",
                 "northern block",
                 "Eastern Block",
                 "Southern Block",
                 "Eastern Block",
                 " Eastern Block",
                 "Northern Block"],
    # Problems: trailing spaces,
    # inconsistent capitalisation

    "Days_Active": [365, 365, 280, 280,
                    410, 190, 320, 245,
                    245, 400]
}

df_messy = pd.DataFrame(messy_data)

print("=== RAW MESSY DATA ===")
print(df_messy)
print(f"\nShape: {df_messy.shape}")
print(f"\nData types:\n{df_messy.dtypes}")
print(f"\nMissing values:\n{df_messy.isnull().sum()}")

# ═══════════════════════════════════
# STEP 1: DIAGNOSE BEFORE CLEANING

print("=== DATA QUALITY REPORT ===\n")

# Check missing values
print("Missing values per column:")
print(df_messy.isnull().sum())
print(f"Total missing: {df_messy.isnull().sum().sum()}")

# Check duplicate rows
print(f"\nDuplicate rows: {df_messy.duplicated().sum()}")
print("Duplicate entries:")
print(df_messy[df_messy.duplicated(keep=False)])

# Check data types
print(f"\nData types:")
print(df_messy.dtypes)

# Check for impossible values
print(f"\nNegative production values:")

numeric_prod = pd.to_numeric(
    df_messy["Production"], errors="coerce"
)
print(df_messy[numeric_prod < 0])

print(f"\nWater cut above 1.0 (impossible):")
print(df_messy[df_messy["Water_Cut"] > 1.0])

# Check inconsistent text values
print(f"\nUnique location values (should be consistent):")
print(df_messy["Location"].unique())

# ═══════════════════════════════════
# STEP 2: CLEAN SYSTEMATICALLY
# ═══════════════════════════════════

df_clean = df_messy.copy()

# ── CLEAN 1: Remove duplicate rows ──
df_clean = df_clean.drop_duplicates()
print(f"After removing duplicates: "
      f"{len(df_clean)} rows")

# ── CLEAN 2: Fix data types ──
df_clean["Production"] = pd.to_numeric(
    df_clean["Production"],
    errors="coerce"
)
print(f"\nProduction dtype after fix: "
      f"{df_clean['Production'].dtype}")

# ── CLEAN 3: Fix text inconsistencies ──
df_clean["Location"] = (
    df_clean["Location"].str.strip()
)

# Standardise capitalisation
df_clean["Location"] = (
    df_clean["Location"].str.title()
)

# Standardise Well_Name capitalisation
df_clean["Well_Name"] = (
    df_clean["Well_Name"].str.title()
)

print(f"\nUnique locations after fix:")
print(df_clean["Location"].unique())

# ── CLEAN 4: Handle impossible values ──
df_clean.loc[
    df_clean["Production"] < 0,
    "Production"
] = np.nan
print(f"\nNegative production replaced with NaN")

# Water cut must be between 0 and 1
df_clean.loc[
    df_clean["Water_Cut"] > 1.0,
    "Water_Cut"
] = np.nan
print(f"Impossible water cut replaced with NaN")

# ── CLEAN 5: Handle missing values ──
print(f"\nMissing values before handling:")
print(df_clean.isnull().sum())

# Drop rows where Well_Name is missing
# (can't analyse an unnamed well)
df_clean = df_clean.dropna(
    subset=["Well_Name"]
)

# Fill missing Production with
# median production
# (Better than mean — less affected
# by outliers in small datasets)
median_prod = df_clean["Production"].median()
df_clean["Production"] = (
    df_clean["Production"].fillna(median_prod)
)

# Fill missing Water_Cut with
# median water cut
median_wc = df_clean["Water_Cut"].median()
df_clean["Water_Cut"] = (
    df_clean["Water_Cut"].fillna(median_wc)
)

print(f"\nMissing values after handling:")
print(df_clean.isnull().sum())

# ── FINAL CHECK ──
print("\n=== CLEANED DATASET ===")
print(df_clean)
print(f"\nFinal shape: {df_clean.shape}")
print(f"Data types:\n{df_clean.dtypes}")

# ═══════════════════════════════════
# STEP 3: VALIDATE THE CLEAN DATA
# ═══════════════════════════════════

print("=== VALIDATION REPORT ===\n")


assert df_clean.duplicated().sum() == 0, \
    "Duplicates still exist!"
print("✓ No duplicate rows")


assert df_clean["Production"].dtype in \
    ["float64", "int64"], \
    "Production is not numeric!"
print("✓ Production is numeric")


assert (df_clean["Production"] >= 0).all(), \
    "Negative production values exist!"
print("✓ No negative production values")

assert (df_clean["Water_Cut"] <= 1.0).all(), \
    "Impossible water cut values exist!"
print("✓ All water cut values valid")


assert df_clean["Well_Name"].isnull().sum() == 0, \
    "Missing well names!"
print("✓ No missing well names")

print("\n=== ALL VALIDATION CHECKS PASSED ===")
print("Data is ready for analysis.\n")


print("=== CLEAN DATA SUMMARY ===")
print(df_clean.describe().round(2))