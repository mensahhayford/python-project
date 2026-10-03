# Well Production Analysis with Python
## Overview
This project is a Python-based analysis tool for examining daily oil production from multiple wells.
The program takes a set of daily production values and calculates useful production statistics for each well. It demonstrates how basic Python programming can be applied to a petroleum production-data problem.
## Project Objective
The objective is to transform daily production figures into simple indicators that can help describe well performance.
For each well, the program calculates:
- Average daily production
- Best production day
- Worst production day
- Total production over the 10-day period
## Dataset
The project uses production data for three sample wells:
- Well A
- Well B
- Well C
Each value represents the number of barrels of oil produced by a well on a particular day.
The dataset contains 10 days of production for each well.
## Key Results
### Well A
- Average daily production: 501.5 barrels/day
- Best production day: 530 barrels
- Worst production day: 470 barrels
- Total production: 5,015 barrels
### Well B
- Average daily production: 304.5 barrels/day
- Best production day: 320 barrels
- Worst production day: 285 barrels
- Total production: 3,045 barrels
### Well C
- Average daily production: 741.5 barrels/day
- Best production day: 780 barrels
- Worst production day: 710 barrels
- Total production: 7,415 barrels
## How the Program Works
The production data is stored using a Python dictionary, with each well associated with a list of daily production values.
The program uses separate functions to calculate:
1. Average production
2. Maximum production
3. Minimum production
4. Total production
It then loops through each well and generates a production report.
### Basic Workflow
```text
Daily Well Production Data
          ↓
     Python Dictionary
          ↓
   Analysis Functions
          ↓
 ┌────────┼─────────┐
 ↓        ↓         ↓
Average  Best     Worst
Output   Day       Day
          ↓
     Total Production
          ↓
    Production Report

Technologies and Concepts Used

* Python
* Dictionaries
* Lists
* Functions
* For loops
* sum()
* max()
* min()
* Basic statistical calculations
* Structured production data
* Automated reporting

Skills Demonstrated

This project demonstrates practical ability to:

* Structure production data in Python
* Create reusable functions
* Perform basic production calculations
* Automate repetitive analysis
* Convert raw production figures into useful performance indicators
* Generate a simple production report

Petroleum Industry Relevance

Production engineers and analysts regularly work with production measurements to understand how wells are performing over time.

Although this project uses a small sample dataset, the same basic analytical approach can be extended to larger production datasets containing many wells and longer production periods.

Future Improvements

Possible improvements include:

* Reading production data from CSV files
* Analysing larger datasets
* Adding production trend visualizations
* Comparing wells automatically
* Adding decline analysis
* Including water-cut analysis
* Adding additional production indicators
* Developing an interactive dashboard

Project Files

Python Source Code⁠￼

Main Portfolio Repository⁠￼

Conclusion

This project demonstrates how Python can be used to turn basic daily well-production data into meaningful production statistics.

It provides a foundation for more advanced petroleum data-analysis workflows involving larger datasets, visualization, production trends, and machine learning.