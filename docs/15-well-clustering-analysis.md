Project 15: Well Clustering Analysis Using K-Means

Overview

This project applies unsupervised machine learning to synthetic oil-well data to identify groups of wells with similar production and operational characteristics.

The analysis uses Python, Pandas, NumPy, Matplotlib, and Scikit-learn. It standardizes the selected features, compares K-Means clustering configurations, selects the best number of clusters using the silhouette score, and summarizes the resulting groups.

Objectives

* Prepare and standardize well production data.
* Evaluate K-Means clustering for values of K from 2 to 8.
* Select the number of clusters with the highest silhouette score.
* Compare clusters by production rate, water cut, pressure decline, and producing days.
* Apply simple rules to classify wells for operational review.

Dataset

The dataset contains 80 synthetically generated wells with these features:

* Production_Rate: production rate in barrels per day.
* Water_Cut: proportion of produced water.
* Pressure_Decline: pressure-decline value used in the simulation.
* Days_Producing: number of producing days in the simulation.

Data note: The dataset is synthetic and is intended for demonstration and learning. The results are not observations from a real oil field.

Methodology

1. Generate the synthetic dataset.
2. Select the four numerical features.
3. Standardize the features using StandardScaler.
4. Fit K-Means models for K values from 2 through 8.
5. Compare models using inertia and silhouette scores.
6. Select the K value with the highest silhouette score.
7. Summarize the resulting clusters.
8. Apply rule-based labels to individual wells.

Model Selection Results

The best silhouette score among the tested configurations was approximately 0.7176, obtained with 3 clusters.

Number of clusters	Silhouette score
2	0.5982
3	0.7176
4	0.6075
5	0.6015
6	0.4193
7	0.4403
8	0.3071

The model therefore selected three clusters for the final analysis.

Cluster Summary

The following table summarizes the generated clusters. Values are approximate and should be checked against the output of the saved script before publication.

Cluster	Wells	Average production (bbl/day)	Average water cut	Average pressure decline	Average producing days
0	30	453.70	35%	0.07	717.60
1	25	177.38	64%	0.12	1,129.86
2	25	786.92	9%	0.02	395.76

The clusters show distinct production and operational profiles in this synthetic dataset.

Rule-Based Well Classification

In addition to clustering, the script assigns labels using explicit rules:

* HIGH PERFORMER: production rate greater than 600 bbl/day.
* DECLINING — REVIEW: production rate is not above 600 bbl/day and water cut is greater than 50%.
* STABLE PRODUCER: neither of the preceding conditions is met.

These are simple demonstration rules, not a validated engineering diagnosis or a substitute for field assessment.

Tools and Libraries

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* K-Means clustering
* StandardScaler
* Silhouette score

Key Takeaways

* Feature scaling is important when clustering variables have different units and ranges.
* The silhouette score helps compare candidate clustering configurations.
* Cluster summaries can help identify groups with different production characteristics.
* Rule-based labels should be distinguished from labels learned by an unsupervised model.

Limitations

* The data is synthetic, not real field data.
* The selected number of clusters is based on the tested range of K values.
* The rule-based labels are simplified and are not automatically learned by K-Means.
* This version imports PCA but does not yet use it in the analysis.

How to Run

Install the required libraries if necessary:

pip install pandas numpy matplotlib scikit-learn

Run the script:

python well_clustering_analysis.py

Conclusion

This project demonstrates a reproducible workflow for exploring well groups using K-Means clustering and silhouette-based model selection. It provides a foundation for future work with real production data, richer validation, and engineering-informed analysis.