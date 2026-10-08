# Project 11 — GroupBy Profitability Dashboard
## Overview
The **GroupBy Profitability Dashboard** is a Python-based petroleum data analysis project that combines well-production data with financial assumptions to evaluate the performance and profitability of different field blocks.
The project demonstrates how Python and Pandas can be used to move from basic well-level data to higher-level operational and financial analysis.
The workflow combines:
- Pandas `groupby()`
- Multiple aggregations
- Conditional filtering
- `transform()`
- Dataset merging
- Revenue calculations
- Operating-cost calculations
- Profit calculations
- Return on Investment (ROI)
- Data visualization
The final output is a two-chart financial performance dashboard showing annual profit and ROI by block.
---
# Project Objective
The main objective of this project is to analyze petroleum well data at the **field-block level** and combine production information with financial assumptions to estimate profitability.
The project demonstrates how data can be transformed from individual wells into useful management-level indicators such as:
- Total production by block
- Average production
- Water-cut performance
- Active-well production
- Block production contribution
- Daily revenue
- Daily operating expenditure
- Annual profit
- Estimated ROI
---
# Dataset
The program first attempts to load:
```text
well_data_cleaned.csv

If that file is unavailable, it creates a built-in sample dataset containing 8 wells.

The well dataset includes:

* Well name
* Location
* Well type
* Average daily production
* Days active
* Water cut
* Status

⸻

Sample Well Dataset

Well	Location	Type	Avg. Daily Production	Days Active	Water Cut	Status
Well Alpha	Northern Block	Oil	520 bbl/day	365	15%	Active
Well Beta	Southern Block	Oil	303 bbl/day	280	22%	Active
Well Gamma	Northern Block	Gas Condensate	742 bbl/day	410	8%	Active
Well Delta	Eastern Block	Oil	179 bbl/day	190	45%	Review needed
Well Epsilon	Southern Block	Oil	634 bbl/day	320	18%	Active
Well Zeta	Eastern Block	Gas Condensate	289 bbl/day	245	35%	Review needed
Well Eta	Northern Block	Oil	891 bbl/day	400	11%	Active
Well Theta	Western Block	Oil	156 bbl/day	180	67%	Inactive

⸻

1. Production by Location

The first GroupBy analysis calculates total production by location.

The program uses:

df.groupby("Location")["Avg_Daily_Barrels"].sum()

The results are:

Block	Total Production
Northern Block	2,153 bbl/day
Southern Block	937 bbl/day
Eastern Block	468 bbl/day
Western Block	156 bbl/day

Key Observation

The Northern Block has the highest total reported production at:

2,153 bbl/day

The Western Block has the lowest at:

156 bbl/day

⸻

2. Average Water Cut by Well Type

The program groups wells according to their type and calculates average water cut.

Results

Well Type	Average Water Cut
Oil	29.7%
Gas Condensate	21.5%

The calculation provides a simple comparison of average water-cut levels between the two well types represented in the sample dataset.

⸻

3. Comprehensive Block Analysis

The project demonstrates multiple Pandas aggregations within a single groupby() operation.

The following metrics are calculated for each block:

* Well count
* Total production
* Average production
* Maximum production
* Minimum production
* Average water cut
* Total active days recorded in the dataset

Results

Block	Wells	Total Production	Avg. Production	Max	Min	Avg. Water Cut	Total Days
Eastern Block	2	468	234.0	289	179	40.0%	435
Northern Block	3	2,153	717.7	891	520	11.3%	1,175
Southern Block	2	937	468.5	634	303	20.0%	600
Western Block	1	156	156.0	156	156	67.0%	180

Key Observations

Northern Block

* Highest total production
* Highest average production
* Highest individual well production
* Lowest average water cut among the four blocks

Western Block

* Lowest production
* Highest average water cut at 67%

Eastern Block

* Average water cut of 40%
* Contains two wells requiring review

⸻

4. Active Wells by Block

The program filters the dataset to include only wells whose status is:

Active

It then performs another GroupBy analysis.

Results

Block	Active Wells	Active Production	Average Water Cut
Northern Block	3	2,153 bbl/day	11.3%
Southern Block	2	937 bbl/day	20.0%

The Eastern and Western Blocks have no wells classified as Active in this dataset.

⸻

5. GroupBy Transform

One of the important techniques demonstrated in this project is Pandas transform().

The program calculates each block’s total production:

df["Block_Total"] = df.groupby(
    "Location"
)["Avg_Daily_Barrels"].transform("sum")

Unlike a normal GroupBy summary, transform() returns a value for every original row.

This allows the program to calculate each well’s contribution to its own block.

The calculation is:

Well Production
------------------------- × 100
Block Total Production

⸻

6. Well Contribution to Block Production

Northern Block

Total production:

2,153 bbl/day

* Well Eta: 41.4%
* Well Gamma: 34.5%
* Well Alpha: 24.2%

Southern Block

Total production:

937 bbl/day

* Well Epsilon: 67.7%
* Well Beta: 32.3%

Eastern Block

Total production:

468 bbl/day

* Well Zeta: 61.8%
* Well Delta: 38.2%

Western Block

Total production:

156 bbl/day

* Well Theta: 100.0%

This analysis provides a simple way to understand how dependent each block’s production is on individual wells.

⸻

7. Financial Dataset

The project creates a second dataset containing financial assumptions for each block.

The financial assumptions include:

* Oil price
* Operating cost per barrel
* Investment
* Years producing

Financial Assumptions

Block	Oil Price	Operating Cost/Bbl	Investment	Years Producing
Northern Block	$72.50	$18.20	$125M	3
Southern Block	$72.50	$22.10	$87M	2
Eastern Block	$72.50	$31.50	$43M	1
Western Block	$72.50	$45.80	$28M	1

These values are sample assumptions included in the program and are not presented as actual commercial field data.

⸻

8. Merging Production and Financial Data

The project combines the production and financial datasets using:

pd.merge()

The merge is performed using:

Location

as the common key.

This is conceptually similar to a SQL JOIN.

The resulting dataset combines:

Production Data
       +
Financial Assumptions
       ↓
Combined Block Dataset

This allows operational data to be connected to financial assumptions for further analysis.

⸻

9. Revenue Calculation

Daily revenue is calculated using:

Daily Production × Oil Price

The program uses an assumed oil price of:

$72.50/bbl

Example — Northern Block

Production:

2,153 bbl/day

Therefore:

2,153 × $72.50
= $156,092.50/day

⸻

10. Operating Expenditure Calculation

Daily operating expenditure is calculated using:

Daily Production × Operating Cost per Barrel

For the Northern Block:

2,153 × $18.20
= $39,184.60/day

⸻

11. Daily Profit Calculation

The program calculates daily profit as:

Daily Revenue − Daily Operating Cost

For the Northern Block:

$156,092.50 − $39,184.60
= $116,907.90/day

⸻

12. Annual Profit Estimate

Annual profit is calculated as:

Daily Profit × 365

The result is then converted to millions of US dollars.

Estimated Annual Profit by Block

Block	Daily Profit	Estimated Annual Profit
Northern Block	$116,907.90	$42.67M
Southern Block	$47,067.20	$17.18M
Eastern Block	$19,188.00	$7.00M
Western Block	$4,165.20	$1.52M

These are modelled estimates based on the production, oil-price, and operating-cost assumptions contained in the program.

⸻

13. ROI Calculation

The program calculates ROI using:

Annual Profit
------------------------- × 100
Investment

Estimated ROI

Block	Annual Profit	Investment	Estimated ROI
Northern Block	$42.67M	$125M	34.1%
Southern Block	$17.18M	$87M	19.8%
Eastern Block	$7.00M	$43M	16.3%
Western Block	$1.52M	$28M	5.4%

Best ROI

Northern Block — 34.1%

Lowest ROI

Western Block — 5.4%

⸻

14. Profitability Ranking

Based on the program’s ROI calculation:

1. Northern Block — 34.1%
2. Southern Block — 19.8%
3. Eastern Block — 16.3%
4. Western Block — 5.4%

The Northern Block produces the strongest estimated return under the assumptions used in the model.

⸻

15. Profitability Dashboard

The program creates a two-panel visualization using Matplotlib.

The output file is:

block_profitability_dashboard.png

The dashboard contains two charts.

⸻

Chart 1 — Annual Profit by Block

The first chart compares estimated annual profit across the four blocks.

It allows the user to quickly identify which blocks contribute the greatest estimated annual profit under the model assumptions.

The Northern Block has the highest estimated annual profit.

⸻

Chart 2 — ROI Comparison

The second chart compares estimated ROI between the blocks.

It also displays the average ROI across the four blocks as a reference line.

This makes it easier to identify blocks performing above or below the modelled average.

⸻

16. Key Findings

Based on the sample dataset and the financial assumptions used by the program:

Highest Production

Northern Block — 2,153 bbl/day

Highest Average Production

Northern Block — 717.7 bbl/day per well

Lowest Production

Western Block — 156 bbl/day

Highest Average Water Cut

Western Block — 67.0%

Highest Estimated Annual Profit

Northern Block — approximately $42.67M

Highest Estimated ROI

Northern Block — approximately 34.1%

Lowest Estimated ROI

Western Block — approximately 5.4%

⸻

17. Important Financial Interpretation

The profitability analysis is a simplified financial model.

The results are based on assumptions included directly in the project:

* Constant oil price of $72.50/bbl
* Constant production rates
* Constant operating costs
* 365-day annualization
* Investment values supplied in the sample dataset

The model does not include many factors that would be required for a full petroleum-economic evaluation, such as:

* Taxes
* Royalties
* Transportation costs
* Processing costs
* Capital expenditure schedules
* Depreciation
* Inflation
* Production decline
* Oil-price fluctuations
* Gas pricing
* Working-interest arrangements
* Revenue-sharing agreements
* Abandonment costs
* Discount rates
* Net present value
* Internal rate of return

Therefore, the financial results should be interpreted as portfolio-project estimates demonstrating data-analysis techniques, rather than actual investment recommendations.

⸻

18. Technical Concepts Demonstrated

This project demonstrates several important Python and Pandas concepts.

groupby()

Used to aggregate well-level data into block-level summaries.

agg()

Used to calculate multiple statistics simultaneously.

Conditional Filtering

Used to isolate active wells before performing further analysis.

transform()

Used to calculate block totals while retaining the original well-level rows.

merge()

Used to combine production data with financial assumptions.

Calculated Columns

Used to derive:

* Revenue
* Operating expenditure
* Profit
* ROI

Matplotlib

Used to create the profitability dashboard.

⸻

19. Python Libraries Used

Pandas

Used for:

* Data loading
* DataFrames
* GroupBy operations
* Aggregation
* Filtering
* Transformation
* Dataset merging
* Financial calculations

NumPy

Imported as part of the data-analysis environment.

Matplotlib

Used to create the profitability dashboard.

⸻

20. Petroleum Data Science Relevance

This project demonstrates how petroleum data can be connected to both operational and financial analysis.

Production data alone can show:

* How much each block produces
* Which wells contribute most
* Water-cut patterns
* Active-well performance

Combining production data with financial assumptions allows additional questions to be explored:

* Which block generates the highest estimated profit?
* Which block has the highest estimated ROI?
* Which blocks have higher operating costs?
* How dependent is a block on individual wells?
* Which blocks may require closer financial or operational review?

This represents a transition from basic data analysis toward decision-support analysis.

⸻

21. Skills Demonstrated

Through this project, I practiced:

* Python programming
* Pandas
* GroupBy analysis
* Multiple aggregation
* Conditional data analysis
* Transform operations
* Data merging
* Financial calculations
* ROI analysis
* Data visualization
* Analytical interpretation
* Petroleum production analysis

⸻

22. Limitations

This project has several limitations.

Sample Dataset

The fallback dataset is a small demonstration dataset.

Simplified Financial Model

The profitability calculations use simplified assumptions and do not represent a complete petroleum-economic model.

Constant Oil Price

The model uses the same oil price of $72.50/bbl for all blocks.

Constant Production

The annual profit calculation assumes the reported daily production remains constant throughout the year.

Operating Costs

Operating costs are represented by a single cost-per-barrel assumption for each block.

No Production Decline

The model does not account for future production decline.

No Time-Series Financial Analysis

The project does not currently model changes in production, price, or operating cost over time.

⸻

23. Future Improvements

Potential improvements include:

* Adding historical production data
* Adding production-decline modelling
* Adding oil-price sensitivity analysis
* Adding break-even analysis
* Adding Net Present Value (NPV)
* Adding Internal Rate of Return (IRR)
* Adding discounted cash-flow analysis
* Adding production forecasting
* Adding interactive dashboards
* Adding database connectivity
* Adding automated PDF reports
* Adding scenario analysis
* Adding uncertainty analysis

A future version could allow users to change oil price, operating costs, and investment assumptions interactively and immediately see how profitability changes.

⸻

24. Projet files;


 Project Documentation:
https://github.com/mensahhayford/python-project/blob/main/docs/11-groupby-profitability-dashboard.md

Python Source Code:
https://github.com/mensahhayford/python-project/blob/main/advanced_groupby_profitability.py

Dashboard:
https://github.com/mensahhayford/python-project/blob/main/block_profitability_dashboard.png

Complete Portfolio:
https://github.com/mensahhayford/python-project

⸻

25. Conclusion

The GroupBy Profitability Dashboard demonstrates how Python can be used to connect petroleum production data with financial analysis.

The project progresses through several levels of analysis:

Well-Level Data
      ↓
GroupBy Analysis
      ↓
Block-Level Production Analysis
      ↓
Conditional Analysis
      ↓
Transform Operations
      ↓
Financial Data
      ↓
Dataset Merge
      ↓
Revenue & Cost Analysis
      ↓
Profitability & ROI
      ↓
Visualization

The project strengthened my understanding of Pandas GroupBy operations, data transformation, dataset merging, financial modelling, ROI analysis, and data visualization.

It also demonstrates how programming can help turn production data into structured information that can support further operational and financial investigation.

Important: The financial figures presented in this project are modelled estimates based on the assumptions contained in the sample dataset and should not be interpreted as actual field financial results or investment advice.