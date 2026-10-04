# CSV Field Analysis with Pandas GroupBy
## Overview
The CSV Field Analysis project is a Python and Pandas-based tool for analysing structured petroleum well-production data stored in a CSV file.
The program loads the dataset, examines its structure, analyses active wells, evaluates water-cut levels, compares production across field blocks, and generates a field-level production summary.
This project demonstrates how tabular petroleum data can be transformed into useful operational insights using Python and Pandas.
## Project Objective
The main objective is to demonstrate practical data analysis using a structured well dataset.
The analysis focuses on:
- Well production performance
- Active well production
- Water-cut levels
- Wells requiring attention
- Production performance by field block
- Overall field production
- Well-status distribution
## Dataset
The project uses a CSV dataset named `well_data.csv`.
The dataset contains eight wells with the following fields:
| Column | Description |
|---|---|
| Well_Name | Name of the well |
| Location | Field block where the well is located |
| Type | Production type |
| Avg_Daily_Barrels | Average daily production |
| Days_Producing | Number of producing days |
| Water_Cut | Water cut as a decimal proportion |
| Status | Current well status |
## Dataset Summary
The dataset contains:
- **8 wells**
- **4 active wells**
- **2 wells requiring review**
- **1 inactive well**
## Production Analysis
The program filters the dataset to identify active wells and calculates their combined production.
### Active Wells
| Well | Average Daily Production |
|---|---:|
| Well_Alpha | 520 bbl/day |
| Well_Beta | 303 bbl/day |
| Well_Gamma | 742 bbl/day |
| Well_Epsilon | 634 bbl/day |
### Active Production
The combined production from active wells is:
**2,199 bbl/day**
## Water Cut Analysis
Water cut is analysed to identify wells that may require additional attention.
The program sorts wells from highest to lowest water cut.
The highest water-cut wells are:
| Well | Water Cut | Status |
|---|---:|---|
| Well_Theta | 67% | Inactive |
| Well_Delta | 45% | Review needed |
| Well_Zeta | 35% | Review needed |
| Well_Beta | 22% | Active |
### High Water-Cut Wells
The program flags wells with water cut greater than 40%.
The identified wells are:
- **Well_Theta — 67%**
- **Well_Delta — 45%**
These wells are therefore highlighted by the analysis as requiring attention based on the project's defined threshold.
## Performance by Field Block
The project uses Pandas `groupby()` to compare production performance across field locations.
### Northern Block
- Total production: **2,153 bbl/day**
- Average production per well: **717.67 bbl/day**
- Wells: **3**
- Average water cut: **11.33%**
### Southern Block
- Total production: **937 bbl/day**
- Average production per well: **468.50 bbl/day**
- Wells: **2**
- Average water cut: **20%**
### Eastern Block
- Total production: **468 bbl/day**
- Average production per well: **234.00 bbl/day**
- Wells: **2**
- Average water cut: **40%**
### Western Block
- Total production: **156 bbl/day**
- Average production per well: **156.00 bbl/day**
- Wells: **1**
- Average water cut: **67%**
The Northern Block has the highest total production and the highest average production per well in this dataset.
## Field Production Summary
The program generates an overall field production report.
### Results
- Total wells: **8**
- Active wells: **4**
- Under review: **2**
- Inactive: **1**
- Total daily field output: **3,714 bbl/day**
- Best-performing well: **Well_Eta**
- Highest water-cut well: **Well_Theta**
Well_Eta has the highest average daily production at:
**891 bbl/day**
Well_Theta has the highest water cut at:
**67%**
## Key Pandas Operations Used
### Reading the CSV
The project uses:
```python
pd.read_csv("well_data.csv")

to load the structured dataset into a Pandas DataFrame.

Filtering

Active wells are identified using:

df[df["Status"] == "Active"]

This demonstrates conditional filtering of rows.

Sorting

The dataset is sorted by water cut using:

df.sort_values("Water_Cut", ascending=False)

This places the highest water-cut wells first.

GroupBy Analysis

The project uses Pandas groupby() with agg() to calculate block-level production statistics:

df.groupby("Location").agg(
    Total_Production=("Avg_Daily_Barrels", "sum"),
    Average_Production=("Avg_Daily_Barrels", "mean"),
    Well_Count=("Well_Name", "count"),
    Avg_Water_Cut=("Water_Cut", "mean")
)

This allows multiple performance indicators to be calculated for each field block.

Basic Workflow

well_data.csv
      ↓
Pandas DataFrame
      ↓
Data Inspection
      ↓
Filtering & Sorting
      ↓
Production Analysis
      ↓
Water Cut Analysis
      ↓
GroupBy Block Analysis
      ↓
Field Production Summary
      ↓
Operational Insights

Technologies Used

* Python
* Pandas
* CSV
* DataFrames
* Data filtering
* Data sorting
* GroupBy
* Aggregation
* Statistical summaries

Skills Demonstrated

This project demonstrates practical ability to:

* Load structured data from CSV files
* Work with Pandas DataFrames
* Inspect datasets
* Filter rows based on conditions
* Sort data by analytical variables
* Calculate aggregate production metrics
* Group wells by field location
* Compare production performance
* Analyse water-cut levels
* Identify wells requiring attention
* Generate automated field summaries

Petroleum Industry Relevance

Production and petroleum data teams frequently work with structured well datasets containing production rates, water cut, well status, field location, and other operational variables.

This project demonstrates a simplified version of that workflow.

By combining production and water-cut information, analysts can compare wells and field blocks and identify areas that may warrant further investigation.

The dataset is a structured learning dataset rather than a live operational field dataset.

Current Limitations

The current version has several limitations:

* The dataset is small, containing only eight wells.
* The data is static and stored in a CSV file.
* Water-cut thresholds are manually defined in the code.
* The analysis does not include production trends over time.
* No visual dashboard is currently included.
* No statistical anomaly detection is implemented.
* The program does not automatically export its results.

Future Improvements

Potential improvements include:

* Adding larger production datasets
* Reading data from databases
* Adding production trend analysis
* Creating production and water-cut visualizations
* Building an interactive dashboard
* Adding automated anomaly detection
* Adding decline-curve analysis
* Creating automated Excel or PDF reports
* Adding more production variables
* Connecting the analysis to real-time or regularly updated datasets

Project Files

Python Source Code⁠; https://github.com/mensahhayford/python-project/blob/main/csv_field_analysis.py

CSV Dataset⁠; https://github.com/mensahhayford/python-project/blob/main/well_data.csv

Main Portfolio Repository⁠; https://github.com/mensahhayford/python-project⁠￼

Conclusion

The CSV Field Analysis project demonstrates how Python and Pandas can be used to analyse structured petroleum production data.

The project progresses beyond basic Python calculations by introducing DataFrames, filtering, sorting, aggregation, and groupby() analysis.

It provides a foundation for more advanced petroleum data-analysis workflows involving larger datasets, visualization, statistical analysis, databases, and machine learning.