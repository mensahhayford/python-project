import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

print("="*60)
print("  PETROLEUM FIELD ML ANALYSIS PIPELINE")
print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)


# STAGE 1: DATA INGESTION

def ingest_data(filepath=None):
    """
    Load data from CSV or generate sample data.
    Returns raw DataFrame and ingestion report.
    """
    print("\n[STAGE 1] Data Ingestion...")

    def _generate_sample_data():
        np.random.seed(42)
        n = 60
        data = {
            "Well_Name": [
                f"Well_{chr(65+i//10)}{i%10+1:02d}"
                for i in range(n)
            ],
            "Location": np.random.choice(
                ["Northern Block","Southern Block",
                 "Eastern Block","Western Block"],
                n, p=[0.35,0.30,0.20,0.15]
            ),
            "Type": np.random.choice(
                ["Oil","Gas Condensate"],
                n, p=[0.75,0.25]
            ),
            "Avg_Daily_Barrels": np.random.normal(
                450,200,n
            ).clip(50,1100).round(1),
            "Water_Cut": np.random.beta(2,5,n).round(3),
            "Days_Active": np.random.randint(90,1500,n),
            "Pressure_Decline": np.random.uniform(
                0.01,0.15,n
            ).round(4),
            "Sand_Production": np.random.choice(
                [0,1],n,p=[0.75,0.25]
            )
        }
        df = pd.DataFrame(data)
        idx = np.random.choice(n,5,replace=False)
        df.loc[idx[:3],"Water_Cut"] = np.nan
        df.loc[idx[3:],"Pressure_Decline"] = np.nan
        df.loc[0,"Water_Cut"] = 1.45 
        df.loc[1,"Avg_Daily_Barrels"] = -50 
        df = pd.concat(
            [df, df.iloc[[5]]], ignore_index=True
        ) 
        return df, "Generated sample dataset"

    if filepath:
        try:
            df = pd.read_csv(filepath)
            source = filepath
        except FileNotFoundError:
            print(f"  File not found: {filepath}")
            print("  Falling back to sample data...")
            df, source = _generate_sample_data()
    else:
        df, source = _generate_sample_data()

    report = {
        "source": source,
        "rows_loaded": len(df),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum()
    }

    print(f"  Source     : {source}")
    print(f"  Rows loaded: {report['rows_loaded']}")
    print(f"  Columns    : {len(report['columns'])}")
    print(f"  Missing    : {sum(report['missing_values'].values())}")
    print(f"  Duplicates : {report['duplicates']}")

    return df, report


# STAGE 2: DATA CLEANING

def clean_data(df):
    """
    Complete data cleaning pipeline.
    Returns clean DataFrame and cleaning log.
    """
    print("\n[STAGE 2] Data Cleaning...")

    dc = df.copy()
    log = []

    before = len(dc)
    dc = dc.drop_duplicates()
    removed = before - len(dc)
    if removed > 0:
        log.append(f"Removed {removed} duplicate rows")


    dc["Avg_Daily_Barrels"] = pd.to_numeric(
        dc["Avg_Daily_Barrels"], errors="coerce"
    )


    n_neg = (dc["Avg_Daily_Barrels"] < 0).sum()
    dc.loc[dc["Avg_Daily_Barrels"] < 0,
           "Avg_Daily_Barrels"] = np.nan
    if n_neg > 0:
        log.append(f"Fixed {n_neg} negative production values")

    n_wc = (dc["Water_Cut"] > 1.0).sum()
    dc.loc[dc["Water_Cut"] > 1.0, "Water_Cut"] = np.nan
    if n_wc > 0:
        log.append(f"Fixed {n_wc} impossible water cut values")


    for col in ["Avg_Daily_Barrels","Water_Cut","Pressure_Decline"]:
        n_miss = dc[col].isnull().sum()
        if n_miss > 0:
            med = dc[col].median()
            dc[col] = dc[col].fillna(med)
            log.append(
                f"Filled {n_miss} missing {col} "
                f"with median ({med:.3f})"
            )

    
    dc["Location"] = dc["Location"].str.strip().str.title()

    for item in log:
        print(f"  + {item}")
    print(f"  Clean rows : {len(dc)}")

    return dc, log


# STAGE 3: FEATURE ENGINEERING

def engineer_features(df):
    """
    Create derived features for analysis.
    Returns enriched DataFrame.
    """
    print("\n[STAGE 3] Feature Engineering...")


    df["Total_Production"] = (
        df["Avg_Daily_Barrels"] * df["Days_Active"]
    ).round(0)


    prod_norm = (
        df["Avg_Daily_Barrels"] /
        df["Avg_Daily_Barrels"].max()
    )
    df["Efficiency_Score"] = (
        prod_norm * 60 + (1 - df["Water_Cut"]) * 40
    ).round(1)


    def classify_risk(row):
        if row["Water_Cut"] > 0.60:
            return "CRITICAL"
        elif (row["Water_Cut"] > 0.40 or
              row["Pressure_Decline"] > 0.10 or
              row["Avg_Daily_Barrels"] < 150):
            return "HIGH"
        elif row["Water_Cut"] > 0.25:
            return "MEDIUM"
        else:
            return "LOW"

    df["Risk_Level"] = df.apply(classify_risk, axis=1)

    dist = df["Risk_Level"].value_counts()
    print(f"  Features   : Total_Production, Efficiency_Score, Risk_Level")
    print(f"  Risk dist  : " +
          " | ".join(f"{k}:{v}" for k,v in dist.items()))

    return df


# STAGE 4: ML CLUSTERING

def run_clustering(df, max_k=6):
    """
    K-Means clustering with automatic K selection.
    Returns DataFrame with cluster labels.
    """
    print("\n[STAGE 4] ML Clustering Analysis...")

    features = [
        "Avg_Daily_Barrels","Water_Cut",
        "Pressure_Decline","Days_Active"
    ]

    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)


    best_k, best_score = 3, -1
    for k in range(2, min(max_k+1, len(df)//5)):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        if score > best_score:
            best_score, best_k = score, k

    
    final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    df["Cluster"] = final.fit_predict(X_scaled)

    
    stats = df.groupby("Cluster").agg(
        Avg_Prod=("Avg_Daily_Barrels","mean"),
        Avg_WC=("Water_Cut","mean")
    )

    def name_cluster(row):
        if row["Avg_Prod"] > 600:
            return "HIGH PERFORMER"
        elif row["Avg_WC"] > 0.45:
            return "DECLINING"
        elif row["Avg_Prod"] < 250:
            return "LOW PRODUCER"
        else:
            return "STABLE PRODUCER"

    stats["Name"] = stats.apply(name_cluster, axis=1)
    name_map = stats["Name"].to_dict()
    df["Cluster_Name"] = df["Cluster"].map(name_map)

    print(f"  Optimal K        : {best_k}")
    print(f"  Silhouette score : {best_score:.3f}")
    for cid, name in name_map.items():
        count = (df["Cluster"] == cid).sum()
        print(f"  Cluster {cid} ({name}): {count} wells")

    return df, best_k, name_map


# STAGE 5: STATISTICAL ANALYSIS

def analyse_field(df, oil_price=72.50, opex_per_bbl=22.00):
    """
    Complete field-level statistical analysis.
    Returns results dictionary.
    """
    print("\n[STAGE 5] Statistical Analysis...")

    r = {}


    r["total_daily_production"] = df["Avg_Daily_Barrels"].sum()
    r["active_production"] = df[
        df["Risk_Level"] != "CRITICAL"
    ]["Avg_Daily_Barrels"].sum()
    r["field_average"] = df["Avg_Daily_Barrels"].mean()


    daily_rev  = r["total_daily_production"] * oil_price
    daily_opex = r["total_daily_production"] * opex_per_bbl
    r["daily_revenue"] = daily_rev
    r["daily_profit"]  = daily_rev - daily_opex
    r["annual_profit"] = r["daily_profit"] * 365 / 1_000_000


    r["risk_counts"]    = df["Risk_Level"].value_counts().to_dict()
    r["critical_wells"] = df[
        df["Risk_Level"] == "CRITICAL"
    ]["Well_Name"].tolist()


    r["block_summary"] = df.groupby("Location").agg(
        Wells=("Well_Name","count"),
        Avg_Production=("Avg_Daily_Barrels","mean"),
        Total_Production=("Avg_Daily_Barrels","sum"),
        Avg_Water_Cut=("Water_Cut","mean"),
        Avg_Efficiency=("Efficiency_Score","mean")
    ).round(2).reset_index()

    r["cluster_summary"] = df.groupby(
        ["Cluster","Cluster_Name"]
    ).agg(
        Count=("Well_Name","count"),
        Avg_Production=("Avg_Daily_Barrels","mean"),
        Avg_Water_Cut=("Water_Cut","mean"),
        Avg_Efficiency=("Efficiency_Score","mean")
    ).round(2).reset_index()

    print(f"  Total production : {r['total_daily_production']:,.0f} bbl/day")
    print(f"  Daily profit     : ${r['daily_profit']:,.0f}")
    print(f"  Annual profit    : ${r['annual_profit']:.1f}M")
    print(f"  Critical wells   : {len(r['critical_wells'])}")

    return r


# STAGE 6: AUTOMATED REPORT

def generate_pipeline_report(df, results,
                             field_name="Alpha Field",
                             oil_price=72.50):
    """
    Generate complete executive report from pipeline results.
    """
    print("\n[STAGE 6] Generating Report...")

    now = datetime.now()
    ts  = now.strftime("%Y%m%d_%H%M")
    ds  = now.strftime("%d %B %Y %H:%M")

    sep  = "=" * 65
    dash = "-" * 65

    symbols = {"CRITICAL":"X","HIGH":"!","MEDIUM":"~","LOW":"OK"}
    risk_lines = ""
    for level in ["CRITICAL","HIGH","MEDIUM","LOW"]:
        count = results["risk_counts"].get(level, 0)
        risk_lines += f"\n  [{symbols[level]}] {level:<10}: {count} wells"


    crit_section = ""
    if results["critical_wells"]:
        crit_section = (
            "\n\n  Wells requiring immediate attention:"
        )
        for w in results["critical_wells"]:
            crit_section += f"\n    -> {w}"


    recs = ""
    rn = 1
    if results["critical_wells"]:
        recs += (
            f"\n  {rn}. URGENT — Immediate review of "
            f"{len(results['critical_wells'])} critical wells."
            f"\n     Schedule intervention within 7 days."
        )
        rn += 1
    high = results["risk_counts"].get("HIGH", 0)
    if high > 0:
        recs += (
            f"\n  {rn}. Schedule workover review for "
            f"{high} high-risk wells this quarter."
        )
        rn += 1
    best_block = results["block_summary"].loc[
        results["block_summary"]["Avg_Production"].idxmax(),
        "Location"
    ]
    recs += (
        f"\n  {rn}. Prioritise development in "
        f"{best_block} — highest average production."
    )

    report = f"""
{sep}
       AUTOMATED FIELD INTELLIGENCE REPORT
{sep}
  Field         : {field_name}
  Report Date   : {ds}
  Wells Analysed: {len(df)}
  Oil Price     : ${oil_price}/bbl
  Pipeline Ver  : 1.0
{sep}

EXECUTIVE SUMMARY
{dash}
  Total Production : {results["total_daily_production"]:>8,.0f} bbl/day
  Daily Revenue    : {results["daily_revenue"]:>8,.0f} USD
  Daily Profit     : {results["daily_profit"]:>8,.0f} USD
  Annual Profit    : {results["annual_profit"]:>8.1f}M USD
  Critical Wells   : {len(results["critical_wells"]):>8}
  Field Efficiency : {df["Efficiency_Score"].mean():>8.1f}/100
{dash}

RISK SUMMARY
{dash}{risk_lines}{crit_section}

ML CLUSTER ANALYSIS
{dash}
{results["cluster_summary"].to_string(index=False)}

BLOCK PERFORMANCE
{dash}
{results["block_summary"].to_string(index=False)}

RECOMMENDATIONS
{dash}{recs}

{sep}
  Report generated : {ds}
  System           : Automated ML Pipeline v1.0
  Classification   : Internal — Operations Use
{sep}
"""

    filename = f"pipeline_report_{ts}.txt"
    with open(filename, "w") as f:
        f.write(report)

    print(report)
    print(f"  Report saved: {filename}")

    return report, filename



# STAGE 7: DASHBOARD VISUALISATION

def generate_dashboard(df, results):
    """Generate 6-chart field intelligence dashboard."""
    print("\n[STAGE 7] Generating Dashboard...")

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle(
        "Petroleum Field Intelligence Dashboard\n"
        f"Generated: {datetime.now().strftime('%d %B %Y %H:%M')}",
        fontsize=14, fontweight="bold"
    )

    colours = ["#2196F3","#4CAF50","#FF9800","#F44336","#9C27B0"]


    cp = results["cluster_summary"].sort_values(
        "Avg_Production", ascending=False
    )
    axes[0,0].bar(
        range(len(cp)),
        cp["Avg_Production"],
        color=colours[:len(cp)],
        edgecolor="black", linewidth=0.5
    )
    axes[0,0].set_xticks(range(len(cp)))
    axes[0,0].set_xticklabels(
        cp["Cluster_Name"], rotation=15, ha="right", fontsize=8
    )
    axes[0,0].set_title("Avg Production by Cluster",
                        fontweight="bold")
    axes[0,0].set_ylabel("Avg Production (bbl/day)")
    axes[0,0].grid(alpha=0.3, axis="y")


    risk_order = ["CRITICAL","HIGH","MEDIUM","LOW"]
    risk_cols  = {"CRITICAL":"#F44336","HIGH":"#FF9800",
                  "MEDIUM":"#FFC107","LOW":"#4CAF50"}
    rc = results["risk_counts"]
    labels = [r for r in risk_order if r in rc]
    sizes  = [rc[r] for r in labels]
    pcols  = [risk_cols[r] for r in labels]
    axes[0,1].pie(
        sizes, labels=labels, colors=pcols,
        autopct="%1.1f%%", startangle=90,
        textprops={"fontsize":9}
    )
    axes[0,1].set_title("Well Risk Distribution", fontweight="bold")


    for i, cid in enumerate(
        sorted(df["Cluster"].unique())
    ):
        mask = df["Cluster"] == cid
        name = df.loc[mask,"Cluster_Name"].iloc[0]
        axes[0,2].scatter(
            df.loc[mask,"Water_Cut"]*100,
            df.loc[mask,"Avg_Daily_Barrels"],
            c=colours[i%len(colours)],
            label=name, alpha=0.7, s=50,
            edgecolors="black", linewidth=0.3
        )
    axes[0,2].set_title("Production vs Water Cut by Cluster",
                        fontweight="bold")
    axes[0,2].set_xlabel("Water Cut (%)")
    axes[0,2].set_ylabel("Production (bbl/day)")
    axes[0,2].legend(fontsize=7)
    axes[0,2].grid(alpha=0.3)


    bs = results["block_summary"].sort_values(
        "Total_Production"
    )
    axes[1,0].barh(
        bs["Location"], bs["Total_Production"],
        color="#2196F3", edgecolor="black", linewidth=0.5
    )
    axes[1,0].set_title("Total Production by Block",
                        fontweight="bold")
    axes[1,0].set_xlabel("Total Production (bbl/day)")
    axes[1,0].grid(alpha=0.3, axis="x")


    axes[1,1].hist(
        df["Efficiency_Score"], bins=20,
        color="#4CAF50", edgecolor="black",
        linewidth=0.3, alpha=0.8
    )
    mean_eff = df["Efficiency_Score"].mean()
    axes[1,1].axvline(
        mean_eff, color="red", linestyle="--",
        linewidth=2, label=f"Mean: {mean_eff:.1f}"
    )
    axes[1,1].set_title("Well Efficiency Score Distribution",
                        fontweight="bold")
    axes[1,1].set_xlabel("Efficiency Score (0–100)")
    axes[1,1].set_ylabel("Well Count")
    axes[1,1].legend()
    axes[1,1].grid(alpha=0.3)


    risk_present = [r for r in risk_order
                    if r in df["Risk_Level"].values]
    box_data = [
        df[df["Risk_Level"]==r]["Water_Cut"]*100
        for r in risk_present
    ]
    bp = axes[1,2].boxplot(
        box_data, labels=risk_present,
        patch_artist=True
    )
    box_colours = ["#4CAF50","#FFC107","#FF9800","#F44336"]
    for patch, col in zip(bp["boxes"],
                          box_colours[:len(box_data)]):
        patch.set_facecolor(col)
        patch.set_alpha(0.7)
    axes[1,2].set_title("Water Cut by Risk Level",
                        fontweight="bold")
    axes[1,2].set_ylabel("Water Cut (%)")
    axes[1,2].grid(alpha=0.3, axis="y")

    plt.tight_layout()
    dash_file = (
        f"field_dashboard_"
        f"{datetime.now().strftime('%Y%m%d_%H%M')}.png"
    )
    plt.savefig(dash_file, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  Dashboard saved: {dash_file}")

    return dash_file


# MASTER RUNNER

def run_pipeline(filepath=None,
                 field_name="Alpha Field",
                 oil_price=72.50):
    """
    Execute the complete 7-stage ML pipeline.
    One function call — full automation.

    Parameters
    ----------
    filepath   : str, optional
        Path to your CSV well data file.
        If None or not found, uses built-in
        sample data so the pipeline always runs.
    field_name : str
        Display name used in the report.
    oil_price  : float
        Current oil price in USD/bbl.

    Returns
    -------
    df_final   : DataFrame — fully processed well data
    results    : dict — all analysis outputs
    """
    print(f"\nField  : {field_name}")
    print(f"Price  : ${oil_price}/bbl\n")

    df_raw,  _     = ingest_data(filepath)
    df_clean, _    = clean_data(df_raw)
    df_feat        = engineer_features(df_clean)
    df_clust, n_k, cmap = run_clustering(df_feat)
    results        = analyse_field(df_clust, oil_price)
    _, rpt_file    = generate_pipeline_report(
                         df_clust, results,
                         field_name, oil_price)
    dash_file      = generate_dashboard(df_clust, results)

    print("\n" + "="*60)
    print("  PIPELINE COMPLETE")
    print(f"  Stages     : 7 / 7")
    print(f"  Wells      : {len(df_clust)}")
    print(f"  Clusters   : {n_k}")
    print(f"  Report     : {rpt_file}")
    print(f"  Dashboard  : {dash_file}")
    print("="*60)

    return df_clust, results


if __name__ == "__main__":
    df_final, field_results = run_pipeline(
        filepath=None, 
        field_name="Northern Field Operations",
        oil_price=72.50
    )