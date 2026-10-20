Project 14: Well Intervention Classifier

Overview

This project uses Python and a Random Forest classification model to predict whether a synthetic oil well is labelled as needing intervention, such as a workover or chemical treatment, within a hypothetical 90-day planning period.

The project demonstrates how machine learning can classify wells using production and operating characteristics. The dataset is synthetically generated for learning purposes and does not represent measured field data.

Objectives

* Generate a synthetic dataset of 150 wells.
* Explore production and operating features associated with intervention labels.
* Train a Random Forest classifier.
* Evaluate the model using test accuracy, cross-validation, precision, recall, F1-score, and a confusion matrix.
* Examine feature importance.
* Generate intervention predictions and probabilities for four example wells.
* Visualize classification performance and water-cut distributions.

Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Random Forest Classification

Dataset

The synthetic dataset contains the following features:

Feature	Description
Days_Producing	Number of days the well has been producing
Water_Cut	Fraction of produced fluid represented by water
Production_Rate	Synthetic production-rate value
Pressure_Decline_Rate	Synthetic pressure-decline indicator
Sand_Production	Binary indicator for sand production
Needs_Intervention	Target label: 1 for intervention and 0 otherwise

The intervention label is generated using a formula based on the input features and random noise. Consequently, the model learns a simulated labelling rule rather than a verified real-world intervention mechanism.

Methodology

1. Generate 150 synthetic well records using NumPy.
2. Separate the five input features from the target label.
3. Split the data into 80% training and 20% testing subsets using stratification.
4. Train a Random Forest classifier with 100 trees, maximum depth of 5, and balanced class weights.
5. Evaluate performance on the held-out test set.
6. Perform five-fold cross-validation.
7. Rank features using the model’s feature-importance scores.
8. Predict intervention classes and probabilities for four illustrative wells.
9. Generate and save visualizations as intervention_classifier.png.

Model Configuration

* Model: RandomForestClassifier
* Number of trees: 100
* Maximum tree depth: 5
* Random state: 42
* Class weighting: balanced
* Test-set proportion: 20%
* Cross-validation: 5-fold accuracy scoring

Results

Using the current code and its fixed random seed:

* Test accuracy: 90.0%
* Five-fold cross-validation mean accuracy: 93.3%
* Cross-validation scores: 93.3%, 90.0%, 96.7%, 96.7%, and 90.0%

The synthetic dataset contains 123 of 150 wells labelled as needing intervention (82.0%).

The test classification report showed:

Metric	No Intervention	Needs Intervention
Precision	1.00	0.89
Recall	0.40	1.00
F1-score	0.57	0.94
Test support	5	25

The model identified all test wells labelled as needing intervention but incorrectly flagged some wells that were labelled as not needing intervention. The small test sample for the no-intervention class also makes its metrics sensitive to individual predictions.

Feature Importance

The model’s feature-importance scores from the current run ranked the inputs approximately as follows:

1. Days_Producing: 0.341
2. Water_Cut: 0.288
3. Production_Rate: 0.206
4. Sand_Production: 0.085
5. Pressure_Decline_Rate: 0.080

These scores describe how the fitted model used the features. They do not prove that a feature causes a well intervention.

Visualizations

The script saves three visualizations in intervention_classifier.png:

1. Confusion Matrix: Compares actual test labels with predicted labels.
2. Feature Importance: Displays the relative importance scores assigned by the Random Forest model.
3. Water-Cut Distribution: Compares water-cut distributions between the two intervention-label groups.

How to Run

Install the required libraries if they are not already available:

pip install pandas numpy matplotlib scikit-learn

Run the Python script from the project directory:

python well_intervention_classifier.py

Use the actual filename of your script if it differs.

Limitations and Future Improvements

* The dataset is synthetic, not real petroleum field data.
* The target label is generated from a formula using the same features supplied to the classifier.
* The dataset is imbalanced, with 82% of wells assigned the intervention label.
* Accuracy alone is insufficient for evaluating intervention decisions.
* Future versions could use verified historical well data, assess precision-recall trade-offs, evaluate probability calibration, and compare alternative models.
* Any real operational use would require validation, appropriate engineering review, and consideration of intervention costs and risks.

Conclusion

This project demonstrates an end-to-end machine learning classification workflow for a simulated petroleum engineering problem. It covers synthetic data generation, feature selection, model training, cross-validation, classification metrics, feature importance, prediction probabilities, and visualization.

The project provides a foundation for future work using verified field data and more rigorous evaluation of intervention-planning models. 