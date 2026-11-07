import sqlite3
import pandas as pd
from pathlib import Path

# 1. DATABASE CONFIGURATION

DATABASE_NAME = "petroleum_field.db"
OUTPUT_FOLDER = Path("project18_outputs")

OUTPUT_FOLDER.mkdir(exist_ok=True)

conn = sqlite3.connect(DATABASE_NAME)

# Enable foreign-key enforcement
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

print("=" * 65)
print("PETROLEUM FIELD DATABASE AND ANALYSIS SYSTEM")
print("=" * 65)

print("\nDatabase connected successfully.")
print("SQLite version:", sqlite3.sqlite_version)

# 2. CREATE DATABASE TABLES

cursor.execute("""
    CREATE TABLE IF NOT EXISTS blocks (
        block_id INTEGER PRIMARY KEY,
        block_name TEXT NOT NULL,
        region TEXT,
        operator TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS wells (
        well_id INTEGER PRIMARY KEY,
        well_name TEXT NOT NULL,
        block_id INTEGER,
        well_type TEXT,
        spud_date TEXT,
        total_depth_m REAL,
        status TEXT,

        FOREIGN KEY (block_id)
        REFERENCES blocks(block_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS production (
        record_id INTEGER PRIMARY KEY,
        well_id INTEGER NOT NULL,
        record_date TEXT NOT NULL,
        oil_bbl REAL NOT NULL CHECK (oil_bbl >= 0),
        water_bbl REAL NOT NULL CHECK (water_bbl >= 0),
        gas_mcf REAL NOT NULL CHECK (gas_mcf >= 0),

        FOREIGN KEY (well_id)
        REFERENCES wells(well_id)
    )
""")

conn.commit()

print("\nDatabase tables verified or created:")
print("- blocks")
print("- wells")
print("- production")

# 3. CREATE DATABASE INDEXES

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_wells_block
    ON wells(block_id)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_production_well
    ON production(well_id)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_production_date
    ON production(record_date)
""")

conn.commit()

print("\nDatabase indexes created or verified.")


# 4. INSERT SYNTHETIC PETROLEUM DATA

blocks_data = [
    (1, "Northern Block", "Onshore North", "PetroAlpha Ltd"),
    (2, "Southern Block", "Offshore South", "DeepSea Corp"),
    (3, "Eastern Block", "Onshore East", "PetroAlpha Ltd"),
    (4, "Western Block", "Onshore West", "Atlantic E&P")
]

wells_data = [
    (1, "Well_Alpha", 1, "Oil", "2019-03-15", 3200, "Active"),
    (2, "Well_Beta", 2, "Oil", "2020-07-22", 4100, "Active"),
    (3, "Well_Gamma", 1, "Gas Condensate", "2018-11-01", 3800, "Active"),
    (4, "Well_Delta", 3, "Oil", "2021-02-10", 2900, "Review"),
    (5, "Well_Epsilon", 2, "Oil", "2020-09-14", 4300, "Active"),
    (6, "Well_Zeta", 3, "Gas Condensate", "2022-01-05", 3100, "Active"),
    (7, "Well_Eta", 1, "Oil", "2018-06-30", 3600, "Active"),
    (8, "Well_Theta", 4, "Oil", "2023-04-18", 2700, "Inactive")
]

production_data = [
    (1, 1, "2024-01-01", 520, 92, 15.2),
    (2, 1, "2024-01-02", 510, 95, 14.8),
    (3, 2, "2024-01-01", 303, 84, 0.0),
    (4, 2, "2024-01-02", 298, 87, 0.0),
    (5, 3, "2024-01-01", 742, 64, 210.5),
    (6, 3, "2024-01-02", 755, 61, 214.2),
    (7, 4, "2024-01-01", 179, 148, 5.1),
    (8, 4, "2024-01-02", 165, 156, 4.8),
    (9, 5, "2024-01-01", 634, 139, 0.0),
    (10, 5, "2024-01-02", 628, 142, 0.0),
    (11, 6, "2024-01-01", 289, 117, 88.3),
    (12, 7, "2024-01-01", 891, 109, 22.1),
    (13, 7, "2024-01-02", 878, 112, 21.9),
    (14, 8, "2024-01-01", 0, 0, 0.0)
]


cursor.executemany("""
    INSERT OR IGNORE INTO blocks
    (block_id, block_name, region, operator)
    VALUES (?, ?, ?, ?)
""", blocks_data)

cursor.executemany("""
    INSERT OR IGNORE INTO wells
    (well_id, well_name, block_id, well_type,
     spud_date, total_depth_m, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", wells_data)

cursor.executemany("""
    INSERT OR IGNORE INTO production
    (record_id, well_id, record_date,
     oil_bbl, water_bbl, gas_mcf)
    VALUES (?, ?, ?, ?, ?, ?)
""", production_data)

conn.commit()

print("\nSample data inserted or already present.")

print(f"Sample blocks: {len(blocks_data)}")
print(f"Sample wells: {len(wells_data)}")
print(f"Sample production records: {len(production_data)}")

def run_query(title, query, params=None, decimals=None):
    """Execute a SQL query and display its Pandas result."""

    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    if decimals is not None:
        result = result.round(decimals)

    if result.empty:
        print("No records found.")
    else:
        print(result.to_string(index=False))

    return result


#  QUERY 1: RETRIEVE ALL WELLS

all_wells = run_query(
    "QUERY 1: ALL REGISTERED WELLS",
    """
    SELECT *
    FROM wells
    ORDER BY well_id
    """
)


# QUERY 2: FILTER ACTIVE WELLS

active_wells = run_query(
    "QUERY 2: ACTIVE WELLS",
    """
    SELECT
        well_name,
        well_type,
        total_depth_m,
        status
    FROM wells
    WHERE status = 'Active'
    ORDER BY total_depth_m DESC
    """
)


# QUERY 3: PRODUCTION AGGREGATE ANALYSIS

production_summary = run_query(
    "QUERY 3: OVERALL PRODUCTION SUMMARY",
    """
    SELECT
        COUNT(*) AS total_records,

        ROUND(SUM(oil_bbl), 2)
            AS total_oil_bbl,

        ROUND(AVG(oil_bbl), 2)
            AS average_oil_bbl,

        ROUND(MAX(oil_bbl), 2)
            AS peak_oil_bbl,

        ROUND(MIN(oil_bbl), 2)
            AS lowest_oil_bbl,

        ROUND(SUM(water_bbl), 2)
            AS total_water_bbl,

        ROUND(SUM(gas_mcf), 2)
            AS total_gas_mcf

    FROM production
    """
)


# QUERY 4: PRODUCTION PERFORMANCE BY WELL

well_performance = run_query(
    "QUERY 4: PRODUCTION PERFORMANCE BY WELL",
    """
    SELECT
        w.well_name,
        w.well_type,
        w.status,

        COUNT(p.record_id)
            AS days_recorded,

        ROUND(SUM(p.oil_bbl), 2)
            AS total_oil_bbl,

        ROUND(AVG(p.oil_bbl), 2)
            AS average_daily_oil,

        ROUND(SUM(p.water_bbl), 2)
            AS total_water_bbl,

        ROUND(SUM(p.gas_mcf), 2)
            AS total_gas_mcf

    FROM wells w

    LEFT JOIN production p
        ON w.well_id = p.well_id

    GROUP BY
        w.well_id,
        w.well_name,
        w.well_type,
        w.status

    ORDER BY total_oil_bbl DESC
    """
)


# QUERY 5: WELLS WITH BLOCK INFORMATION
well_block_details = run_query(
    "QUERY 5: WELLS WITH BLOCK AND OPERATOR DETAILS",
    """
    SELECT
        w.well_name,
        b.block_name,
        b.operator,
        b.region,
        w.well_type,
        w.status,

        ROUND(AVG(p.oil_bbl), 2)
            AS average_daily_oil,

        ROUND(SUM(p.oil_bbl), 2)
            AS total_oil

    FROM wells w

    INNER JOIN blocks b
        ON w.block_id = b.block_id

    LEFT JOIN production p
        ON w.well_id = p.well_id

    GROUP BY
        w.well_id,
        w.well_name,
        b.block_name,
        b.operator,
        b.region,
        w.well_type,
        w.status

    ORDER BY total_oil DESC
    """
)

# QUERY 6: BLOCK-LEVEL PRODUCTION ANALYSIS

block_performance = run_query(
    "QUERY 6: PETROLEUM BLOCK PERFORMANCE",
    """
    SELECT
        b.block_name,
        b.operator,

        COUNT(DISTINCT w.well_id)
            AS total_wells,

        COUNT(p.record_id)
            AS production_records,

        ROUND(SUM(p.oil_bbl), 2)
            AS total_oil_bbl,

        ROUND(SUM(p.water_bbl), 2)
            AS total_water_bbl,

        ROUND(SUM(p.gas_mcf), 2)
            AS total_gas_mcf,

        ROUND(
            SUM(p.oil_bbl) /
            NULLIF(COUNT(DISTINCT w.well_id), 0),
            2
        ) AS oil_per_registered_well

    FROM blocks b

    LEFT JOIN wells w
        ON b.block_id = w.block_id

    LEFT JOIN production p
        ON w.well_id = p.well_id

    GROUP BY
        b.block_id,
        b.block_name,
        b.operator

    ORDER BY total_oil_bbl DESC
    """
)

# QUERY 7: HAVING - HIGH-PRODUCTION BLOCKS

high_production_blocks = run_query(
    "QUERY 7: BLOCKS WITH AVERAGE DAILY OIL ABOVE 300 BBL",
    """
    SELECT
        b.block_name,
        b.operator,

        ROUND(AVG(p.oil_bbl), 2)
            AS average_daily_oil,

        COUNT(DISTINCT w.well_id)
            AS well_count

    FROM blocks b

    INNER JOIN wells w
        ON b.block_id = w.block_id

    INNER JOIN production p
        ON w.well_id = p.well_id

    GROUP BY
        b.block_id,
        b.block_name,
        b.operator

    HAVING AVG(p.oil_bbl) > 300

    ORDER BY average_daily_oil DESC
    """
)


# QUERY 8: WATER-CUT ANALYSIS

water_cut_analysis = run_query(
    "QUERY 8: WATER-CUT ANALYSIS BY WELL",
    """
    SELECT
        w.well_name,
        w.status,

        ROUND(SUM(p.oil_bbl), 2)
            AS total_oil,

        ROUND(SUM(p.water_bbl), 2)
            AS total_water,

        ROUND(
            100.0 * SUM(p.water_bbl) /
            NULLIF(
                SUM(p.oil_bbl + p.water_bbl),
                0
            ),
            2
        ) AS water_cut_pct,

        CASE

            WHEN SUM(p.oil_bbl + p.water_bbl) = 0
                THEN 'NO LIQUID PRODUCTION'

            WHEN
                1.0 * SUM(p.water_bbl) /
                NULLIF(
                    SUM(p.oil_bbl + p.water_bbl),
                    0
                ) > 0.50
                THEN 'CRITICAL'

            WHEN
                1.0 * SUM(p.water_bbl) /
                NULLIF(
                    SUM(p.oil_bbl + p.water_bbl),
                    0
                ) > 0.30
                THEN 'HIGH'

            ELSE 'ACCEPTABLE'

        END AS water_cut_status

    FROM wells w

    LEFT JOIN production p
        ON w.well_id = p.well_id

    GROUP BY
        w.well_id,
        w.well_name,
        w.status

    ORDER BY water_cut_pct DESC
    """
)


# QUERY 9: OPERATOR PERFORMANCE

operator_performance = run_query(
    "QUERY 9: OPERATOR PRODUCTION PERFORMANCE",
    """
    SELECT
        b.operator,

        COUNT(DISTINCT w.well_id)
            AS total_wells,

        ROUND(SUM(p.oil_bbl), 2)
            AS total_oil_bbl,

        ROUND(SUM(p.water_bbl), 2)
            AS total_water_bbl,

        ROUND(SUM(p.gas_mcf), 2)
            AS total_gas_mcf,

        ROUND(AVG(p.oil_bbl), 2)
            AS average_recorded_oil

    FROM blocks b

    INNER JOIN wells w
        ON b.block_id = w.block_id

    LEFT JOIN production p
        ON w.well_id = p.well_id

    GROUP BY b.operator

    ORDER BY total_oil_bbl DESC
    """
)


# QUERY 10: WELL RANKING

well_ranking = run_query(
    "QUERY 10: WELL PRODUCTION RANKING",
    """
    SELECT
        w.well_name,

        ROUND(SUM(p.oil_bbl), 2)
            AS total_oil_bbl,

        RANK() OVER (
            ORDER BY SUM(p.oil_bbl) DESC
        ) AS production_rank

    FROM wells w

    LEFT JOIN production p
        ON w.well_id = p.well_id

    GROUP BY
        w.well_id,
        w.well_name

    ORDER BY production_rank
    """
)


# DATA QUALITY VALIDATION

print("\n" + "=" * 65)
print("DATA QUALITY VALIDATION")
print("=" * 65)


# Check 1: Negative production

negative_production = run_query(
    "CHECK 1: NEGATIVE PRODUCTION VALUES",
    """
    SELECT *
    FROM production
    WHERE oil_bbl < 0
       OR water_bbl < 0
       OR gas_mcf < 0
    """
)


# Check 2: Missing production values

missing_production = run_query(
    "CHECK 2: MISSING PRODUCTION VALUES",
    """
    SELECT *
    FROM production
    WHERE well_id IS NULL
       OR record_date IS NULL
       OR oil_bbl IS NULL
       OR water_bbl IS NULL
       OR gas_mcf IS NULL
    """
)


# Check 3: Orphan production records

orphan_records = run_query(
    "CHECK 3: PRODUCTION RECORDS WITHOUT MATCHING WELLS",
    """
    SELECT p.*
    FROM production p

    LEFT JOIN wells w
        ON p.well_id = w.well_id

    WHERE w.well_id IS NULL
    """
)


# Check 4: Wells without a valid block

orphan_wells = run_query(
    "CHECK 4: WELLS WITHOUT MATCHING BLOCKS",
    """
    SELECT w.*
    FROM wells w

    LEFT JOIN blocks b
        ON w.block_id = b.block_id

    WHERE b.block_id IS NULL
    """
)


# Check 5: Duplicate well-date production records

duplicate_records = run_query(
    "CHECK 5: DUPLICATE WELL-DATE RECORDS",
    """
    SELECT
        well_id,
        record_date,
        COUNT(*) AS duplicate_count

    FROM production

    GROUP BY well_id, record_date

    HAVING COUNT(*) > 1
    """
)


# Check 6: Wells without production records

wells_without_production = run_query(
    "CHECK 6: WELLS WITHOUT PRODUCTION RECORDS",
    """
    SELECT
        w.well_id,
        w.well_name,
        w.status

    FROM wells w

    LEFT JOIN production p
        ON w.well_id = p.well_id

    WHERE p.record_id IS NULL
    """
)


database_summary = run_query(
    "DATABASE SUMMARY",
    """
    SELECT
        (SELECT COUNT(*) FROM blocks)
            AS total_blocks,

        (SELECT COUNT(*) FROM wells)
            AS total_wells,

        (SELECT COUNT(*) FROM production)
            AS total_production_records,

        (SELECT ROUND(SUM(oil_bbl), 2)
         FROM production)
            AS total_oil_bbl,

        (SELECT ROUND(SUM(water_bbl), 2)
         FROM production)
            AS total_water_bbl,

        (SELECT ROUND(SUM(gas_mcf), 2)
         FROM production)
            AS total_gas_mcf
    """
)


# EXPORT ANALYTICAL RESULTS

print("\n" + "=" * 65)
print("EXPORTING ANALYTICAL RESULTS")
print("=" * 65)


reports = {
    "all_wells": all_wells,
    "active_wells": active_wells,
    "production_summary": production_summary,
    "well_performance": well_performance,
    "well_block_details": well_block_details,
    "block_performance": block_performance,
    "high_production_blocks": high_production_blocks,
    "water_cut_analysis": water_cut_analysis,
    "operator_performance": operator_performance,
    "well_ranking": well_ranking,
    "negative_production": negative_production,
    "missing_production": missing_production,
    "orphan_records": orphan_records,
    "orphan_wells": orphan_wells,
    "duplicate_records": duplicate_records,
    "wells_without_production": wells_without_production,
    "database_summary": database_summary
}

for report_name, dataframe in reports.items():

    output_path = OUTPUT_FOLDER / f"{report_name}.csv"

    dataframe.to_csv(
        output_path,
        index=False
    )

    print(f"Saved: {output_path}")


# GENERATE A TEXT SUMMARY REPORT

report_path = OUTPUT_FOLDER / "petroleum_database_report.txt"

with open(report_path, "w", encoding="utf-8") as report:

    report.write("=" * 65 + "\n")
    report.write("PETROLEUM FIELD DATABASE ANALYSIS REPORT\n")
    report.write("=" * 65 + "\n\n")

    for report_name, dataframe in reports.items():

        report.write("\n" + "=" * 65 + "\n")
        report.write(report_name.upper().replace("_", " ") + "\n")
        report.write("=" * 65 + "\n")

        if dataframe.empty:
            report.write("No records found.\n")
        else:
            report.write(
                dataframe.to_string(index=False)
            )

        report.write("\n")


print("\nText report saved:", report_path)


# FINAL DATABASE VALIDATION

foreign_key_check = cursor.execute(
    "PRAGMA foreign_key_check"
).fetchall()

print("\n" + "=" * 65)
print("FINAL DATABASE VALIDATION")
print("=" * 65)

if foreign_key_check:
    print("Foreign-key violations detected:")
    print(foreign_key_check)
else:
    print("Foreign-key validation passed.")

print("\nDatabase file:", DATABASE_NAME)
print("Output folder:", OUTPUT_FOLDER)


# CLOSE DATABASE CONNECTION

conn.close()

print("\nDatabase connection closed successfully.")

print("\n" + "=" * 65)
print("PROJECT 18 EXECUTION COMPLETED")
print("=" * 65)