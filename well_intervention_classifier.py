import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import (
    RandomForestClassifier
)
from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)
from sklearn.preprocessing import LabelEncoder

# ═══════════════════════════════════
# THE PROBLEM:
# Predict which wells will need
# intervention (workover or
# chemical treatment) in the
# next 90 days.
#
# REAL INDUSTRY CONTEXT:
# Workovers (well intervention jobs)
# cost $100K–$5M each.
# Predicting them in advance allows
# scheduling and cost optimisation.
# Late detection = emergency intervention
# = much higher cost.
# ═══════════════════════════════════

np.random.seed(42)
n_wells = 150

# Generate features
days_producing = np.random.randint(
    30, 2000, n_wells
)
water_cut = np.random.uniform(
    0.02, 0.90, n_wells
)
production_rate = np.random.randint(
    50, 1200, n_wells
)
pressure_decline = np.random.uniform(
    0.01, 0.15, n_wells
)
sand_production = np.random.choice(
    [0, 1], n_wells, p=[0.7, 0.3]
)

# Create intervention label
# Wells needing intervention tend to have:
# high water cut, declining pressure,
# sand production, long producing time
intervention_score = (
    2.0 * water_cut +
    3.0 * pressure_decline +
    1.5 * (sand_production) +
    0.001 * days_producing -
    0.001 * production_rate +
    np.random.normal(0, 0.2, n_wells)
)

needs_intervention = (
    intervention_score > 0.8
).astype(int)

df_class = pd.DataFrame({
    "Days_Producing": days_producing,
    "Water_Cut": water_cut.round(3),
    "Production_Rate": production_rate,
    "Pressure_Decline_Rate": pressure_decline.round(4),
    "Sand_Production": sand_production,
    "Needs_Intervention": needs_intervention
})

print("=== CLASSIFICATION DATASET ===")
print(df_class.describe().round(3))
print(f"\nWells needing intervention: "
      f"{needs_intervention.sum()} "
      f"({needs_intervention.mean()*100:.1f}%)")

# ═══════════════════════════════════
# PREPARE FEATURES AND TARGET
# ═══════════════════════════════════

feature_columns = [
    "Days_Producing", "Water_Cut",
    "Production_Rate",
    "Pressure_Decline_Rate",
    "Sand_Production"
]

X = df_class[feature_columns]
y = df_class["Needs_Intervention"]

# Split data
X_train, X_test, y_train, y_test = (
    train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y  # Ensures balanced split
    )
)

print(f"\nTraining: {len(X_train)} wells")
print(f"Testing : {len(X_test)} wells")

# ═══════════════════════════════════
# BUILD RANDOM FOREST CLASSIFIER
#
# WHY RANDOM FOREST?
# More powerful than single
# decision tree.
# Handles non-linear relationships.
# Provides feature importance.
# Widely used in petroleum ML.
# ═══════════════════════════════════

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42,
    class_weight="balanced"
)

rf_model.fit(X_train, y_train)
print("\nModel trained successfully.")

# ═══════════════════════════════════
# EVALUATE THE MODEL
# ═══════════════════════════════════

y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
cv_scores = cross_val_score(
    rf_model, X, y, cv=5, scoring="accuracy"
)

print(f"\n=== MODEL PERFORMANCE ===")
print(f"Test accuracy    : {accuracy:.3f}")
print(f"Cross-val scores : {cv_scores.round(3)}")
print(f"CV mean accuracy : {cv_scores.mean():.3f}")

print(f"\n=== CLASSIFICATION REPORT ===")
print(classification_report(
    y_test, y_pred,
    target_names=["No Intervention", "Needs Intervention"]
))

# ═══════════════════════════════════
# FEATURE IMPORTANCE
# Which factors most predict
# intervention need?
# ═══════════════════════════════════

importance_df = pd.DataFrame({
    "Feature": feature_columns,
    "Importance": rf_model.feature_importances_
}).sort_values("Importance", ascending=False)

print("\n=== FEATURE IMPORTANCE ===")
print("What most predicts intervention need:")
for _, row in importance_df.iterrows():
    bar = "█" * int(row["Importance"] * 50)
    print(f"  {row['Feature']:<25} "
          f"{row['Importance']:.3f} {bar}")

# ═══════════════════════════════════
# PREDICT ON NEW WELLS
# ═══════════════════════════════════

new_wells = pd.DataFrame({
    "Days_Producing": [90, 450, 1200, 730],
    "Water_Cut": [0.08, 0.42, 0.71, 0.28],
    "Production_Rate": [850, 320, 180, 550],
    "Pressure_Decline_Rate": [0.02, 0.08, 0.13, 0.05],
    "Sand_Production": [0, 1, 1, 0]
})

predictions = rf_model.predict(new_wells)
probabilities = rf_model.predict_proba(
    new_wells
)[:, 1]

print("\n=== INTERVENTION PREDICTIONS ===")
print("Well | Intervention? | Probability")
print("-" * 45)
for i, (pred, prob) in enumerate(
    zip(predictions, probabilities)
):
    status = (
        "⚠ YES — Schedule now"
        if pred == 1
        else "✓ NO — Continue monitoring"
    )
    print(f"Well {i+1:2d} | {status:<25} "
          f"| {prob:.1%}")

 # ═══════════════════════════════════
# CLASSIFICATION VISUALISATIONS
# ═══════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Chart 1: Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
im = axes[0].imshow(
    cm, interpolation="nearest",
    cmap="Blues"
)
axes[0].set_title(
    "Confusion Matrix",
    fontweight="bold"
)
axes[0].set_xlabel("Predicted Label")
axes[0].set_ylabel("True Label")
axes[0].set_xticks([0, 1])
axes[0].set_yticks([0, 1])
axes[0].set_xticklabels(
    ["No Intervention", "Intervention"]
)
axes[0].set_yticklabels(
    ["No Intervention", "Intervention"]
)

for i in range(2):
    for j in range(2):
        axes[0].text(
            j, i, str(cm[i, j]),
            ha="center", va="center",
            fontsize=14, fontweight="bold",
            color="white" if cm[i, j] > cm.max()/2
            else "black"
        )

# Chart 2: Feature Importance
colors = [
    "#2196F3" if i == 0
    else "#4CAF50" if i == 1
    else "#FF9800"
    for i in range(len(importance_df))
]
axes[1].barh(
    importance_df["Feature"],
    importance_df["Importance"],
    color=colors,
    edgecolor="black",
    linewidth=0.5
)
axes[1].set_title(
    "Feature Importance\n"
    "(What drives intervention need)",
    fontweight="bold"
)
axes[1].set_xlabel("Importance Score")

for i, (_, row) in enumerate(
    importance_df.iterrows()
):
    axes[1].text(
        row["Importance"] + 0.002,
        i,
        f"{row['Importance']:.3f}",
        va="center",
        fontsize=9
    )

# Chart 3: Probability Distribution
intervention = df_class[
    df_class["Needs_Intervention"] == 1
]["Water_Cut"]
no_intervention = df_class[
    df_class["Needs_Intervention"] == 0
]["Water_Cut"]

axes[2].hist(
    no_intervention,
    bins=20,
    alpha=0.6,
    color="#4CAF50",
    label="No Intervention",
    edgecolor="black",
    linewidth=0.3
)
axes[2].hist(
    intervention,
    bins=20,
    alpha=0.6,
    color="#F44336",
    label="Needs Intervention",
    edgecolor="black",
    linewidth=0.3
)
axes[2].set_title(
    "Water Cut Distribution\nby Intervention Status",
    fontweight="bold"
)
axes[2].set_xlabel("Water Cut")
axes[2].set_ylabel("Well Count")
axes[2].legend()

plt.suptitle(
    "Well Intervention Classification Model —"
    " Random Forest",
    fontsize=13,
    fontweight="bold",
    y=1.02
)
plt.tight_layout()
plt.savefig(
    "intervention_classifier.png",
    dpi=150,
    bbox_inches="tight"
)
plt.show()
print("Classification charts saved.")         