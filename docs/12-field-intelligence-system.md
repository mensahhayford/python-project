# Project 12 — Field Intelligence System
## Petroleum Data Science Portfolio — Capstone Project
### Overview
The **Field Intelligence System** is a Python-based petroleum data analytics capstone that combines production decline analysis, forecasting, well performance scoring, risk classification, recommended actions, and block-level intelligence into one analytical workflow.
The project demonstrates how Python can be used to move from raw production information toward structured operational insights.
The system contains two major analytical components:
1. **Production Decline Analysis and Forecasting**
2. **Well Performance and Field Intelligence Analysis**
The project was developed as a capstone exercise for a petroleum data analytics learning journey.
---
## Project Objective
The objective of this project is to demonstrate how multiple Python and data science techniques can be combined into a single petroleum-focused analytical system.
The system is designed to:
- Analyse historical well production behaviour
- Model production decline
- Forecast future production
- Score wells based on production and water cut
- Classify operational risk
- Recommend follow-up actions
- Compare performance across field blocks
- Identify high-risk wells
- Present analytical results in a structured format
- Visualise production decline and forecast trends
---
# Part 1 — Production Decline Analysis
## 1. Simulated Production History
The first component creates a 24-month production history using simulated data.
The model begins with an assumed initial production rate of:
**1,000 bbl/day**
and an assumed exponential decline rate of:
**8%**
The underlying production trend is generated using:
```python
initial_rate * np.exp(-decline_rate * months)

Random noise is then added to simulate variation in observed production.

A fixed random seed is used:

np.random.seed(42)

This ensures that the simulated dataset is reproducible.

Important note

This production history is simulated data, not measured production data from an actual field.

⸻

2. Production History

The system generates 24 monthly observations.

The simulated production begins at approximately:

933.1 bbl/day

at Month 1.

By Month 24, the simulated production is approximately:

118.1 bbl/day

The values include random variation around the underlying exponential decline trend.

⸻

3. Production Decline Visualisation

The first chart displays the simulated production history as a scatter plot.

The chart allows the production trend to be visually examined before modelling.

The project uses Matplotlib to create the visualisation.

⸻

4. Log Transformation

Because exponential decline can be represented as a linear relationship on a logarithmic scale, production is transformed using:

np.log(df_decline["Production_bbl_day"])

A new column is created:

Log_Production

This transformation allows the project to fit a linear regression relationship between:

* Month
* Logarithm of production

⸻

5. Manual Linear Regression

Instead of using a pre-built machine-learning regression library, the project calculates the linear regression coefficients directly using NumPy.

The calculation determines:

* Mean of the month values
* Mean of the log-production values
* Regression slope
* Regression intercept

The fitted relationship is:

Log(Production) = intercept + slope × Month

Calculated regression results

Intercept (log scale):

6.9365

Slope:

-0.0842

The negative slope represents the declining production trend.

The estimated initial rate from the fitted model is approximately:

1,029.2 bbl/day

The calculated monthly decline parameter is approximately:

8.42%

This is close to the 8% decline parameter used to generate the simulated underlying production.

⸻

6. Twelve-Month Production Forecast

The fitted model is then used to forecast production for Months 25–36.

The predicted production is calculated by converting the predicted logarithmic values back to the original production scale:

np.exp(predicted_log)

Forecast horizon

12 months

Estimated production at Month 36

Approximately:

49.7 bbl/day

This forecast represents the continuation of the fitted decline relationship.

Important interpretation

The forecast is a model-based projection using simulated data.

It should not be interpreted as an actual production forecast for a real petroleum field without real production history, engineering assumptions, model validation, and appropriate field-specific analysis.

⸻

7. Decline Curve Visualisation

The project creates a combined visualisation showing:

* Historical production
* Fitted decline curve
* 12-month forecast
* Historical/forecast boundary

The generated image is saved as:

decline_curve_analysis.png

The chart provides a visual representation of the production decline model and its future projection.

⸻

Part 2 — Well Performance Intelligence

The second component analyses a sample dataset containing eight wells.

The dataset includes:

* Well name
* Location
* Well type
* Average daily production
* Days active
* Water cut
* Operational status

If well_data_cleaned.csv is available, the system loads it.

Otherwise, the program uses its built-in sample dataset.

⸻

8. Composite Performance Score

The system creates a custom performance score for each well.

The score combines:

Production component

Production contributes up to 60 points.

The calculation is:

min(Avg_Daily_Barrels / 1000 * 60, 60)

Water-cut component

The water-cut component contributes up to 40 points.

The calculation is:

(1 - Water_Cut) * 40

The two components are added to produce:

Performance_Score

The maximum theoretical score is approximately:

100

Interpretation

The scoring logic rewards:

* Higher production
* Lower water cut

This is an original analytical scoring framework created for this project, rather than an industry-standard petroleum performance index.

⸻

9. Well Risk Classification

Each well is assigned a risk level based on water cut and production.

The rules are:

CRITICAL

Water cut:

> 50%

HIGH

Water cut:

> 30%

OR production:

< 200 bbl/day

MEDIUM

Water cut:

> 15%

LOW

All other wells.

This provides a simple screening mechanism for identifying wells that may require additional attention.

⸻

10. Recommended Actions

The system converts the risk classification and performance score into a recommended action.

CRITICAL

Immediate intervention required

HIGH

Schedule review within 30 days

Strong performer

When the performance score is above 70:

Monitor — performing well

Other wells

Optimisation study recommended

These recommendations are analytical outputs designed for demonstration and screening purposes.

They are not substitutes for engineering diagnostics or field operating decisions.

⸻

11. Well Performance Results

The eight sample wells produce the following results.

Well	Production (bbl/day)	Water Cut	Score	Risk
Well_Eta	891	11%	89.1	LOW
Well_Gamma	742	8%	81.3	LOW
Well_Epsilon	634	18%	70.8	MEDIUM
Well_Alpha	520	15%	65.2	LOW
Well_Beta	303	22%	49.4	MEDIUM
Well_Zeta	289	35%	43.3	HIGH
Well_Delta	179	45%	32.7	HIGH
Well_Theta	156	67%	22.6	CRITICAL

⸻

12. Highest-Scoring Wells

The highest performance score in the sample dataset belongs to:

Well_Eta

* Production: 891 bbl/day
* Water cut: 11%
* Performance score: 89.1
* Risk level: LOW
* Recommended action: Monitor — performing well

The second-highest score belongs to:

Well_Gamma

* Production: 742 bbl/day
* Water cut: 8%
* Performance score: 81.3
* Risk level: LOW

⸻

13. Highest-Risk Wells

Well_Theta

* Production: 156 bbl/day
* Water cut: 67%
* Performance score: 22.6
* Risk: CRITICAL
* Recommended action: Immediate intervention required

Well_Delta

* Production: 179 bbl/day
* Water cut: 45%
* Performance score: 32.7
* Risk: HIGH
* Recommended action: Schedule review within 30 days

Well_Zeta

* Production: 289 bbl/day
* Water cut: 35%
* Performance score: 43.3
* Risk: HIGH
* Recommended action: Schedule review within 30 days

These classifications are generated by the project’s defined rules.

⸻

14. Block-Level Intelligence

The system uses Pandas groupby() to analyse performance by location.

The following metrics are calculated:

* Number of wells
* Average performance score
* Total production
* Number of high/critical-risk wells

Block summary

Block	Wells	Average Score	Total Production (bbl/day)	High/Critical Risk Wells
Northern Block	3	78.5	2,153	0
Southern Block	2	60.1	937	0
Eastern Block	2	38.0	468	2
Western Block	1	22.6	156	1

⸻

15. Block-Level Insights

Northern Block

The Northern Block has:

* 3 wells
* 2,153 bbl/day total production
* Average performance score of 78.5
* No HIGH or CRITICAL-risk wells

It is the strongest-performing block in the sample according to the project’s scoring framework.

⸻

Southern Block

The Southern Block has:

* 2 wells
* 937 bbl/day total production
* Average performance score of 60.1
* No HIGH or CRITICAL-risk wells

The block contains a mixture of medium-risk and strong-performing wells.

⸻

Eastern Block

The Eastern Block has:

* 2 wells
* 468 bbl/day total production
* Average performance score of 38.0
* 2 HIGH/CRITICAL-risk wells

Both wells in the block meet the project’s high-risk criteria.

⸻

Western Block

The Western Block contains:

* 1 well
* 156 bbl/day production
* Average performance score of 22.6
* 1 HIGH/CRITICAL-risk well

The well is classified as CRITICAL because its water cut is 67%.

⸻

16. Technologies Used

Python

Primary programming language.

Pandas

Used for:

* DataFrames
* Data manipulation
* GroupBy analysis
* Dataset processing
* Sorting
* Aggregation

NumPy

Used for:

* Numerical calculations
* Exponential decline modelling
* Random noise generation
* Logarithmic transformation
* Manual regression calculations
* Forecast calculations

Matplotlib

Used for:

* Production history visualisation
* Decline curve visualisation
* Forecast visualisation

⸻

17. Key Python Concepts Demonstrated

This project demonstrates several important programming and data science concepts:

* NumPy arrays
* Random number generation
* Reproducible simulations
* Exponential functions
* Log transformations
* Manual linear regression
* Prediction
* Pandas DataFrames
* Custom functions
* Row-wise apply()
* Conditional logic
* Risk classification
* Custom scoring systems
* GroupBy aggregation
* Data sorting
* Data visualisation
* File input
* Exception handling

⸻

18. Petroleum Industry Relevance

The project demonstrates several concepts that can be relevant to petroleum data analysis.

Production decline analysis

Production decline analysis can help analysts examine how production changes over time and explore possible future production trends.

Well performance screening

Combining production and water cut can help create structured screening frameworks for identifying wells that may require additional review.

Risk classification

Automated rules can help organise wells into different levels of attention.

Field/block comparison

Grouping wells by location allows analysts to compare operational performance between blocks.

Decision support

Combining production, risk, and recommended actions demonstrates how analytical systems can transform raw data into structured information for further technical investigation.

⸻

19. Important Limitations

This project is an educational and portfolio capstone.

Several limitations should be recognised.

Simulated forecasting data

The decline-analysis dataset is artificially generated and should not be treated as actual field production data.

Simplified decline model

The forecasting component uses a log-linear regression approach to model exponential decline.

Real petroleum production forecasting may require more detailed reservoir, well, pressure, operational, and historical production information.

Custom performance score

The performance score is a project-specific analytical framework.

It is not an industry-standard petroleum engineering metric.

Simplified risk rules

Risk categories are based on simple threshold rules for water cut and production.

Actual intervention decisions would require additional technical information.

Sample financial/operational data

The well intelligence dataset is a sample dataset used to demonstrate analytical methods.

The results should therefore be interpreted as portfolio analysis rather than actual field recommendations.

⸻

20. Future Improvements

Possible future development includes:

* Connecting the system to real production datasets
* Adding production decline model comparison
* Testing additional forecasting techniques
* Adding model evaluation metrics
* Incorporating pressure data
* Incorporating well intervention history
* Adding reservoir or completion information
* Adding economic analysis
* Creating an interactive dashboard
* Adding automated report generation
* Adding anomaly detection
* Creating a database-backed version
* Adding machine-learning models for production forecasting
* Developing a web-based interface

⸻

21. Skills Developed

This project strengthened my ability to:

* Work with structured petroleum datasets
* Generate and analyse simulated production data
* Transform data for modelling
* Implement mathematical models using NumPy
* Build regression calculations from first principles
* Generate production forecasts
* Create custom analytical scoring systems
* Develop rule-based risk classification
* Use Pandas for field-level analysis
* Aggregate data by operational blocks
* Create technical visualisations
* Translate analytical results into operational insights

⸻

22. Project Workflow

The overall workflow can be summarised as:

Production Data
       ↓
Data Preparation
       ↓
Production Decline Analysis
       ↓
Log Transformation
       ↓
Linear Regression
       ↓
Production Forecast
       ↓
Well Performance Scoring
       ↓
Risk Classification
       ↓
Recommended Actions
       ↓
Block-Level GroupBy Analysis
       ↓
Field Intelligence

⸻

23. Project Files

Project Documentation:
https://github.com/mensahhayford/python-project/blob/main/docs/12-field-intelligence-system.md

Python Source Code:
https://github.com/mensahhayford/python-project/blob/main/field_intelligence_system.py

Decline Curve Analysis Chart:
https://github.com/mensahhayford/python-project/blob/main/decline_curve_analysis.png

⸻

24. Conclusion

The Field Intelligence System represents a transition from individual Python exercises toward an integrated petroleum data analytics workflow.

The project combines:

Production Analysis + Forecasting + Well Scoring + Risk Screening + Block Analysis + Visualisation

The main lesson from this project is that data science can be used not only to calculate statistics, but also to organise complex operational information into a form that can support further technical investigation and decision-making.

This capstone forms an important stage in my development toward applying Python and Data Science to petroleum and energy-related problems.

https://github.com/mensahhayford/python-project