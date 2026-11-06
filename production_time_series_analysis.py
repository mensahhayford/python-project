import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path
import warnings

warnings.filterwarnings("default")
np.random.seed(42)


FIELD_NAME = "Northern Field"
WELL_NAME = "Well-001"
OIL_PRICE = 72.50
CURRENCY = "USD"
ANOMALY_THRESHOLD = 2.5
ROLLING_WINDOW = 30

OUTPUT_DIR = Path("project17_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# 1. GENERATE SYNTHETIC PRODUCTION TIME SERIES

def generate_production_data(n_days=1095):
    """
    Generate three years of synthetic daily
    oil production data for one petroleum well.
    """

    start_date = datetime(2021, 1, 1)

    dates = [
        start_date + timedelta(days=i)
        for i in range(n_days)
    ]

    day_number = np.arange(n_days)

    # Natural exponential production decline
    trend = 800 * np.exp(-0.0003 * day_number)

    # Seasonal variation
    day_of_year = np.array([
        date.timetuple().tm_yday
        for date in dates
    ])

    seasonal = 20 * np.sin(
        2 * np.pi * day_of_year / 365
    )

    # Simulated workover production improvements
    step_changes = np.zeros(n_days)
    step_changes[400:] += 80
    step_changes[750:] += 40

    # Simulated equipment-related anomalies
    anomaly_days = [120, 350, 600, 900, 1050]
    anomaly_magnitudes = [-150, -200, -120, -180, -100]

    anomalies = np.zeros(n_days)

    for day, magnitude in zip(
        anomaly_days, anomaly_magnitudes
    ):
        duration = np.random.randint(3, 8)

        anomalies[day:day + duration] = magnitude

    # Random operating noise
    noise = np.random.normal(0, 15, n_days)

    production = (
        trend
        + seasonal
        + step_changes
        + anomalies
        + noise
    ).clip(0, 1200)

    df = pd.DataFrame({
        "Date": pd.to_datetime(dates),
        "Production": production.round(1)
    })

    df = df.set_index("Date")

    return df


# ====================
# 2. DATA VALIDATION
# ====================

def validate_production_data(df):
    """Validate the production time series."""

    required_columns = ["Production"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(
            "The DataFrame index must be a DatetimeIndex."
        )

    if df.index.has_duplicates:
        raise ValueError(
            "Duplicate dates found in production data."
        )

    df = df.sort_index().copy()

    df["Production"] = pd.to_numeric(
        df["Production"],
        errors="coerce"
    )

    df["Production"] = df["Production"].replace(
        [np.inf, -np.inf], np.nan
    )

    df.loc[
        df["Production"] < 0,
        "Production"
    ] = np.nan

    missing_count = int(
        df["Production"].isna().sum()
    )

    if missing_count:
        df["Production"] = df["Production"].interpolate(
            method="time",
            limit_direction="both"
        )

    if df["Production"].isna().any():
        raise ValueError(
            "Production data contains unresolved missing values."
        )

    if len(df) < 90:
        raise ValueError(
            "At least 90 observations are required."
        )

    print("\n✓ Data validation completed")
    print(f"  Observations: {len(df)}")
    print(f"  Missing values handled: {missing_count}")

    return df


# ===================
# 3. MOVING AVERAGES
# ===================

def calculate_moving_averages(df):
    """
    Calculate trailing moving averages.

    Trailing windows use current and previous
    observations rather than future observations.
    """

    df = df.copy()

    df["MA_7"] = df["Production"].rolling(
        window=7,
        min_periods=7
    ).mean()

    df["MA_30"] = df["Production"].rolling(
        window=30,
        min_periods=30
    ).mean()

    df["MA_90"] = df["Production"].rolling(
        window=90,
        min_periods=90
    ).mean()

    print("✓ Moving averages calculated")

    return df


# ===============================
# 4. PRODUCTION DECLINE ANALYSIS
# ===============================

def calculate_decline_rate(df, window=30):
    """
    Calculate the percentage change in the
    30-day average production over a specified
    number of observations.

    Negative values indicate production decline.
    """

    df = df.copy()

    df["Production_Change_Pct"] = (
        df["MA_30"].pct_change(periods=window) * 100
    ).round(2)

    valid_values = (
        df["Production_Change_Pct"].dropna()
    )

    current_change = (
        valid_values.iloc[-1]
        if not valid_values.empty
        else np.nan
    )

    print("\n✓ Production change calculated")

    if pd.notna(current_change):
        print(
            f"  Latest {window}-observation change: "
            f"{current_change:.2f}%"
        )

    return df, current_change


# ==================================
# 5. EXPLORATORY ANOMALY DETECTION
# ==================================

def detect_anomalies(
    df,
    threshold=2.5,
    window=30
):
    """
    Detect observations outside rolling statistical
    limits using the rolling mean and standard deviation.

    These are exploratory anomaly limits, not validated
    engineering or formal SPC control limits.
    """

    df = df.copy()

    rolling_mean = df["Production"].rolling(
        window=window,
        min_periods=window
    ).mean()

    rolling_std = df["Production"].rolling(
        window=window,
        min_periods=window
    ).std()

    df["Rolling_Centre_Line"] = rolling_mean

    df["Upper_Control"] = (
        rolling_mean + threshold * rolling_std
    )

    df["Lower_Control"] = (
        rolling_mean - threshold * rolling_std
    ).clip(lower=0)

    df["Anomaly"] = (
        (df["Production"] > df["Upper_Control"])
        | (df["Production"] < df["Lower_Control"])
    ).fillna(False)

    anomaly_count = int(df["Anomaly"].sum())

    print("\n✓ Anomaly detection completed")
    print(f"  Anomalies detected: {anomaly_count}")

    if anomaly_count > 0:
        anomaly_dates = df.index[df["Anomaly"]]

        print(
            f"  First anomaly: {anomaly_dates[0].date()}"
        )

        print(
            f"  Latest anomaly: {anomaly_dates[-1].date()}"
        )

    return df, anomaly_count


# =========================
# 6. CUMULATIVE PRODUCTION
# =========================

def calculate_cumulative_production(df):
    """
    Calculate cumulative production from daily
    production rates, assuming one observation
    represents one day of production.
    """

    df = df.copy()

    df["Cumulative_Production"] = (
        df["Production"].cumsum()
    )

    total = df["Cumulative_Production"].iloc[-1]

    print("\n✓ Cumulative production calculated")

    print(
        f"  Total production: {total:,.1f} barrels"
    )

    return df


# ==================================
# 7. PRODUCTION PERFORMANCE METRICS
# ==================================
def calculate_performance_metrics(df):
    """Calculate key production performance indicators."""

    metrics = {}

    metrics["total_production"] = (
        df["Production"].sum()
    )

    metrics["average_production"] = (
        df["Production"].mean()
    )

    metrics["peak_production"] = (
        df["Production"].max()
    )

    metrics["minimum_production"] = (
        df["Production"].min()
    )

    metrics["current_rate"] = (
        df["MA_30"].iloc[-1]
    )

    metrics["peak_smoothed_rate"] = (
        df["MA_30"].max()
    )

    metrics["peak_smoothed_date"] = (
        df["MA_30"].idxmax()
    )

    metrics["current_vs_peak_pct"] = (
        metrics["current_rate"]
        / metrics["peak_smoothed_rate"]
        * 100
    )

    metrics["production_volatility"] = (
        df["Production"].std()
    )

    metrics["total_days"] = len(df)

    return metrics


# ========================
# 8. FINANCIAL ESTIMATION
# ========================

def calculate_financial_estimates(
    df,
    oil_price=OIL_PRICE
):
    """
    Calculate illustrative gross revenue.

    Assumes all daily production is oil and that
    each observation represents one day.

    This is not net profit or actual field economics.
    """

    total_production = df["Production"].sum()

    estimated_revenue = (
        total_production * oil_price
    )

    daily_revenue = (
        df["Production"] * oil_price
    )

    financial_metrics = {
        "oil_price": oil_price,
        "total_production": total_production,
        "estimated_gross_revenue": estimated_revenue,
        "average_daily_revenue": daily_revenue.mean()
    }

    return financial_metrics


# =============================
# 9. PRODUCTION EVENT ANALYSIS
# =============================

def identify_production_events(df):
    """
    Summarise dates identified by exploratory
    anomaly detection.
    """

    events = df[df["Anomaly"]].copy()

    event_summary = []

    for date, row in events.iterrows():

        event_summary.append({
            "Date": date.date(),
            "Production": row["Production"],
            "Rolling_Centre": row["Rolling_Centre_Line"],
            "Upper_Limit": row["Upper_Control"],
            "Lower_Limit": row["Lower_Control"]
        })

    return event_summary


# ================================
# 10. AUTOMATED REPORT GENERATION
# ================================

def generate_time_series_report(
    df,
    metrics,
    decline_change,
    anomaly_count,
    financial_metrics
):
    """Generate a detailed text report."""

    report_date = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_path = OUTPUT_DIR / (
        f"production_timeseries_report_{report_date}.txt"
    )

    total_production = metrics["total_production"]

    lines = []

    lines.append("=" * 65)
    lines.append("PETROLEUM PRODUCTION TIME SERIES ANALYSIS")
    lines.append("=" * 65)

    lines.append(f"\nField: {FIELD_NAME}")
    lines.append(f"Well: {WELL_NAME}")

    lines.append(
        f"Analysis Period: {df.index[0].date()} "
        f"to {df.index[-1].date()}"
    )

    lines.append(
        f"Observations: {metrics['total_days']}"
    )

    lines.append("\nPRODUCTION PERFORMANCE")
    lines.append("-" * 65)

    lines.append(
        f"Total Production: {total_production:,.1f} barrels"
    )

    lines.append(
        f"Average Daily Production: "
        f"{metrics['average_production']:,.2f} bbl/day"
    )

    lines.append(
        f"Peak Daily Production: "
        f"{metrics['peak_production']:,.2f} bbl/day"
    )

    lines.append(
        f"Minimum Daily Production: "
        f"{metrics['minimum_production']:,.2f} bbl/day"
    )

    lines.append(
        f"Latest 30-Day Average: "
        f"{metrics['current_rate']:,.2f} bbl/day"
    )

    lines.append(
        f"Peak 30-Day Average: "
        f"{metrics['peak_smoothed_rate']:,.2f} bbl/day"
    )

    lines.append(
        f"Latest Rate vs Peak: "
        f"{metrics['current_vs_peak_pct']:.2f}%"
    )

    lines.append("\nDECLINE ANALYSIS")
    lines.append("-" * 65)

    if pd.notna(decline_change):

        lines.append(
            f"Latest 30-observation change: "
            f"{decline_change:.2f}%"
        )

        if decline_change < -3:
            lines.append(
                "Assessment: Significant recent production decline."
            )

        elif decline_change < -1:
            lines.append(
                "Assessment: Moderate recent production decline."
            )

        elif decline_change < 0:
            lines.append(
                "Assessment: Mild recent production decline."
            )

        else:
            lines.append(
                "Assessment: Production increased over the comparison period."
            )

    else:
        lines.append(
            "Insufficient data for decline calculation."
        )

    lines.append("\nANOMALY ANALYSIS")
    lines.append("-" * 65)

    lines.append(
        f"Anomalies detected: {anomaly_count}"
    )

    lines.append(
        "Method: Rolling mean and standard deviation "
        f"with {ANOMALY_THRESHOLD} standard deviations."
    )

    lines.append(
        "Note: Exploratory statistical flags, not confirmed equipment failures."
    )

    lines.append("\nFINANCIAL ESTIMATION")
    lines.append("-" * 65)

    lines.append(
        f"Assumed oil price: ${financial_metrics['oil_price']:.2f}/bbl"
    )

    lines.append(
        f"Estimated gross revenue: "
        f"${financial_metrics['estimated_gross_revenue']:,.2f}"
    )

    lines.append(
        "Note: Revenue is illustrative and excludes operating costs, "
        "taxes, royalties, and other deductions."
    )

    lines.append("\nDATA AND MODEL LIMITATIONS")
    lines.append("-" * 65)

    lines.append(
        "1. The dataset is synthetic, not actual field production data."
    )

    lines.append(
        "2. Workovers and anomalies are simulated events."
    )

    lines.append(
        "3. Percentage changes are not fitted reservoir decline curves."
    )

    lines.append(
        "4. Rolling anomaly limits are exploratory, not formal SPC limits."
    )

    lines.append(
        "5. Financial estimates use a simplified oil-price assumption."
    )

    lines.append(
        "6. Operational decisions require validation with real field data."
    )

    lines.append("\n" + "=" * 65)
    lines.append("END OF REPORT")
    lines.append("=" * 65)

    report_text = "\n".join(lines)

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_text)

    print("\n✓ Automated report generated")
    print(f"  Location: {report_path}")

    print("\n" + report_text)

    return report_path


# ========================
# 11. PRODUCTION DASHBOARD
# ========================

def generate_dashboard(
    df,
    metrics,
    anomaly_count
):
    """Generate a four-chart production dashboard."""

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    dashboard_path = OUTPUT_DIR / (
        f"production_dashboard_{timestamp}.png"
    )

    fig, axes = plt.subplots(
        4,
        1,
        figsize=(16, 18)
    )

    fig.suptitle(
        f"{FIELD_NAME} — {WELL_NAME}\n"
        "Production Time Series Analysis",
        fontsize=16,
        fontweight="bold"
    )

    # ---------------------------------------
    # CHART 1: PRODUCTION AND MOVING AVERAGES
    # ---------------------------------------

    axes[0].plot(
        df.index,
        df["Production"],
        color="#B0BEC5",
        linewidth=0.6,
        alpha=0.7,
        label="Daily Production"
    )

    axes[0].plot(
        df.index,
        df["MA_7"],
        color="#2196F3",
        linewidth=1.2,
        label="7-Day MA"
    )

    axes[0].plot(
        df.index,
        df["MA_30"],
        color="#4CAF50",
        linewidth=2,
        label="30-Day MA"
    )

    axes[0].plot(
        df.index,
        df["MA_90"],
        color="#FF9800",
        linewidth=2.2,
        label="90-Day MA"
    )

    axes[0].set_title(
        "Daily Production and Moving Averages"
    )

    axes[0].set_ylabel(
        "Production (bbl/day)"
    )

    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # --------------------------------------
    # CHART 2: EXPLORATORY ANOMALY DETECTION
    # --------------------------------------

    axes[1].plot(
        df.index,
        df["Production"],
        color="#90A4AE",
        linewidth=0.6,
        label="Daily Production"
    )

    axes[1].plot(
        df.index,
        df["Rolling_Centre_Line"],
        color="#2196F3",
        linewidth=1.8,
        label="Rolling Centre"
    )

    axes[1].fill_between(
        df.index,
        df["Lower_Control"],
        df["Upper_Control"],
        alpha=0.15,
        color="#4CAF50",
        label="Exploratory Rolling Limits"
    )

    anomaly_mask = df["Anomaly"]

    axes[1].scatter(
        df.index[anomaly_mask],
        df.loc[anomaly_mask, "Production"],
        color="#F44336",
        s=25,
        zorder=5,
        label=f"Flagged Observations ({anomaly_count})"
    )

    axes[1].set_title(
        "Rolling Statistical Anomaly Detection"
    )

    axes[1].set_ylabel(
        "Production (bbl/day)"
    )

    axes[1].legend()
    axes[1].grid(alpha=0.3)

    # ------------------------------
    # CHART 3: CUMULATIVE PRODUCTION
    # ------------------------------

    cumulative = (
        df["Cumulative_Production"] / 1_000_000
    )

    axes[2].fill_between(
        df.index,
        cumulative,
        alpha=0.3,
        color="#2196F3"
    )

    axes[2].plot(
        df.index,
        cumulative,
        color="#1565C0",
        linewidth=2
    )

    axes[2].set_title(
        "Cumulative Production"
    )

    axes[2].set_ylabel(
        "Million Barrels"
    )

    axes[2].grid(alpha=0.3)

    # --------------------------
    # CHART 4: PRODUCTION CHANGE
    # --------------------------

    axes[3].plot(
        df.index,
        df["Production_Change_Pct"],
        color="#7E57C2",
        linewidth=1.2,
        label="30-Observation Percentage Change"
    )

    axes[3].axhline(
        0,
        color="black",
        linewidth=1,
        linestyle="--"
    )

    axes[3].set_title(
        "Production Percentage Change"
    )

    axes[3].set_ylabel(
        "Change (%)"
    )

    axes[3].set_xlabel(
        "Date"
    )

    axes[3].legend()
    axes[3].grid(alpha=0.3)

    plt.tight_layout(
        rect=[0, 0, 1, 0.97]
    )

    plt.savefig(
        dashboard_path,
        dpi=160,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("\n✓ Dashboard generated")
    print(f"  Location: {dashboard_path}")

    return dashboard_path


# ===================
# 12. MASTER PIPELINE
# ===================

def run_pipeline():
    """Execute the complete production analysis."""

    print("\n" + "=" * 65)
    print("PETROLEUM PRODUCTION TIME SERIES PIPELINE")
    print("=" * 65)

    print("\nSTAGE 1: DATA GENERATION")

    df = generate_production_data()

    print(
        f"✓ Generated {len(df)} daily observations"
    )

    print(
        f"  Period: {df.index[0].date()} "
        f"to {df.index[-1].date()}"
    )

    print("\nSTAGE 2: DATA VALIDATION")

    df = validate_production_data(df)

    print("\nSTAGE 3: MOVING AVERAGES")

    df = calculate_moving_averages(df)

    print("\nSTAGE 4: DECLINE ANALYSIS")

    df, decline_change = calculate_decline_rate(
        df,
        window=ROLLING_WINDOW
    )

    print("\nSTAGE 5: ANOMALY DETECTION")

    df, anomaly_count = detect_anomalies(
        df,
        threshold=ANOMALY_THRESHOLD,
        window=ROLLING_WINDOW
    )

    print("\nSTAGE 6: CUMULATIVE PRODUCTION")

    df = calculate_cumulative_production(df)

    print("\nSTAGE 7: PERFORMANCE METRICS")

    metrics = calculate_performance_metrics(df)

    print("\nSTAGE 8: FINANCIAL ESTIMATION")

    financial_metrics = calculate_financial_estimates(
        df,
        oil_price=OIL_PRICE
    )

    print("\nSTAGE 9: EVENT ANALYSIS")

    events = identify_production_events(df)

    print(
        f"✓ {len(events)} flagged observations summarised"
    )

    print("\nSTAGE 10: AUTOMATED REPORT")

    report_path = generate_time_series_report(
        df,
        metrics,
        decline_change,
        anomaly_count,
        financial_metrics
    )

    print("\nSTAGE 11: DASHBOARD GENERATION")

    dashboard_path = generate_dashboard(
        df,
        metrics,
        anomaly_count
    )

    # Save complete analytical dataset
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    csv_path = OUTPUT_DIR / (
        f"production_analysis_{timestamp}.csv"
    )

    df.to_csv(csv_path)

    print("\n✓ Processed dataset saved")
    print(f"  Location: {csv_path}")

    print("\n" + "=" * 65)
    print("PIPELINE EXECUTION COMPLETED")
    print("=" * 65)

    print(f"\nField: {FIELD_NAME}")
    print(f"Well: {WELL_NAME}")

    print(
        f"Total production: "
        f"{metrics['total_production']:,.1f} barrels"
    )

    print(
        f"Average daily production: "
        f"{metrics['average_production']:,.2f} bbl/day"
    )

    print(
        f"Latest 30-day average: "
        f"{metrics['current_rate']:,.2f} bbl/day"
    )

    print(
        f"Flagged observations: {anomaly_count}"
    )

    print(f"\nReport: {report_path}")
    print(f"Dashboard: {dashboard_path}")
    print(f"Dataset: {csv_path}")

    print("\n" + "=" * 65)

    return df, metrics, events


# =========
# EXECUTION
# =========

if __name__ == "__main__":

    df_ts, performance_metrics, detected_events = (
        run_pipeline()
    )