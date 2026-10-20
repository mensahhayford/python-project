Project 13: Machine Learning Water Cut Prediction

Overview

This project applies supervised machine learning to petroleum well analysis. It uses a Linear Regression model to predict the water cut of a well based on two input features: days producing and initial production rate.

Water cut is the proportion of produced fluid that consists of water. Monitoring and estimating water cut can support production surveillance and help engineers identify wells that may require further investigation.

Important: This project uses synthetically generated data for learning and demonstration. Its predictions are not validated against actual field measurements.

Project Objectives

* Generate a reproducible dataset containing 50 synthetic well records.
* Explore relationships between production duration, initial production rate, and water cut.
* Prepare features and a target variable for machine learning.
* Split the dataset into training and testing subsets.
* Train a Linear Regression model.
* Evaluate model performance using R², Root Mean Squared Error (RMSE), and Mean Absolute Error (MAE).
* Predict water cut for four example wells.
* Visualize prediction performance and residuals.

Tools and Libraries

* Python
* pandas — data manipulation and analysis
* NumPy — numerical operations and synthetic data generation
* Matplotlib — data visualization
* scikit-learn — model training, data splitting, and evaluation

Dataset

The dataset contains 50 synthetically generated wells using a fixed random seed for reproducibility.

Features

Feature	Description
Days_Producing	Number of days a well has been producing
Initial_Production	Initial production rate, expressed in barrels per day (bbl/d)
Water_Cut	Target variable representing the fraction of produced fluid that is water

The synthetic water-cut values are generated using a formula that incorporates production duration, initial production, and random noise. Values are then constrained to a range between 0.01 and 0.95.

This is a demonstration dataset, not a record of actual petroleum wells.

Methodology

1. Synthetic Data Generation

NumPy generates production durations, initial production rates, and water-cut values. A fixed random seed makes the generated dataset reproducible.

2. Feature and Target Selection

The model uses:

* Days_Producing
* Initial_Production

The target variable is Water_Cut.

3. Train-Test Split

The dataset is divided into:

* 80% training data
* 20% testing data

A fixed random_state makes the split reproducible.

4. Model Training

A Linear Regression model is fitted using the training data. The model learns coefficients that describe the linear relationship between the selected features and water cut.

5. Model Evaluation

The model is evaluated against the held-out test set using three metrics:

* R² score: Measures how well the model explains variation in the test targets. A higher value generally indicates a better fit; a negative value means the model performs worse than predicting the test-set mean.
* RMSE: Measures the square root of the mean squared prediction error. It penalizes larger errors more heavily and is expressed in water-cut fraction units.
* MAE: Measures the average absolute prediction error, also in water-cut fraction units.

The actual metric values are printed when the program runs. They should be reported from the current execution rather than assumed in advance.

6. Predictions for New Wells

The trained model predicts water cut for four example combinations of production duration and initial production rate.

The script clips these displayed predictions to the range from 0 to 1 and converts them into percentages. The un-clipped predictions are used for the model evaluation metrics.

7. Visualization

The program generates a three-panel figure:

1. Actual vs. Predicted Water Cut: Compares test-set predictions with actual synthetic target values and includes a reference line for perfect predictions.
2. Production Duration vs. Water Cut: Displays the synthetic well observations and a model line calculated while holding initial production at its dataset average.
3. Residual Analysis: Plots prediction residuals against predicted values to help inspect error patterns.

The figure is saved as ml_water_cut_prediction.png.

How to Run the Project

Install the required libraries if they are not already installed:

pip install pandas numpy matplotlib scikit-learn

Run the script from the folder containing ml_water_cut_prediction.py:

python ml_water_cut_prediction.py

The program prints the dataset summary, training and testing sizes, model coefficients, evaluation metrics, and example predictions. It then displays the visualizations and saves the figure.

Key Learning Outcomes

This project demonstrates how to:

* Structure a supervised machine learning problem.
* Separate input features from a prediction target.
* Split data into training and testing sets.
* Fit and evaluate a Linear Regression model.
* Interpret common regression evaluation metrics.
* Generate predictions for new observations.
* Use plots to examine model fit and residual behavior.
* Explain the limitations of synthetic data in an applied petroleum context.

Limitations and Future Improvements

The dataset is synthetic and follows a formula chosen for demonstration. Consequently, the model may learn patterns built into that formula rather than relationships that generalize to actual field conditions.

Further development could include:

* Testing the workflow on quality-controlled, real well production data.
* Including additional features such as reservoir pressure, cumulative production, water production rate, and well characteristics where available.
* Comparing Linear Regression with other regression algorithms.
* Using cross-validation and appropriate baseline models.
* Examining outliers, residual patterns, and prediction uncertainty.
* Evaluating performance on independent field data before drawing operational conclusions.

Conclusion

Project 13 demonstrates an end-to-end introductory regression workflow for petroleum data science, from synthetic data generation and model training to evaluation, prediction, and visualization.

It provides a foundation for developing and testing water-cut prediction methods, while recognizing that real operational use requires validation against representative field data.