# Pandas Well Analysis
## Overview
The Pandas Well Analysis project demonstrates how Python and Pandas can be used to create, explore, filter, transform, sort, and analyse structured petroleum well data.
Unlike the previous CSV-based project, this program creates the dataset directly inside Python as a Pandas DataFrame.
The project focuses on developing practical DataFrame skills while applying them to a petroleum production scenario.
## Project Objective
The objective of this project is to demonstrate how Pandas can be used to:
- Create a DataFrame from structured data
- Explore a dataset
- Select specific columns
- Filter rows using conditions
- Apply multiple filtering conditions
- Create calculated columns
- Calculate summary statistics
- Sort data by production performance
- Identify wells requiring review
## Dataset
The project contains information for four sample wells.
| Well | Location | Type | Avg. Daily Production | Days Producing | Status |
|---|---|---|---:|---:|---|
| Well Alpha | Northern Block | Oil | 502 bbl/day | 365 | Active |
| Well Beta | Southern Block | Oil | 303 bbl/day | 280 | Active |
| Well Gamma | Northern Block | Gas condensate | 742 bbl/day | 410 | Active |
| Well Delta | Eastern Block | Oil | 179 bbl/day | 190 | Review needed |
The original DataFrame contains **4 rows and 6 columns**.
## DataFrame Exploration
The project uses several Pandas methods to understand the dataset.
### First rows
The `head()` method is used to display the first three records:
```python
df.head(3)

Dataset shape

The project checks the number of rows and columns using:

df.shape

Result:

* Rows: 4
* Columns: 6

Column names

The program retrieves the column names using:

df.columns.tolist()

Data types

The dtypes attribute is used to inspect the data types of the DataFrame columns.

Statistical summary

The project also uses:

df.describe()

to generate descriptive statistics for the numerical columns.

Selecting Data

The project demonstrates both single-column and multi-column selection.

Single column

df["Well_Name"]

returns the well names as a Pandas Series.

Multiple columns

df[["Well_Name", "Avg_Daily_Barrels"]]

returns a DataFrame containing the selected columns.

Filtering Wells

The project demonstrates conditional filtering.

High-Producing Wells

Wells producing more than 400 bbl/day are identified using:

df[df["Avg_Daily_Barrels"] > 400]

The result is:

* Well Alpha — 502 bbl/day
* Well Gamma — 742 bbl/day

Oil Wells

The program filters for wells where the production type is Oil:

df[df["Type"] == "Oil"]

This identifies:

* Well Alpha
* Well Beta
* Well Delta

Northern Block Wells

The program filters wells located in the Northern Block:

df[df["Location"] == "Northern Block"]

This identifies:

* Well Alpha
* Well Gamma

High-Producing Oil Wells

The project combines two conditions:

(df["Type"] == "Oil") &
(df["Avg_Daily_Barrels"] > 200)

The resulting wells are:

* Well Alpha — 502 bbl/day
* Well Beta — 303 bbl/day

This demonstrates how multiple conditions can be combined in Pandas.

Calculated Production

The project creates a new column called Total_Production.

The calculation is:

df["Total_Production"] = (
    df["Avg_Daily_Barrels"] *
    df["Days_Producing"]
)

This estimates total production from the average daily production rate and the number of producing days recorded for each well.

Calculated Results

Well	Avg. Daily Production	Days Producing	Calculated Production
Well Alpha	502 bbl/day	365	183,230 bbl
Well Beta	303 bbl/day	280	84,840 bbl
Well Gamma	742 bbl/day	410	304,220 bbl
Well Delta	179 bbl/day	190	34,010 bbl

Total Calculated Field Production

The combined calculated production is:

606,300 barrels

Field Summary

The project calculates several overall field indicators.

Average Daily Production per Well

The average of the four daily production rates is:

431.5 bbl/day per well

Best Performing Well

The program uses idxmax() to identify the well with the highest average daily production.

The result is:

Well Gamma — 742 bbl/day

Wells Requiring Review

The program counts wells with the status:

"Review needed"

Result:

1 well — Well Delta

Production Ranking

The project sorts wells from highest to lowest average daily production using:

df.sort_values(
    "Avg_Daily_Barrels",
    ascending=False
)

The resulting ranking is:

Rank	Well	Average Daily Production	Status
1	Well Gamma	742 bbl/day	Active
2	Well Alpha	502 bbl/day	Active
3	Well Beta	303 bbl/day	Active
4	Well Delta	179 bbl/day	Review needed

Basic Workflow

Structured Well Data
        ↓
Create Pandas DataFrame
        ↓
Explore Dataset
        ↓
Select Columns
        ↓
Filter Wells
        ↓
Create Calculated Column
        ↓
Calculate Field Summary
        ↓
Sort Production
        ↓
Performance Insights

Technologies Used

* Python
* Pandas
* DataFrames
* Lists
* Dictionaries
* Conditional filtering
* Boolean logic
* Data transformation
* Aggregation
* Sorting
* Statistical summaries

Skills Demonstrated

This project demonstrates practical ability to:

* Create Pandas DataFrames
* Explore structured datasets
* Select individual and multiple columns
* Filter data using conditions
* Combine multiple conditions
* Create calculated columns
* Perform aggregate calculations
* Identify maximum values with idxmax()
* Count records matching conditions
* Sort data for performance ranking
* Interpret structured petroleum data

Petroleum Industry Relevance

Petroleum data analysts frequently work with structured information about wells, production rates, production days, locations, production types, and operational status.

This project provides a simplified example of using Pandas to transform well-level information into useful production indicators and rankings.

The dataset is a learning dataset created within the Python program rather than live operational field data.

Current Limitations

The current version has several limitations:

* The dataset contains only four sample wells.
* The data is manually defined inside the Python script.
* Production is represented using average daily rates rather than a time-series production history.
* The calculated total production assumes the average daily rate applies across all recorded producing days.
* No water-cut analysis is included.
* No production visualization is included.
* Results are printed to the terminal rather than exported.

Future Improvements

Potential improvements include:

* Loading data from CSV or Excel files
* Adding water-cut analysis
* Adding production trend analysis
* Creating charts and dashboards
* Adding statistical measures
* Exporting analysis results to Excel or PDF
* Connecting the DataFrame to a database
* Adding production decline analysis
* Analysing larger well datasets
* Integrating machine-learning workflows

Project Files

Python Source Code⁠; https://github.com/mensahhayford/python-project/blob/main/pandas_well_analysis_eight.py

Main Portfolio Repository⁠; https://github.com/mensahhayford/python-project⁠￼

Conclusion

The Pandas Well Analysis project demonstrates the transition from basic Python data structures toward practical tabular data analysis using Pandas.

The project covers core DataFrame operations including creation, exploration, selection, filtering, calculated columns, aggregation, and sorting.

These skills provide an important foundation for more advanced petroleum data-analysis, visualization, database, and machine-learning projects