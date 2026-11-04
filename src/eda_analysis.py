"""Exploratory analysis for the Week 2 apparel retail internship task.

Run from the repository root:
    pip install -r requirements.txt
    python src/eda_analysis.py

The source CSV is fetched from the public dataset repository. Missing values are
preserved (never silently replaced with zero), and extreme observations are
flagged for review rather than deleted.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SOURCE_URL = (
    "https://raw.githubusercontent.com/Ishita95-AIML/"
    "-Fashion-Retail-Sales-Dataset/main/Fashion_Retail_Sales.csv"
)
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = ROOT / "visualizations"

AMOUNT = "Purchase Amount (USD)"
RATING = "Review Rating"
DATE = "Date Purchase"
ITEM = "Item Purchased"
PAYMENT = "Payment Method"


def load_data(source_url: str = SOURCE_URL) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the original CSV and return (raw, typed_analysis_copy)."""
    raw = pd.read_csv(
        source_url,
        encoding="utf-8",
        dtype={"Customer Reference ID": "string"},
    )
    df = raw.copy()
    df[AMOUNT] = pd.to_numeric(df[AMOUNT], errors="coerce")
    df[RATING] = pd.to_numeric(df[RATING], errors="coerce")
    df[DATE] = pd.to_datetime(
        df[DATE], format="%d-%m-%Y", errors="coerce"
    )
    return raw, df


def profile_and_summaries(df: pd.DataFrame) -> dict[str, Any]:
    """Calculate quality counts and grouped EDA results from typed data."""
    amount = df[AMOUNT].dropna()
    rating = df[RATING].dropna()
    q1 = float(amount.quantile(0.25))
    median = float(amount.median())
    q3 = float(amount.quantile(0.75))
    iqr = q3 - q1
    upper_fence = q3 + 1.5 * iqr
    complete = df[[AMOUNT, RATING]].dropna()

    month_key = df[DATE].dt.to_period("M").astype("string")
    monthly = (
        df.assign(Month=month_key)
        .groupby("Month", dropna=False)
        .agg(
            transaction_rows=(ITEM, "size"),
            amount_present=(AMOUNT, "count"),
            observed_amount_sum=(AMOUNT, "sum"),
        )
        .reset_index()
    )
    monthly.to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False)

    top_items = df[ITEM].value_counts().head(10)
    payment_counts = df[PAYMENT].value_counts()
    payment_summary = (
        df.groupby(PAYMENT)
        .agg(
            transaction_rows=(ITEM, "size"),
            amount_present=(AMOUNT, "count"),
            mean_observed_amount=(AMOUNT, "mean"),
            mean_review_rating=(RATING, "mean"),
        )
        .reset_index()
    )
    payment_summary.to_csv(OUTPUT_DIR / "payment_summary.csv", index=False)

    amount_outliers = amount[amount > upper_fence]
    extreme_amounts = amount[amount > 1000]

    summary: dict[str, Any] = {
        "source_url": SOURCE_URL,
        "records": int(len(df)),
        "columns": list(df.columns),
        "date_min": df[DATE].min().strftime("%Y-%m-%d"),
        "date_max": df[DATE].max().strftime("%Y-%m-%d"),
        "missing_values": {
            column: int(count)
            for column, count in df.isna().sum().items()
        },
        "purchase_amount": {
            "observed_count": int(amount.count()),
            "sum_usd": float(amount.sum()),
            "mean_usd": float(amount.mean()),
            "median_usd": median,
            "q1_usd": q1,
            "q3_usd": q3,
            "min_usd": float(amount.min()),
            "max_usd": float(amount.max()),
            "iqr_upper_fence_usd": float(upper_fence),
            "iqr_outlier_count": int(amount_outliers.count()),
            "above_1000_count": int(extreme_amounts.count()),
        },
        "review_rating": {
            "observed_count": int(rating.count()),
            "mean": float(rating.mean()),
            "median": float(rating.median()),
            "min": float(rating.min()),
            "max": float(rating.max()),
        },
        "amount_rating_complete_cases": int(len(complete)),
        "amount_rating_pearson_correlation": float(
            complete[AMOUNT].corr(complete[RATING])
        ),
        "payment_method_counts": {
            str(k): int(v) for k, v in payment_counts.items()
        },
        "top_items_by_row_count": {
            str(k): int(v) for k, v in top_items.items()
        },
        "monthly_summary": monthly.to_dict(orient="records"),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / "eda_summary.json").open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)
    return summary


def make_visualizations(df: pd.DataFrame, summary: dict[str, Any]) -> None:
    """Create the four chart types discussed in the report (PNG and SVG)."""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def save(fig: plt.Figure, name: str) -> None:
        fig.tight_layout()
        fig.savefig(FIGURE_DIR / f"{name}.png", dpi=180, bbox_inches="tight")
        fig.savefig(FIGURE_DIR / f"{name}.svg", bbox_inches="tight")
        plt.close(fig)

    amount = df[AMOUNT].dropna()
    q1 = amount.quantile(0.25)
    q3 = amount.quantile(0.75)
    upper_fence = q3 + 1.5 * (q3 - q1)
    flagged = int((amount > upper_fence).sum())

    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.boxplot(amount, vert=False, showfliers=False)
    ax.set_title("Purchase amount distribution — central range")
    ax.set_xlabel("Purchase amount (USD)")
    ax.grid(axis="x", alpha=0.25)
    ax.text(
        0.02,
        -0.28,
        f"{flagged} values lie beyond the 1.5×IQR upper fence; investigate separately.",
        transform=ax.transAxes,
        fontsize=9,
    )
    save(fig, "purchase_amount_boxplot")

    top_items = df[ITEM].value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.barh(top_items.index, top_items.values)
    ax.set_title("Top purchased item names by transaction-row count")
    ax.set_xlabel("Number of rows")
    ax.grid(axis="x", alpha=0.25)
    for index, value in enumerate(top_items.values):
        ax.text(value + 0.5, index, str(value), va="center", fontsize=8)
    save(fig, "top_items")

    monthly = pd.DataFrame(summary["monthly_summary"])
    monthly["Month"] = pd.PeriodIndex(monthly["Month"], freq="M").to_timestamp()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(
        monthly["Month"],
        monthly["observed_amount_sum"],
        marker="o",
        linewidth=2,
    )
    ax.set_title("Observed purchase-amount total by month")
    ax.set_ylabel("Sum of non-missing amounts (USD)")
    ax.set_xlabel("Purchase month")
    ax.grid(axis="y", alpha=0.25)
    ax.tick_params(axis="x", rotation=35)
    if len(monthly) and monthly.iloc[-1]["transaction_rows"] < 20:
        last = monthly.iloc[-1]
        ax.annotate(
            f"Partial month: {int(last['transaction_rows'])} records",
            xy=(last["Month"], last["observed_amount_sum"]),
            xytext=(-150, 35),
            textcoords="offset points",
            arrowprops={"arrowstyle": "->"},
            fontsize=8,
        )
    save(fig, "monthly_observed_amount")

    payment_counts = df[PAYMENT].value_counts()
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    wedges, _, _ = ax.pie(
        payment_counts.values,
        startangle=90,
        autopct="%1.1f%%",
        wedgeprops={"width": 0.42, "edgecolor": "white"},
        pctdistance=0.78,
    )
    ax.legend(
        wedges,
        [f"{name}: {value:,}" for name, value in payment_counts.items()],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=2,
        frameon=False,
    )
    ax.set_title("Payment method mix")
    save(fig, "payment_method_mix")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw, df = load_data()
    if len(df) != 3400:
        print(f"Notice: source file now has {len(df):,} rows; report snapshot used 3,400.")
    if df[DATE].isna().any():
        raise ValueError("Some purchase dates could not be parsed; inspect source values.")

    summary = profile_and_summaries(df)
    make_visualizations(df, summary)
    print(f"Loaded {len(raw):,} records and {len(raw.columns)} columns.")
    print(f"Missing values: {summary['missing_values']}")
    print(f"Purchase amount summary: {summary['purchase_amount']}")
    print(
        "Pearson correlation (amount vs rating; complete cases): "
        f"{summary['amount_rating_pearson_correlation']:.4f}"
    )
    print(f"Outputs written to: {OUTPUT_DIR} and {FIGURE_DIR}")


if __name__ == "__main__":
    main()
