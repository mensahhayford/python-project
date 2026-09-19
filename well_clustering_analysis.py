import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

np.random.seed(42)

# ═══════════════════════════════════
# THE PROBLEM:
# We have 80 wells across a field.
# We don't know in advance how many
# "types" of wells exist.
# We want the data to tell us.
#
# REAL INDUSTRY VALUE:
# Different well types need different
# management strategies.
# A well in decline needs different
# intervention than a stable producer.
# Finding these groups automatically
# helps operations teams prioritise.
# ═══════════════════════════════════

n_wells = 80

# Simulate three distinct well types
# that we want the algorithm to "discover"

# Type 1: High producers, low water cut
# (25 wells)
type1_prod = np.random.normal(800, 80, 25)
type1_wc = np.random.normal(0.10, 0.03, 25)
type1_pressure = np.random.normal(0.02, 0.005, 25)
type1_days = np.random.normal(400, 60, 25)

# Type 2: Medium producers, rising water cut
# (30 wells)
type2_prod = np.random.normal(450, 70, 30)
type2_wc = np.random.normal(0.35, 0.05, 30)
type2_pressure = np.random.normal(0.07, 0.01, 30)
type2_days = np.random.normal(700, 80, 30)

# Type 3: Low producers, high water cut
# (25 wells)
type3_prod = np.random.normal(180, 40, 25)
type3_wc = np.random.normal(0.65, 0.08, 25)
type3_pressure = np.random.normal(0.12, 0.02, 25)
type3_days = np.random.normal(1100, 100, 25)

# Combine all wells
production = np.concatenate([
    type1_prod, type2_prod, type3_prod
])
water_cut = np.clip(
    np.concatenate([
        type1_wc, type2_wc, type3_wc
    ]), 0, 1
)
pressure_decline = np.concatenate([
    type1_pressure, type2_pressure,
    type3_pressure
])
days_producing = np.concatenate([
    type1_days, type2_days, type3_days
])

well_names = [f"Well_{i:03d}"
              for i in range(1, n_wells + 1)]

df_cluster = pd.DataFrame({
    "Well_Name": well_names,
    "Production_Rate": production.round(1),
    "Water_Cut": water_cut.round(3),
    "Pressure_Decline": pressure_decline.round(4),
    "Days_Producing": days_producing.round(0)
})

print("=== WELL DATASET FOR CLUSTERING ===")
print(df_cluster.describe().round(2))
print(f"\n{n_wells} wells, no labels —")
print("algorithm will find the groups.")

# ═══════════════════════════════════
# STEP 1: SCALE THE FEATURES
# ═══════════════════════════════════

features = [
    "Production_Rate",
    "Water_Cut",
    "Pressure_Decline",
    "Days_Producing"
]

X = df_cluster[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("\nFeatures scaled successfully.")
print(f"Scaled array shape: {X_scaled.shape}")

# ═══════════════════════════════════
# STEP 2: FIND OPTIMAL K
# ═══════════════════════════════════

inertias = []
silhouette_scores = []
k_range = range(2, 9)

for k in k_range:
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    score = silhouette_score(
        X_scaled, kmeans.labels_
    )
    silhouette_scores.append(score)

print("\n=== OPTIMAL K SEARCH ===")
print(f"{'K':>3} | {'Inertia':>10} | "
      f"{'Silhouette':>10}")
print("-" * 30)
for k, inertia, sil in zip(
    k_range, inertias, silhouette_scores
):
    print(f"{k:>3} | {inertia:>10.1f} | "
          f"{sil:>10.4f}")

best_k = k_range[
    silhouette_scores.index(max(silhouette_scores))
]
print(f"\nBest K by silhouette score: {best_k}")

# ═══════════════════════════════════
# STEP 3: FIT THE FINAL MODEL
# ═══════════════════════════════════

final_kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)
final_kmeans.fit(X_scaled)
df_cluster["Cluster"] = final_kmeans.labels_

# ═══════════════════════════════════
# STEP 4: ANALYSE THE CLUSTERS
# What did the algorithm find?
# ═══════════════════════════════════

print(f"\n=== CLUSTER ANALYSIS ===")
print(f"Algorithm found {best_k} distinct well types\n")

cluster_summary = df_cluster.groupby(
    "Cluster"
).agg(
    Well_Count=("Well_Name", "count"),
    Avg_Production=("Production_Rate", "mean"),
    Avg_Water_Cut=("Water_Cut", "mean"),
    Avg_Pressure_Decline=("Pressure_Decline", "mean"),
    Avg_Days_Producing=("Days_Producing", "mean")
).round(3)

print(cluster_summary.to_string())

# Name clusters by their characteristics
def name_cluster(row):
    if row["Avg_Production"] > 600:
        return "HIGH PERFORMER"
    elif row["Avg_Water_Cut"] > 0.50:
        return "DECLINING — REVIEW"
    else:
        return "STABLE PRODUCER"

cluster_summary["Classification"] = (
    cluster_summary.apply(name_cluster, axis=1)
)

print("\n=== CLUSTER CLASSIFICATIONS ===")
for cluster_id, row in cluster_summary.iterrows():
    print(f"\nCluster {cluster_id}: "
          f"{row['Classification']}")
    print(f"  Wells     : {row['Well_Count']:.0f}")
    print(f"  Production: "
          f"{row['Avg_Production']:.0f} bbl/day")
    print(f"  Water cut : "
          f"{row['Avg_Water_Cut']*100:.1f}%")
    print(f"  Pressure  : "
          f"{row['Avg_Pressure_Decline']*100:.1f}%/mo")