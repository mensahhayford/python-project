# Petroleum Field Production Analyser
## Overview
The Petroleum Field Production Analyser is a Python-based tool designed to analyse production performance across multiple wells in a petroleum field.
The program stores production data together with basic well information such as location and production type. It then calculates production indicators, classifies wells according to their average output, identifies their best and worst production days, and generates both individual well reports and an overall field summary.
## Project Objective
The objective of this project is to demonstrate how Python can be used to transform structured well-production data into useful performance information.
The analyser focuses on:
- Individual well performance
- Production consistency
- Well performance classification
- Best and worst production days
- Total production
- Field-level performance comparison
## Dataset
The project contains production data for four sample wells:
| Well | Location | Type |
|---|---|---|
| Well Alpha | Northern Block | Oil |
| Well Beta | Southern Block | Oil |
| Well Gamma | Northern Block | Gas condensate |
| Well Delta | Eastern Block | Oil |
Each well contains 10 daily production measurements.
## Well Performance Results
### Well Alpha
- Average daily production: **501.5 bbl**
- Total production: **5,015 bbl**
- Best day: **Day 5 — 530 bbl**
- Worst day: **Day 6 — 470 bbl**
- Production range: **60 bbl**
- Classification: **SOLID PERFORMER**
### Well Beta
- Average daily production: **304.5 bbl**
- Total production: **3,045 bbl**
- Best day: **Day 3 — 320 bbl**
- Worst day: **Day 4 — 285 bbl**
- Production range: **35 bbl**
- Classification: **AVERAGE PERFORMER**
### Well Gamma
- Average daily production: **741.5 bbl**
- Total production: **7,415 bbl**
- Best day: **Day 3 — 780 bbl**
- Worst day: **Day 4 — 710 bbl**
- Production range: **70 bbl**
- Classification: **HIGH PERFORMER**
### Well Delta
- Average daily production: **178.5 bbl**
- Total production: **1,785 bbl**
- Best day: **Day 7 — 195 bbl**
- Worst day: **Day 8 — 160 bbl**
- Production range: **35 bbl**
- Classification: **UNDERPERFORMER — review required**
## Field Summary
Across all four wells, the analyser calculates:
- Total field production: **17,260 bbl over 10 days**
- Wells analysed: **4**
- Best performing well: **Well Gamma**
- Most consistent wells based on the smallest production range: **Well Beta and Well Delta**
- Average production per well over 10 days: **4,315 bbl**
The program identifies Well Gamma as the highest-performing well based on average daily production.
## Key Features
### 1. Well Performance Analysis
The program calculates the average production for each well and uses this value to classify its performance.
The classification thresholds are:
- **700 bbl/day or more:** HIGH PERFORMER
- **450–699.9 bbl/day:** SOLID PERFORMER
- **250–449.9 bbl/day:** AVERAGE PERFORMER
- **Below 250 bbl/day:** UNDERPERFORMER — review required
### 2. Production Consistency
The program calculates the difference between the highest and lowest daily production values.
This production range is used as a simple measure of consistency:
- Smaller range = more consistent production
- Larger range = greater variation in production
The program flags a well when its production range is greater than 100 bbl.
### 3. Best and Worst Production Days
For every well, the analyser identifies:
- The highest production value
- The day on which it occurred
- The lowest production value
- The day on which it occurred
### 4. Individual Well Reports
The `generate_well_report()` function produces a detailed report containing:
- Well name
- Location
- Production type
- Performance classification
- Average daily production
- Total production
- Best production day
- Worst production day
- Production range
- Consistency warning
### 5. Field Summary Report
The `generate_field_summary()` function provides a field-level overview by calculating:
- Total field production
- Number of wells analysed
- Best-performing well
- Most consistent well
- Average production per well
## Basic Workflow
```text
Well Production Data
        ↓
Python Dictionary
        ↓
Analysis Functions
        ↓
┌──────────────────────────────┐
│ Average Production           │
│ Production Range             │
│ Performance Classification   │
│ Best Production Day          │
│ Worst Production Day         │
└──────────────────────────────┘
        ↓
Individual Well Reports
        ↓
Field Summary Report
        ↓
Performance Insights

Technologies and Python Concepts Used

* Python
* Dictionaries
* Lists
* Functions
* Conditional statements
* for loops
* sum()
* max()
* min()
* List indexing
* String formatting
* Structured data
* Automated report generation

Skills Demonstrated

This project demonstrates practical ability to:

* Structure multi-dimensional petroleum production data
* Create reusable analysis functions
* Calculate production performance indicators
* Classify wells using defined thresholds
* Compare well performance
* Identify production extremes
* Generate automated individual well reports
* Produce field-level summaries
* Apply Python programming to a petroleum-related problem

Petroleum Industry Relevance

Production engineers and petroleum data analysts work with well and field production data to understand performance, identify changes in output, compare wells, and support operational decision-making.

This project provides a simplified example of that workflow using Python.

The dataset is intentionally small and structured for learning purposes, but the analytical framework can be extended to larger production datasets containing more wells, longer production histories, and additional production variables.

Current Limitations

The current version is a learning-focused prototype and has some limitations:

* The dataset is manually entered into the Python program.
* The analysis covers only 10 days of production.
* The production consistency measure is a simple maximum-minus-minimum range rather than statistical variance.
* Performance classifications use fixed thresholds.
* Reports are printed to the terminal rather than exported to a file or dashboard.
* The current script generates the Well Alpha report once before the main analysis function and again during the full analysis, resulting in duplicate Alpha output.

These limitations provide opportunities for further development.

Future Improvements

Potential improvements include:

* Reading production data from CSV files
* Using Pandas for larger datasets
* Adding production trend visualizations
* Exporting reports to CSV, Excel, or PDF
* Adding statistical measures such as standard deviation
* Creating interactive dashboards
* Adding production decline analysis
* Adding water-cut analysis
* Adding more advanced well-performance indicators
* Connecting the analysis to a database
* Adding automated alerts for unusual production behaviour

Project Files

Python Source Code; https://github.com/mensahhayford/python-project/blob/main/field_production_analyser_six.py

Conclusion

The Petroleum Field Production Analyser demonstrates how Python can be used to move beyond simple calculations and build a structured workflow for analysing multiple petroleum wells.

The project combines data structures, reusable functions, conditional logic, automated reporting, and petroleum-domain thinking to produce both individual well insights and a field-level summary.