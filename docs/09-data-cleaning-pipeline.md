# Data Cleaning Pipeline
## Overview
The Data Cleaning Pipeline project demonstrates how Python, Pandas, and NumPy can be used to identify and correct common data-quality problems before a dataset is used for analysis.
The project uses a deliberately messy petroleum well dataset containing duplicate records, missing values, inconsistent text formatting, incorrect data types, and impossible values.
The pipeline follows a structured process:
**Raw Data → Diagnose → Clean → Handle Missing Values → Validate → Ready for Analysis**
---
## Project Objective
The objective of this project is to build a systematic data-cleaning workflow that can transform an inconsistent dataset into a cleaner and validated dataset suitable for further analysis.
The project focuses on practical data-quality problems that can occur when working with petroleum production data.
---
## Dataset
The sample dataset contains information about:
- Well Name
- Production
- Water Cut
- Location
- Days Active
The original dataset contains 10 records.
### Deliberate Data-Quality Problems
The dataset includes:
- Duplicate rows
- Missing well names
- Missing production values
- Missing water-cut values
- Production stored as a string in one record
- Negative production
- Water cut greater than 1.0
- Inconsistent well-name capitalization
- Inconsistent location capitalization
- Leading and trailing spaces in location values
These problems were intentionally included to demonstrate the cleaning process.
---
## Step 1: Diagnose the Dataset
Before changing the data, the program performs a data-quality assessment.
It checks:
- Dataset shape
- Data types
- Missing values
- Duplicate rows
- Negative production values
- Impossible water-cut values
- Unique location values
This diagnostic stage is important because data should be understood before it is modified.
---
## Step 2: Remove Duplicate Records
Duplicate rows are identified and removed using:
```python
df_clean = df_clean.drop_duplicates()

This prevents the same record from being counted more than once during later analysis.

Step 3: Correct Data Types

Production values are converted to numeric format using:

pd.to_numeric(
    df_clean["Production"],
    errors="coerce"
)

Invalid values are converted to missing values (NaN) so that they can be handled systematically.

⸻

Step 4: Standardise Text Data

The pipeline standardises location values by:

1. Removing leading and trailing spaces.
2. Standardising capitalization.

It also standardises well names using title case.

For example, inconsistent location values such as:

Southern Block 
northern block
 Eastern Block

are converted into a consistent format.

⸻

Step 5: Handle Impossible Values

The pipeline identifies values that are not physically or logically valid for the dataset.

Negative Production

Negative production is treated as invalid:

df_clean.loc[
    df_clean["Production"] < 0,
    "Production"
] = np.nan

Invalid Water Cut

Water cut should fall between 0 and 1.

Values greater than 1.0 are therefore treated as invalid:

df_clean.loc[
    df_clean["Water_Cut"] > 1.0,
    "Water_Cut"
] = np.nan

⸻

Step 6: Handle Missing Values

Missing well names are removed because a well cannot be reliably analysed without an identifying name.

For missing Production values, the pipeline uses the median production of the remaining records.

For missing Water Cut values, it uses the median water cut.

Median imputation was selected because the median is generally less sensitive to extreme values than the mean.

⸻

Step 7: Validate the Cleaned Dataset

After cleaning, the program performs automated validation checks using Python assert statements.

It verifies that:

* No duplicate rows remain.
* Production is numeric.
* No negative production values remain.
* Water-cut values are valid.
* No well names are missing.

The program only reports:

ALL VALIDATION CHECKS PASSED

when all required checks succeed.

This provides an automated quality-control stage before analysis.

⸻

Data-Cleaning Workflow

The complete workflow can be summarised as:

Messy Dataset
      ↓
Diagnose Data Quality
      ↓
Remove Duplicates
      ↓
Fix Data Types
      ↓
Standardise Text
      ↓
Identify Invalid Values
      ↓
Handle Missing Values
      ↓
Run Validation Checks
      ↓
Clean Dataset
      ↓
Ready for Analysis

⸻

Technologies Used

* Python
* Pandas
* NumPy

⸻

Skills Demonstrated

This project demonstrates practical skills in:

* Data cleaning
* Data quality assessment
* Pandas DataFrames
* Missing-value handling
* Duplicate detection
* Data-type conversion
* Text standardisation
* Outlier/invalid-value handling
* Median imputation
* Data validation
* Automated quality checks
* Preparing datasets for analysis

⸻

Petroleum Industry Relevance

Data quality is important when working with production and operational datasets.

Before data can be used for analysis, reporting, forecasting, or machine-learning workflows, problems such as missing values, inconsistent formats, duplicate records, and invalid measurements need to be identified and addressed.

This project demonstrates a basic but important part of a petroleum data workflow: making sure the data is trustworthy enough to analyse.

⸻

Current Limitations

This project uses a small manually created sample dataset for demonstration.

The cleaning rules are also specifically designed for this dataset.

For a larger production environment, the pipeline could be expanded to include:

* Configurable validation rules
* Automated data-quality reports
* Logging of every cleaning action
* Handling of extreme but potentially valid production values
* Date and time validation
* Schema validation
* Larger CSV/database inputs
* Automated testing
* Data-quality dashboards

⸻

Future Improvements

Future versions could include:

* Reading data directly from CSV or SQL databases
* A reusable cleaning function
* Automated before-and-after quality reports
* Configurable thresholds for production and water cut
* Detailed cleaning logs
* Data visualisations
* Integration with machine-learning pipelines
* Automated data-quality monitoring

⸻

Project Files

Python Source Code:
https://github.com/mensahhayford/python-project/blob/main/data_cleaning_pipeline.py

Main portfolio:
https://github.com/mensahhayford/python-project


Conclusion

The Data Cleaning Pipeline demonstrates how Python can be used to move from a messy petroleum dataset toward a cleaner, validated dataset.

The project reinforces an important principle in data science:

Good analysis starts with good data.

Before building reports, models, or making decisions from data, the underlying dataset needs to be examined, cleaned, and validated.