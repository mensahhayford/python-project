Project 17: Petroleum Production Time Series Analysis and Statistical Process Control

Overview

This project demonstrates how Python can be used to analyse petroleum well production behaviour over time.

It implements an automated production time-series workflow using three years of synthetic daily production data. The analysis examines production trends, moving averages, production changes, cumulative production, and unusual operating observations.

The project also generates an automated analytical report, a visual dashboard, and a processed dataset.

Project Objectives

* Analyse daily petroleum production trends.
* Calculate 7-day, 30-day, and 90-day moving averages.
* Examine recent production percentage changes.
* Identify unusual production observations using rolling statistical limits.
* Calculate cumulative production.
* Estimate illustrative gross revenue.
* Generate automated analytical reports and dashboards.

Analytical Workflow

1. Synthetic Data Generation

Generates 1,095 daily production observations representing three years of simulated well production.

The dataset incorporates:

* Natural exponential production decline.
* Seasonal production variation.
* Simulated workover-related production improvements.
* Simulated equipment-related production disruptions.
* Random operational noise.

2. Data Validation

Checks the production dataset for:

* Required columns.
* Valid date index.
* Duplicate dates.
* Missing production values.
* Invalid negative production measurements.

3. Moving Average Analysis

Calculates:

* 7-day moving average.
* 30-day moving average.
* 90-day moving average.

These indicators help smooth daily fluctuations and reveal underlying production trends.

4. Production Change Analysis

Calculates the percentage change in the 30-day average production over a specified comparison period.

Negative values indicate a reduction in production, while positive values indicate an increase.

This is a rolling percentage-change indicator, not a fitted reservoir decline-curve model.

5. Exploratory Anomaly Detection

Uses rolling means and standard deviations to identify observations outside exploratory statistical limits.

Observations exceeding the selected threshold are flagged for further investigation.

These statistical flags do not automatically establish equipment failure or represent validated engineering control limits.

6. Cumulative Production Analysis

Calculates cumulative production by summing daily production volumes.

This provides an overview of the well’s total production over the analysis period.

7. Financial Estimation

Calculates illustrative gross revenue using an assumed oil price of $72.50 per barrel.

The estimate excludes operating expenses, royalties, taxes, transportation costs, and other financial deductions.

8. Automated Reporting and Visualisation

Generates:

* A text-based production analysis report.
* A four-chart production dashboard.
* A processed CSV dataset.

Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Datetime
* Statistical analysis
* Rolling-window calculations
* Time-series analysis

How to Run the Project

Install the required libraries:

pip install pandas numpy matplotlib

Run the Python script:

python production_time_series_analysis.py

The program creates a project17_outputs directory containing the generated report, dashboard, and processed dataset.

Key Performance Indicators

The project evaluates:

* Total cumulative production.
* Average daily production.
* Peak daily production.
* Latest 30-day average production.
* Production percentage change.
* Production volatility.
* Number of statistically flagged observations.
* Estimated gross revenue.

Demonstration Results

The supplied synthetic-data run produced the following illustrative results:

Indicator	Result
Analysis duration	1,095 days
Total production	811,798.7 barrels
Average daily production	741.37 bbl/day
Peak 30-day average	805.74 bbl/day
Latest 30-day average	695.52 bbl/day
Latest 30-observation change	+4.15%
Flagged observations	31
Estimated gross revenue	$58,855,405.75

Results are dependent on the generated dataset and analysis configuration.

Limitations and Assumptions

* The production dataset is synthetic and does not represent actual petroleum field measurements.
* Workovers, seasonal effects, and equipment disruptions are simulated.
* Production percentage changes are not substitutes for engineering decline-curve analysis.
* Rolling statistical anomaly limits are exploratory and are not validated formal SPC control limits.
* Anomalies require further investigation before being attributed to operational failures.
* Financial estimates use a simplified oil-price assumption and should not be interpreted as profit or actual field revenue.

Future Improvements

Potential extensions include:

* Applying formal Statistical Process Control methods.
* Developing production forecasting models.
* Implementing change-point detection.
* Analysing multiple wells simultaneously.
* Integrating real-world petroleum production datasets.
* Incorporating pressure, water cut, and operating conditions.
* Developing interactive production monitoring dashboards.

Conclusion

This project demonstrates how time-series analysis and statistical techniques can be applied to petroleum production monitoring.

It provides a foundation for investigating production behaviour, identifying unusual observations, and developing more advanced data-driven production surveillance systems.