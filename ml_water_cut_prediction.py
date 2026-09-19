import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    mean_absolute_error
)

# ═══════════════════════════════════
# THE PROBLEM:
# Can we predict a well's water cut
# based on how long it has been
# producing and its initial production?
#
# In real petroleum operations:
# Predicting water cut rise helps
# engineers schedule interventions
# BEFORE production declines severely.
# ═══════════════════════════════════

# Create a realistic training dataset
# Simulating 50 wells with known history
np.random.seed(42)
n_wells = 50

days_producing = np.random.randint(
    90, 1500, n_wells
)
initial_production = np.random.randint(
    200, 1200, n_wells
)

# Water cut increases with time
# and decreases with initial production
# (high-rate wells tend to have
# better reservoir support)
water_cut = (
    0.05 +
    0.0003 * days_producing -
    0.00005 * initial_production +
    np.random.normal(0, 0.05, n_wells)
)
water_cut = np.clip(water_cut, 0.01, 0.95)

df_ml = pd.DataFrame({
    "Days_Producing": days_producing,
    "Initial_Production": initial_production,
    "Water_Cut": water_cut.round(3)
})

print("=== ML TRAINING DATASET ===")
print(df_ml.describe().round(3))
print(f"\nDataset: {len(df_ml)} wells")

# ═══════════════════════════════════
# STEP 1: DEFINE FEATURES AND TARGET
# ═══════════════════════════════════

# Features — what we use to predict
X = df_ml[[
    "Days_Producing",
    "Initial_Production"
]]

# Target — what we want to predict
y = df_ml["Water_Cut"]

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")

# ═══════════════════════════════════
# STEP 2: SPLIT INTO TRAINING AND TEST
# 80% train, 20% test
# random_state ensures reproducibility
# ═══════════════════════════════════

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print(f"\nTraining set: {len(X_train)} wells")
print(f"Test set: {len(X_test)} wells")

# ═══════════════════════════════════
# STEP 3: FIT THE MODEL
# ═══════════════════════════════════

model = LinearRegression()
model.fit(X_train, y_train)

print("\n=== MODEL PARAMETERS ===")
print(f"Intercept: {model.intercept_:.4f}")
for feature, coef in zip(
    X.columns, model.coef_
):
    print(f"Coefficient ({feature}): {coef:.6f}")

# ═══════════════════════════════════
# STEP 4: EVALUATE ON TEST SET
# ═══════════════════════════════════

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n=== MODEL PERFORMANCE ===")
print(f"R² Score          : {r2:.3f}")
print(f"  → Model explains {r2*100:.1f}% of variance")
print(f"RMSE              : {rmse:.4f}")
print(f"  → Average error : ±{rmse*100:.1f}% water cut")
print(f"MAE               : {mae:.4f}")

# ═══════════════════════════════════
# STEP 5: USE THE MODEL
# Predict water cut for new wells
# ═══════════════════════════════════

new_wells = pd.DataFrame({
    "Days_Producing": [180, 365, 730, 1095],
    "Initial_Production": [800, 600, 400, 300]
})

predictions = model.predict(new_wells)
new_wells["Predicted_Water_Cut"] = (
    np.clip(predictions, 0, 1).round(3)
)
new_wells["Predicted_WC_Pct"] = (
    new_wells["Predicted_Water_Cut"] * 100
).round(1)

print("\n=== PREDICTIONS FOR NEW WELLS ===")
print(new_wells.to_string())
# ═══════════════════════════════════
# VISUALISE MODEL PERFORMANCE
# ═══════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Chart 1: Actual vs Predicted
axes[0].scatter(
    y_test, y_pred,
    alpha=0.6,
    color="#2196F3",
    edgecolors="black",
    linewidth=0.3
)
# Perfect prediction line
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
axes[0].plot(
    [min_val, max_val],
    [min_val, max_val],
    "r--",
    linewidth=2,
    label="Perfect prediction"
)
axes[0].set_xlabel("Actual Water Cut")
axes[0].set_ylabel("Predicted Water Cut")
axes[0].set_title(
    f"Actual vs Predicted\nR² = {r2:.3f}",
    fontweight="bold"
)
axes[0].legend()

# Chart 2: Days producing vs water cut
# with model line
days_range = np.linspace(
    df_ml["Days_Producing"].min(),
    df_ml["Days_Producing"].max(),
    100
)
avg_initial = df_ml["Initial_Production"].mean()
model_line = model.predict(
    pd.DataFrame({
        "Days_Producing": days_range,
        "Initial_Production": [avg_initial] * 100
    })
)

axes[1].scatter(
    df_ml["Days_Producing"],
    df_ml["Water_Cut"],
    alpha=0.5,
    color="#4CAF50",
    edgecolors="black",
    linewidth=0.3,
    label="Actual wells"
)
axes[1].plot(
    days_range,
    np.clip(model_line, 0, 1),
    color="#F44336",
    linewidth=2,
    label=f"Model (avg production = "
          f"{avg_initial:.0f} bbl/d)"
)
axes[1].set_xlabel("Days Producing")
axes[1].set_ylabel("Water Cut")
axes[1].set_title(
    "Production Duration vs Water Cut",
    fontweight="bold"
)
axes[1].legend(fontsize=8)

# Chart 3: Residuals
residuals = y_test - y_pred
axes[2].scatter(
    y_pred, residuals,
    alpha=0.6,
    color="#FF9800",
    edgecolors="black",
    linewidth=0.3
)
axes[2].axhline(
    y=0,
    color="red",
    linestyle="--",
    linewidth=2
)
axes[2].set_xlabel("Predicted Water Cut")
axes[2].set_ylabel("Residual (Actual - Predicted)")
axes[2].set_title(
    "Residual Analysis\n"
    "(Points near zero = good predictions)",
    fontweight="bold"
)

plt.suptitle(
    "ML Water Cut Prediction Model —"
    " Petroleum Well Analysis",
    fontsize=13,
    fontweight="bold",
    y=1.02
)
plt.tight_layout()
plt.savefig(
    "ml_water_cut_prediction.png",
    dpi=150,
    bbox_inches="tight"
)
plt.show()
print("ML model charts saved.")