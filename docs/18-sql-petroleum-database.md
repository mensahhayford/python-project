Project 18: Petroleum Field SQL Database and Production Analysis System

1. Project Overview

This project demonstrates the application of relational database management and SQL-based data analysis to petroleum field operations.

Using Python, SQLite, and Pandas, I developed a petroleum database system that organises information about petroleum blocks, wells, and daily production records.

The system uses SQL queries to retrieve, filter, aggregate, join, rank, and analyse petroleum production data. It also incorporates data-quality checks and automated reporting to support structured production surveillance and operational analysis.

The project demonstrates how relational databases can transform raw petroleum operational records into organised, accessible, and useful analytical information.

Dataset: Synthetic petroleum field data created for demonstration and learning purposes.

2. Project Objectives

The main objectives were to:

* Design a relational database for petroleum field information.
* Establish relationships between petroleum blocks, wells, and production records.
* Use SQL to retrieve and manipulate petroleum data.
* Analyse production performance at well, block, and operator levels.
* Calculate water cut directly through SQL.
* Apply conditional classifications using SQL CASE statements.
* Rank wells according to recorded oil production.
* Perform basic database and data-quality validation.
* Export analytical results into CSV files and an automated text report.

3. Database Architecture

The database consists of three related tables.

A. Blocks Table

Stores information about petroleum blocks and their operators.

Field	Description
block_id	Unique block identifier
block_name	Name of the petroleum block
region	Geographic or operational region
operator	Company responsible for the block

B. Wells Table

Stores information about individual wells.

Field	Description
well_id	Unique well identifier
well_name	Name of the well
block_id	Associated petroleum block
well_type	Oil or gas condensate
spud_date	Date drilling commenced
total_depth_m	Total measured well depth in metres
status	Operational status

C. Production Table

Stores daily production records.

Field	Description
record_id	Unique production record identifier
well_id	Associated well
record_date	Production record date
oil_bbl	Oil production in barrels
water_bbl	Water production in barrels
gas_mcf	Gas production in thousand cubic feet

Database Relationships

The database uses primary and foreign keys to establish relationships:

* One block can contain multiple wells.
* One well can have multiple production records.
* Each well belongs to a petroleum block.
* Each production record is associated with a well.

These relationships support relational queries across multiple levels of petroleum field information.

4. Technologies and Tools

Technology	Application
Python	Main programming language
SQLite	Relational database management
SQL	Database queries and analytical operations
Pandas	Query results and data handling
pathlib	File and output directory management

5. Database Engineering Features

Database Creation

The system creates three relational tables using SQLite.

It uses CREATE TABLE IF NOT EXISTS to avoid automatically dropping existing tables during subsequent executions.

Referential Integrity

Foreign-key enforcement is enabled through:

PRAGMA foreign_keys = ON

This helps ensure that wells reference valid blocks and production records reference valid wells.

Database Indexing

Indexes are created on:

* wells.block_id
* production.well_id
* production.record_date

These indexes support common relationship and date-based queries.

Safe Sample Data Insertion

The system uses parameterised SQL statements and INSERT OR IGNORE to insert its demonstration records without repeatedly inserting rows with existing primary keys.

6. SQL Analytical Operations

The project implements ten principal analytical queries.

Query 1: Retrieve All Wells

Uses SELECT to retrieve registered well information.

Query 2: Filter Active Wells

Uses WHERE and ORDER BY to identify active wells and arrange them by total depth.

Query 3: Production Summary

Uses aggregate functions:

* COUNT()
* SUM()
* AVG()
* MAX()
* MIN()

These functions summarise recorded oil, water, and gas production.

Query 4: Production Performance by Well

Uses LEFT JOIN and GROUP BY to calculate:

* Number of recorded production days.
* Total oil production.
* Average recorded daily oil production.
* Total water production.
* Total gas production.

Query 5: Well and Block Analysis

Uses relational joins to combine well information with block, operator, region, and production details.

Query 6: Block-Level Production Analysis

Aggregates production across petroleum blocks to examine total oil, water, and gas production.

It also calculates oil production per registered well.

Query 7: High-Production Block Identification

Uses HAVING to identify blocks whose average recorded oil production exceeds 300 barrels per production record.

Query 8: Water-Cut Analysis

Calculates water cut using:

Water Cut (%) = Water Production / (Oil Production + Water Production) × 100

SQL CASE statements classify the results as:

* CRITICAL: Water cut above 50%.
* HIGH: Water cut above 30% and up to 50%.
* ACCEPTABLE: Water cut at or below 30%.
* NO LIQUID PRODUCTION: No recorded oil or water production.

These are illustrative project thresholds, not universal petroleum engineering operating limits.

Query 9: Operator Performance

Aggregates recorded production by operator to compare their associated wells and production volumes.

Query 10: Well Production Ranking

Uses the SQL window function RANK() to rank wells according to total recorded oil production.

7. Data Quality and Validation

The project includes six database validation checks.

1. Negative production: Identifies negative oil, water, or gas values.
2. Missing production values: Identifies records with missing essential production fields.
3. Orphan production records: Identifies production records without matching wells.
4. Orphan wells: Identifies wells without matching petroleum blocks.
5. Duplicate well-date records: Identifies multiple production records for the same well and date.
6. Wells without production records: Identifies registered wells with no associated production history.

A final PRAGMA foreign_key_check verifies whether the database contains foreign-key violations.

These checks provide basic data-quality assurance before relying on the analytical results.

8. Automated Reporting and Output

The system uses Pandas to convert SQL query results into structured DataFrames.

It automatically creates a project18_outputs directory containing:

* CSV exports of the analytical query results.
* Production summaries.
* Well and block performance reports.
* Water-cut analysis.
* Operator performance reports.
* Data-quality validation results.
* A consolidated petroleum database text report.

The system generates 17 CSV report files and one consolidated text report.

9. How to Run the Project

Requirements

Install the required Python libraries:

pip install pandas

SQLite is included with Python’s standard library in typical Python installations.

Execute the Script

Run:

python sql_petroleum_queries.py

Expected Files

The project creates or uses:

petroleum_field.db

The generated reports are saved in:

project18_outputs/

The database is designed to preserve existing records when the script is run again. Sample rows with existing primary keys are ignored during insertion.

Important: CREATE TABLE IF NOT EXISTS does not migrate an existing table to a newer schema. Existing databases should be checked before relying on newly introduced constraints.

10. Key Learning Outcomes

Through this project, I strengthened my understanding of:

* Relational database design.
* Primary and foreign keys.
* Database integrity and indexing.
* SQL filtering and aggregation.
* One-to-many relationships.
* Inner and left joins.
* Grouping and conditional filtering.
* SQL window functions.
* Production engineering calculations.
* Database validation and reporting.
* Python integration with SQL databases.

11. Petroleum Industry Applications

The techniques demonstrated in this project can support several petroleum data management and analysis activities:

* Organising well and production records.
* Monitoring production performance across wells.
* Comparing production between petroleum blocks.
* Evaluating operator-level production summaries.
* Identifying wells with high water-cut values.
* Detecting missing, inconsistent, or duplicated records.
* Preparing structured reports for production surveillance.

In a real petroleum operation, the database could be extended to incorporate pressure measurements, reservoir properties, well interventions, completion information, downtime records, and historical production data.

12. Limitations and Future Improvements

Current Limitations

* The dataset is synthetic and does not represent actual field production.
* The database contains only a small number of wells and production records.
* The demonstration uses simplified well and block relationships.
* Water-cut thresholds are illustrative and should be adapted to field-specific engineering requirements.
* The current reporting system is based on SQL query outputs rather than a fully interactive dashboard.
* INSERT OR IGNORE prevents duplicate primary-key insertions but does not enforce uniqueness of every well-date combination.
* The existing database schema is not automatically migrated when the Python script is updated.

Future Improvements

Possible extensions include:

1. Integrating real petroleum production datasets.
2. Adding monthly and annual production summaries.
3. Incorporating pressure and reservoir performance data.
4. Adding well intervention and downtime tables.
5. Developing production decline analysis using SQL and Python.
6. Connecting the database to Power BI or an interactive Python dashboard.
7. Implementing automated database backup and migration procedures.
8. Developing more advanced data-quality rules and exception reporting.

13. Conclusion

Project 18 demonstrates how Python and SQL can be combined to build a structured petroleum database and perform practical production analysis.

By integrating relational database design, SQL queries, production calculations, data-quality validation, and automated reporting, the project provides a foundation for more advanced petroleum data management and analytical applications.

It represents another step in developing the technical skills required to apply data science and database technologies to petroleum engineering and operational decision-making