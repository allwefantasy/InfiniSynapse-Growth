#!/usr/bin/env python3
"""Generate informative matplotlib charts for Pillar 26–30 articles.

Only articles with quantitative practical examples (or viz-demo need) get charts.
Inserts `![...](./images/chart-*.png)` immediately after the Practical example
paragraph. Re-run is idempotent (skips insert if chart ref already present).

Usage:
  python3 gen-data-charts-p26-30.py           # generate + insert
  python3 gen-data-charts-p26-30.py --dry-run # plan only
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[4]  # InfiniSynapse-Growth (scripts→…→repo)
BLOG = ROOT / "SEO" / "Blog"

# Editorial palette — avoid purple/cream AI clichés
PALETTE = {
    "ink": "#1a1f2e",
    "muted": "#5c6578",
    "grid": "#e8ebf0",
    "accent": "#0d9488",  # teal
    "accent2": "#e11d48",  # rose
    "accent3": "#2563eb",  # blue
    "before": "#94a3b8",
    "after": "#0d9488",
    "fill": "#ccfbf1",
}


def style_ax(ax, title: str, ylabel: str | None = None, xlabel: str | None = None):
    ax.set_title(title, fontsize=13, fontweight="600", color=PALETTE["ink"], pad=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color=PALETTE["muted"])
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, color=PALETTE["muted"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(PALETTE["grid"])
    ax.spines["bottom"].set_color(PALETTE["grid"])
    ax.tick_params(colors=PALETTE["muted"], labelsize=9)
    ax.set_facecolor("white")
    ax.yaxis.grid(True, color=PALETTE["grid"], linewidth=0.8)
    ax.set_axisbelow(True)


def save(fig, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)


def _default_categories(title: str) -> tuple[str, ...]:
    t = title.lower()
    if any(k in t for k in ("customer", "crm", "loyalty", "offer", "golden")):
        return ("CRM", "Billing", "Support")
    if any(k in t for k in ("pipeline", "load", "etl", "orchestr", "transform", "adf", "dbt")):
        return ("Ingest", "Transform", "Serve")
    if any(k in t for k in ("lake", "warehouse", "dataset", "catalog", "discover")):
        return ("Raw zone", "Curated", "Serving")
    if any(k in t for k in ("govern", "audit", "retention", "storage", "compliance")):
        return ("Finance", "Ops", "Product")
    if any(k in t for k in ("dashboard", "visual", "analyst", "report", "exec")):
        return ("Exec", "Ops", "Self-serve")
    if any(k in t for k in ("tool", "integrat", "platform", "software", "suite")):
        return ("Catalog", "Quality", "Lineage")
    return ("Team A", "Team B", "Team C")


def chart_before_after_bar(
    path: Path,
    title: str,
    ylabel: str,
    before: float,
    after: float,
    labels=("Before", "After"),
    fmt="{:.0f}",
    categories: tuple[str, ...] | None = None,
):
    """Grouped bars: category × period (always ≥2 data dimensions)."""
    cats = list(categories or _default_categories(title))
    # Spread the headline before/after across categories (illustrative)
    spread_b = np.array([1.18, 1.0, 0.74, 0.92, 1.08][: len(cats)], dtype=float)
    spread_a = np.array([1.05, 1.0, 0.92, 0.98, 1.02][: len(cats)], dtype=float)
    before_vals = before * spread_b
    after_vals = after * spread_a
    # Keep after clearly improved but not identical across cats
    if after < before:
        after_vals = np.minimum(after_vals, before_vals * 0.85)

    x = np.arange(len(cats))
    w = 0.36
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    b1 = ax.bar(x - w / 2, before_vals, w, color=PALETTE["before"], label=labels[0], edgecolor="none")
    b2 = ax.bar(x + w / 2, after_vals, w, color=PALETTE["after"], label=labels[1], edgecolor="none")
    for bars, vals in ((b1, before_vals), (b2, after_vals)):
        for bar, v in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                v,
                fmt.format(v),
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="600",
                color=PALETTE["ink"],
            )
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    style_ax(ax, title, ylabel=ylabel, xlabel="Category (illustrative)")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.set_ylim(0, max(before_vals.max(), after_vals.max()) * 1.28)
    save(fig, path)


def chart_horizontal_retention(path: Path):
    cats = ["Transaction records", "Support tickets", "Marketing logs"]
    days = [7 * 365, 2 * 365, 90]
    labels = ["7 years", "2 years", "90 days"]
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    y = np.arange(len(cats))
    ax.barh(y, days, color=[PALETTE["accent"], PALETTE["accent3"], PALETTE["accent2"]], height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(cats)
    for i, (d, lab) in enumerate(zip(days, labels)):
        ax.text(d + 40, i, lab, va="center", fontsize=10, color=PALETTE["ink"], fontweight="600")
    style_ax(ax, "Illustrative retention schedule by data category", xlabel="Retention (days)")
    ax.set_xlim(0, max(days) * 1.2)
    save(fig, path)


def chart_line_quality_metrics(path: Path):
    weeks = np.arange(1, 13)
    null_rate = np.clip(8.5 - 0.55 * weeks + np.array([0.3, -0.2, 0.1, 0, -0.1, 0.2, 0, -0.15, 0.1, 0, -0.05, 0]), 1.5, None)
    dup_rate = np.clip(12 - 0.85 * weeks + np.array([0.2, 0, -0.3, 0.1, 0, 0.15, -0.1, 0, 0.05, -0.1, 0, 0]), 1.8, None)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(weeks, null_rate, color=PALETTE["accent3"], linewidth=2.2, marker="o", markersize=4, label="Null rate %")
    ax.plot(weeks, dup_rate, color=PALETTE["accent2"], linewidth=2.2, marker="s", markersize=4, label="Duplicate rate %")
    style_ax(ax, "Illustrative quality metrics after automated checks", ylabel="Rate (%)", xlabel="Week")
    ax.legend(frameon=False, fontsize=9)
    ax.set_xticks(weeks)
    save(fig, path)


def chart_stacked_time_split(path: Path):
    """60% reconcile vs 40% analyze → after flip."""
    labels = ["Before investment", "After data management"]
    reconcile = [60, 25]
    analyze = [40, 75]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    b1 = ax.bar(labels, reconcile, color=PALETTE["before"], width=0.5, label="Reconciling numbers")
    b2 = ax.bar(labels, analyze, bottom=reconcile, color=PALETTE["after"], width=0.5, label="Analyzing")
    for bars, vals, bottoms in ((b1, reconcile, [0, 0]), (b2, analyze, reconcile)):
        for bar, v, bot in zip(bars, vals, bottoms):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bot + v / 2,
                f"{v}%",
                ha="center",
                va="center",
                fontsize=11,
                fontweight="600",
                color="white",
            )
    style_ax(ax, "Illustrative analyst time allocation", ylabel="% of analyst time")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    save(fig, path)


def chart_line_cost_control(path: Path):
    months = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]
    with_ctrl = [12, 18, 28, 41, 52, 38, 29, 24]
    no_ctrl = [12, 18, 28, 42, 58, 74, 91, 110]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(months, no_ctrl, color=PALETTE["before"], linewidth=2.2, marker="o", markersize=4, label="No spend controls")
    ax.plot(months, with_ctrl, color=PALETTE["accent2"], linewidth=2.4, marker="s", markersize=4, label="With spend controls")
    ax.axvline(4.5, color=PALETTE["muted"], linestyle="--", linewidth=1)
    ax.text(4.55, 95, "Controls\nadded", fontsize=9, color=PALETTE["muted"])
    style_ax(ax, "Illustrative cloud warehouse spend by control regime", ylabel="Relative cost", xlabel="Month after migration")
    ax.legend(frameon=False, fontsize=9)
    save(fig, path)


def chart_monthly_sales_line(path: Path):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sales_ty = [42, 38, 45, 51, 58, 72, 81, 76, 63, 55, 68, 94]
    sales_ly = [36, 34, 40, 44, 49, 61, 70, 68, 58, 50, 60, 82]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(months, sales_ly, color=PALETTE["before"], linewidth=2.0, marker="o", markersize=4, label="Prior year")
    ax.plot(months, sales_ty, color=PALETTE["accent"], linewidth=2.4, marker="s", markersize=4, label="This year")
    style_ax(ax, "Illustrative monthly sales — year × month (two dimensions)", ylabel="Sales (index)", xlabel="Month")
    ax.legend(frameon=False, fontsize=9)
    save(fig, path)


def chart_viz_examples_triptych(path: Path):
    """Bar + line + scatter in one figure for visualization-examples article."""
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.2))

    # Bar — category comparison
    cats = ["A", "B", "C", "D"]
    vals = [32, 48, 21, 39]
    axes[0].bar(cats, vals, color=PALETTE["accent"], width=0.6)
    style_ax(axes[0], "Bar: compare categories", ylabel="Value")

    # Line — trend
    x = np.arange(1, 9)
    y = 20 + 3.2 * x + np.sin(x) * 2
    axes[1].plot(x, y, color=PALETTE["accent3"], linewidth=2.2, marker="o", markersize=4)
    style_ax(axes[1], "Line: show change over time", xlabel="Period")

    # Scatter — correlation
    rng = np.random.default_rng(42)
    xs = rng.normal(50, 12, 60)
    ys = 0.65 * xs + rng.normal(10, 8, 60)
    axes[2].scatter(xs, ys, c=PALETTE["accent2"], s=28, alpha=0.75, edgecolors="none")
    style_ax(axes[2], "Scatter: see relationships", xlabel="X", ylabel="Y")

    fig.suptitle(
        "Matching chart type to the question (illustrative)",
        fontsize=13,
        fontweight="600",
        color=PALETTE["ink"],
        y=1.02,
    )
    fig.tight_layout()
    save(fig, path)


def chart_analytics_types_line(path: Path):
    """Descriptive dip → diagnostic annotation → predictive forecast."""
    months = np.arange(1, 13)
    actual = np.array([88, 90, 87, 84, 79, 74, 71, 73, 76, 78, 80, 82], dtype=float)
    forecast = np.array([np.nan] * 8 + [76, 79, 83, 87], dtype=float)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(months[:8], actual[:8], color=PALETTE["ink"], linewidth=2.2, marker="o", markersize=4, label="Actual (descriptive)")
    ax.plot(months[7:], actual[7:], color=PALETTE["accent3"], linewidth=2.2, marker="o", markersize=4, label="Recovering")
    ax.plot(months, forecast, color=PALETTE["accent2"], linewidth=2.2, linestyle="--", marker="s", markersize=4, label="Predictive forecast")
    ax.annotate(
        "Diagnostic:\npromo lag found",
        xy=(6, 74),
        xytext=(3.2, 62),
        fontsize=8,
        color=PALETTE["muted"],
        arrowprops=dict(arrowstyle="->", color=PALETTE["muted"]),
    )
    style_ax(ax, "Illustrative analytics progression: describe → diagnose → predict", ylabel="Sales index", xlabel="Month")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    ax.set_xticks(months)
    save(fig, path)


def chart_scatter_custom(path: Path):
    rng = np.random.default_rng(7)
    n = 80
    x = rng.uniform(10, 90, n)
    y = 0.4 * x + rng.normal(0, 8, n) + 15
    size = rng.uniform(20, 120, n)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    sc = ax.scatter(x, y, s=size, c=x, cmap="viridis", alpha=0.75, edgecolors="none")
    style_ax(ax, "Illustrative custom interactive-ready scatter (programmed viz)", xlabel="Engagement score", ylabel="Conversion index")
    fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04).ax.tick_params(labelsize=8)
    save(fig, path)


def chart_join_explosion(path: Path):
    cats = ["Orders", "Items", "Returns"]
    correct = [1.0, 1.0, 1.0]
    exploded = [2.4, 3.1, 1.8]
    x = np.arange(len(cats))
    w = 0.36
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(x - w / 2, correct, w, color=PALETTE["after"], label="Correct grain")
    ax.bar(x + w / 2, exploded, w, color=PALETTE["accent2"], label="Bad join (explosion)")
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    style_ax(ax, "Illustrative SQL grain error by fact table", ylabel="Reported revenue (relative)", xlabel="Fact")
    ax.legend(frameon=False, fontsize=9)
    ax.set_ylim(0, 3.8)
    save(fig, path)


def chart_kpi_sparklines(path: Path):
    """Six focused KPIs as small multiples — dashboard focus idea."""
    fig, axes = plt.subplots(2, 3, figsize=(10, 5.2))
    names = ["Revenue", "Active users", "Churn", "NPS", "Latency", "Error rate"]
    rng = np.random.default_rng(3)
    for ax, name in zip(axes.flat, names):
        y = np.cumsum(rng.normal(0, 1, 20)) + 50
        if name in ("Churn", "Error rate", "Latency"):
            y = 30 - np.cumsum(rng.normal(0.1, 0.6, 20))
        ax.plot(y, color=PALETTE["accent"], linewidth=1.8)
        ax.fill_between(range(len(y)), y, alpha=0.12, color=PALETTE["accent"])
        ax.set_title(name, fontsize=10, color=PALETTE["ink"], fontweight="600")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(PALETTE["grid"])
    fig.suptitle("Illustrative focused dashboard: six decision KPIs", fontsize=13, fontweight="600", color=PALETTE["ink"])
    fig.tight_layout()
    save(fig, path)


def chart_freshness_bar(path: Path):
    domains = ["Revenue", "Ops", "Marketing"]
    needed = [24, 24, 48]
    actual = [168, 96, 168]
    x = np.arange(len(domains))
    w = 0.36
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(x - w / 2, needed, w, color=PALETTE["after"], label="Decision needs")
    ax.bar(x + w / 2, actual, w, color=PALETTE["accent2"], label="Dashboard refresh")
    ax.set_xticks(x)
    ax.set_xticklabels(domains)
    style_ax(ax, "Illustrative freshness mismatch by domain", ylabel="Latency (hours)", xlabel="Domain")
    ax.legend(frameon=False, fontsize=9)
    ax.set_ylim(0, 210)
    save(fig, path)


def chart_grouped_defs(path: Path, title: str):
    """Three teams disagree on a metric → one after governance."""
    teams = ["Team A", "Team B", "Team C"]
    before = [12840, 15120, 9760]
    after = [12400, 12400, 12400]
    x = np.arange(len(teams))
    w = 0.35
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(x - w / 2, before, w, color=PALETTE["before"], label="Before (conflicting defs)")
    ax.bar(x + w / 2, after, w, color=PALETTE["after"], label="After (one definition)")
    ax.set_xticks(x)
    ax.set_xticklabels(teams)
    style_ax(ax, title, ylabel="Active count (illustrative)")
    ax.legend(frameon=False, fontsize=8)
    save(fig, path)


def chart_adoption_curve(path: Path, title: str):
    months = np.arange(1, 13)
    heavy = np.clip(np.array([5, 8, 10, 11, 12, 12, 13, 14, 14, 15, 15, 16]), 0, 100)
    lean = np.clip(np.array([8, 18, 32, 48, 58, 66, 72, 78, 82, 86, 90, 93]), 0, 100)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(months, heavy, color=PALETTE["before"], linewidth=2.2, marker="o", markersize=4, label="Heavy suite, no owners")
    ax.plot(months, lean, color=PALETTE["after"], linewidth=2.2, marker="s", markersize=4, label="Lean start + expand")
    style_ax(ax, title, ylabel="Catalog populated (%)", xlabel="Month")
    ax.legend(frameon=False, fontsize=8)
    ax.set_xticks(months)
    ax.set_ylim(0, 100)
    save(fig, path)


def chart_cloud_bill_triple(path: Path):
    months = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
    aws = [100, 160, 240, 300, 210, 145]
    azure = [80, 120, 190, 250, 180, 130]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(months, aws, color=PALETTE["accent2"], linewidth=2.4, marker="o", markersize=4, label="AWS spend")
    ax.plot(months, azure, color=PALETTE["accent3"], linewidth=2.4, marker="s", markersize=4, label="Azure spend")
    ax.axvline(2.5, color=PALETTE["muted"], linestyle="--", linewidth=1)
    ax.text(2.55, 280, "Tagging +\nownership", fontsize=8, color=PALETTE["muted"])
    style_ax(ax, "Illustrative multi-cloud bill by provider × quarter", ylabel="Relative spend (index)", xlabel="Quarter")
    ax.legend(frameon=False, fontsize=9)
    save(fig, path)


def chart_lake_vs_warehouse_split(path: Path):
    patterns = ["Either/or\n(struggled)", "Layered\n(lake + WH)"]
    ml_fit = [32, 86]
    report_fit = [48, 90]
    x = np.arange(len(patterns))
    w = 0.36
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(x - w / 2, ml_fit, w, color=PALETTE["accent3"], label="ML / exploration fit")
    ax.bar(x + w / 2, report_fit, w, color=PALETTE["after"], label="Reporting fit")
    ax.set_xticks(x)
    ax.set_xticklabels(patterns)
    style_ax(ax, "Illustrative analytics fit: pattern × workload", ylabel="Fit score (0–100)")
    ax.legend(frameon=False, fontsize=9)
    ax.set_ylim(0, 110)
    save(fig, path)


def chart_etl_vs_elt(path: Path):
    stages = ["Extract", "Transform", "Load / serve"]
    etl = [2, 8, 1.5]
    elt = [2, 2.5, 1.2]
    x = np.arange(len(stages))
    w = 0.35
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(x - w / 2, etl, w, color=PALETTE["before"], label="Classic ETL")
    ax.bar(x + w / 2, elt, w, color=PALETTE["after"], label="ELT (transform in warehouse)")
    ax.set_xticks(x)
    ax.set_xticklabels(stages)
    style_ax(ax, "Illustrative pipeline stage duration: ETL vs ELT", ylabel="Hours per run")
    ax.legend(frameon=False, fontsize=8)
    save(fig, path)


def chart_scientist_time_split(path: Path):
    labels = ["Hired scientist\nto 'fix data'", "Engineer owns\npipelines"]
    fix_pipes = [80, 15]
    model = [20, 85]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    b1 = ax.bar(labels, fix_pipes, color=PALETTE["before"], width=0.5, label="Fixing pipelines")
    b2 = ax.bar(labels, model, bottom=fix_pipes, color=PALETTE["after"], width=0.5, label="Modeling / analysis")
    for bars, vals, bottoms in ((b1, fix_pipes, [0, 0]), (b2, model, fix_pipes)):
        for bar, v, bot in zip(bars, vals, bottoms):
            if v >= 12:
                ax.text(bar.get_x() + bar.get_width() / 2, bot + v / 2, f"{v}%", ha="center", va="center", fontsize=10, fontweight="600", color="white")
    style_ax(ax, "Illustrative role mismatch: who spends time on pipelines", ylabel="% of time")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, fontsize=8)
    save(fig, path)


def chart_churn_forecast(path: Path):
    months = np.arange(1, 13)
    churn = np.array([3.2, 3.1, 3.4, 3.6, 3.8, 4.1, 4.0, 3.9, 3.7, 3.5, 3.4, 3.3])
    forecast = np.array([np.nan] * 8 + [3.6, 3.5, 3.3, 3.1])
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(months[:8], churn[:8], color=PALETTE["ink"], linewidth=2.2, marker="o", markersize=4, label="Descriptive (actual)")
    ax.plot(months[7:], churn[7:], color=PALETTE["accent3"], linewidth=2.2, marker="o", markersize=4, label="Observed recovery")
    ax.plot(months, forecast, color=PALETTE["accent2"], linewidth=2.2, linestyle="--", marker="s", markersize=4, label="Predictive forecast")
    style_ax(ax, "Illustrative analytics maturity: descriptive → predictive churn", ylabel="Churn rate (%)", xlabel="Month")
    ax.legend(frameon=False, fontsize=8)
    ax.set_xticks(months)
    save(fig, path)


def chart_tool_stack_bars(path: Path, title: str, items: list[tuple[str, float]], ylabel: str = "Relative effort / value"):
    labels = [i[0] for i in items]
    effort = [i[1] for i in items]
    # Second dimension: delivered value (illustrative inverse/offset of effort)
    value = [max(1.0, min(effort) + max(effort) - v + 1.5) for v in effort]
    x = np.arange(len(labels))
    w = 0.36
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(x - w / 2, effort, w, color=PALETTE["before"], label="Relative effort")
    ax.bar(x + w / 2, value, w, color=PALETTE["after"], label="Relative value")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    style_ax(ax, title, ylabel=ylabel, xlabel="Tool / layer")
    ax.legend(frameon=False, fontsize=9)
    ax.set_ylim(0, max(max(effort), max(value)) * 1.25)
    save(fig, path)


def chart_scatter_correlation(path: Path, title: str):
    rng = np.random.default_rng(11)
    x = rng.uniform(20, 90, 70)
    y = 0.55 * x + rng.normal(5, 9, 70)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.scatter(x, y, c=PALETTE["accent"], s=36, alpha=0.75, edgecolors="none")
    style_ax(ax, title, xlabel="Feature usage", ylabel="Outcome metric")
    save(fig, path)


# folder_slug -> (filename, alt_text, generator)
CHARTS: dict[str, tuple[str, str, callable]] = {
    # Pillar 26
    "388-data-governance-frameworks": (
        "chart-recon-time-before-after.png",
        "Bar chart: month-end reconciliation time before and after adopting a governance framework (illustrative −33%)",
        lambda p: chart_before_after_bar(p, "Month-end reconciliation time (illustrative)", "Hours", 36, 24, fmt="{:.0f}h"),
    ),
    "389-data-quality-management": (
        "chart-quality-metrics-trend.png",
        "Line chart: null rate and duplicate rate trending down after automated quality checks (illustrative)",
        chart_line_quality_metrics,
    ),
    "390-what-is-a-data-retention-policy": (
        "chart-retention-schedule.png",
        "Horizontal bar chart: retention periods by data category — 7 years, 2 years, 90 days (illustrative)",
        chart_horizontal_retention,
    ),
    "393-data-quality": (
        "chart-duplicate-rate-before-after.png",
        "Bar chart: duplicate customer rate before (12%) and after deduplication (illustrative)",
        lambda p: chart_before_after_bar(p, "Duplicate customer records (illustrative)", "Share of records (%)", 12, 2.5, fmt="{:.1f}%"),
    ),
    "395-data-governance-framework": (
        "chart-audit-time-before-after.png",
        "Bar chart: audit response time before and after a governance framework (weeks → days, illustrative)",
        lambda p: chart_before_after_bar(p, "Audit response time (illustrative)", "Days", 21, 3, fmt="{:.0f}d"),
    ),
    "401-data-quality-tools": (
        "chart-detection-latency.png",
        "Bar chart: time to detect a broken pipeline — month-end vs continuous validation (illustrative)",
        lambda p: chart_before_after_bar(p, "Time to detect a broken pipeline (illustrative)", "Hours", 720, 1, fmt="{:.0f}h"),
    ),
    "407-data-quality-software": (
        "chart-detection-latency.png",
        "Bar chart: time to detect a broken pipeline — month-end vs in-pipeline validation (illustrative)",
        lambda p: chart_before_after_bar(p, "Time to detect a broken pipeline (illustrative)", "Hours", 720, 1, fmt="{:.0f}h"),
    ),
    # Pillar 27
    "408-master-data-management": (
        "chart-duplicate-errors-before-after.png",
        "Bar chart: duplicate-customer errors in loyalty analytics before and after MDM (illustrative −50%+)",
        lambda p: chart_before_after_bar(p, "Duplicate-customer errors in loyalty analytics (illustrative)", "Errors / month", 48, 18, fmt="{:.0f}"),
    ),
    "411-data-management": (
        "chart-analyst-time-split.png",
        "Stacked bar chart: analyst time spent reconciling vs analyzing before and after data management (illustrative 60%→25%)",
        chart_stacked_time_split,
    ),
    # Pillar 28
    "428-data-engineering": (
        "chart-failed-load-incidents.png",
        "Bar chart: failed-load incidents before and after orchestrated pipelines (illustrative −70%)",
        lambda p: chart_before_after_bar(p, "Failed-load incidents per quarter (illustrative)", "Incidents", 40, 12, fmt="{:.0f}"),
    ),
    "440-data-pipelines": (
        "chart-pipeline-reliability.png",
        "Bar chart: silent failures vs alerted failures — reliability of pipelines (illustrative)",
        lambda p: chart_before_after_bar(p, "Silent vs alerted pipeline failures (illustrative)", "Events / month", 14, 2, ("Silent failures\n(before)", "Alerted + retried\n(after)"), fmt="{:.0f}"),
    ),
    # Pillar 29
    "448-data-warehouse": (
        "chart-time-to-answer.png",
        "Bar chart: time-to-answer before and after a modeled warehouse layer (hours → minutes, illustrative)",
        lambda p: chart_before_after_bar(p, "Time-to-answer for top subject areas (illustrative)", "Minutes", 180, 12, fmt="{:.0f}m"),
    ),
    "458-snowflake-data-warehouse": (
        "chart-warehouse-spend.png",
        "Line chart: illustrative warehouse spend spike then decline after auto-suspend and sizing controls",
        chart_line_cost_control,
    ),
    "459-cloud-data-warehouse": (
        "chart-cloud-warehouse-spend.png",
        "Line chart: illustrative cloud warehouse cost climb then control after spend governance",
        chart_line_cost_control,
    ),
    # Pillar 30
    "468-data-visualization": (
        "chart-review-time-before-after.png",
        "Bar chart: weekly review time before and after a focused dashboard (45 → 10 minutes, illustrative)",
        lambda p: chart_before_after_bar(p, "Weekly review duration (illustrative)", "Minutes", 45, 10, fmt="{:.0f}m"),
    ),
    "469-dashboard": (
        "chart-focused-kpi-panel.png",
        "Small-multiple line charts: six focused decision KPIs on a dashboard (illustrative)",
        chart_kpi_sparklines,
    ),
    "479-data-dashboard": (
        "chart-freshness-mismatch.png",
        "Bar chart: decision cadence vs dashboard refresh latency (illustrative freshness mismatch)",
        chart_freshness_bar,
    ),
    "480-sql-data-analytics": (
        "chart-sql-grain-error.png",
        "Bar chart: reported revenue with correct grain vs bad join row explosion (illustrative)",
        chart_join_explosion,
    ),
    "481-data-visualization-programming": (
        "chart-custom-scatter.png",
        "Scatter plot: custom programmed visualization with size and color encodings (illustrative)",
        chart_scatter_custom,
    ),
    "484-data-visualization-examples": (
        "chart-types-bar-line-scatter.png",
        "Triptych of data visualization examples: bar chart, line chart, and scatter plot matched to question type",
        chart_viz_examples_triptych,
    ),
    "485-what-is-data-visualization": (
        "chart-monthly-sales-line.png",
        "Line chart: monthly sales with a clear seasonal pattern — why visualization reveals what tables hide",
        chart_monthly_sales_line,
    ),
    "486-define-analytics": (
        "chart-analytics-progression.png",
        "Line chart: descriptive dip, diagnostic annotation, and predictive forecast (illustrative analytics types)",
        chart_analytics_types_line,
    ),
    # --- Expanded coverage (remaining Pillar 26–30) ---
    "391-data-governance": (
        "chart-conflicting-definitions.png",
        "Grouped bar chart: three teams reporting different active-patient counts before and after one definition (illustrative)",
        lambda p: chart_grouped_defs(p, "Conflicting 'active patient' counts across dashboards (illustrative)"),
    ),
    "392-data-governance-news": (
        "chart-retention-risk.png",
        "Bar chart: location-data retention days — over-retention vs policy-aligned (illustrative)",
        lambda p: chart_before_after_bar(p, "Location data retained (illustrative)", "Days kept", 900, 180, ("Ignored news\n(over-retention)", "Tracked news\n(tightened)"), fmt="{:.0f}d"),
    ),
    "394-data-governance-tools": (
        "chart-catalog-adoption.png",
        "Line chart: catalog adoption — heavyweight unused suite vs lean expand (illustrative)",
        lambda p: chart_adoption_curve(p, "Catalog adoption: feature-heavy vs lean start (illustrative)"),
    ),
    "396-what-is-data-governance": (
        "chart-active-user-defs.png",
        "Grouped bar chart: three 'active user' definitions reconciled to one (illustrative)",
        lambda p: chart_grouped_defs(p, "Three dashboards, three 'active user' counts (illustrative)"),
    ),
    "397-master-data-governance": (
        "chart-supplier-spellings.png",
        "Bar chart: unique supplier spellings before and after master data governance (illustrative)",
        lambda p: chart_before_after_bar(p, "Supplier name variants in spend data (illustrative)", "Distinct spellings", 4, 1, fmt="{:.0f}"),
    ),
    "398-data-governance-software": (
        "chart-software-adoption.png",
        "Line chart: governance software adoption — broad empty catalog vs lean populated (illustrative)",
        lambda p: chart_adoption_curve(p, "Governance software adoption curve (illustrative)"),
    ),
    "399-iso-8000-data-quality-standard": (
        "chart-integration-errors.png",
        "Bar chart: partner integration errors before and after ISO 8000-style specs (illustrative)",
        lambda p: chart_before_after_bar(p, "Partner data integration errors / month (illustrative)", "Errors", 42, 11, fmt="{:.0f}"),
    ),
    "400-data-governance-definition": (
        "chart-decision-clarity.png",
        "Bar chart: decisions resolved per quarter — vague vs precise governance definition (illustrative)",
        lambda p: chart_before_after_bar(p, "Governance decisions resolved / quarter (illustrative)", "Decisions", 3, 14, ("Vague definition", "Precise definition"), fmt="{:.0f}"),
    ),
    "402-data-governance-solutions": (
        "chart-solution-islands.png",
        "Bar chart: connected metadata links — disconnected tools vs integrated solutions (illustrative)",
        lambda p: chart_before_after_bar(p, "Cross-tool metadata links in use (illustrative)", "Active links", 2, 18, ("Three islands", "Integrated"), fmt="{:.0f}"),
    ),
    "403-data-governance-best-practices": (
        "chart-domain-rollout.png",
        "Line chart: domains brought under governance practices over two quarters (illustrative)",
        lambda p: chart_tool_stack_bars(
            p,
            "Domains under governance after starting with one (illustrative)",
            [("Month 1", 1), ("Month 3", 2), ("Month 6", 4), ("Month 9", 6)],
            ylabel="Domains governed",
        ),
    ),
    "404-data-governance-tool": (
        "chart-tool-usage.png",
        "Line chart: governance tool usage — feature-picked vs steward-friendly (illustrative)",
        lambda p: chart_adoption_curve(p, "Governance tool weekly active use (illustrative)"),
    ),
    "405-data-governance-strategy": (
        "chart-strategy-alignment.png",
        "Bar chart: reactive firefighting vs goal-aligned governance hours (illustrative)",
        lambda p: chart_before_after_bar(p, "Hours/week on reactive vs planned governance (illustrative)", "Hours", 28, 10, ("Reactive chase", "Goal-aligned"), fmt="{:.0f}h"),
    ),
    "406-data-retention-policy": (
        "chart-storage-cost-cut.png",
        "Bar chart: storage cost index before and after five-tier retention policy (illustrative −⅓)",
        lambda p: chart_before_after_bar(p, "Storage cost after retention automation (illustrative)", "Cost index", 100, 67, fmt="{:.0f}"),
    ),
    "409-data-catalog-platforms": (
        "chart-catalog-fill-rate.png",
        "Line chart: catalog fill rate — manual-entry platform vs automated (illustrative)",
        lambda p: chart_adoption_curve(p, "Catalog fill rate by platform approach (illustrative)"),
    ),
    "410-data-lineage-tracking": (
        "chart-trace-time.png",
        "Bar chart: time to trace a wrong figure — without vs with lineage (illustrative)",
        lambda p: chart_before_after_bar(p, "Time to trace a wrong board figure (illustrative)", "Hours", 72, 0.5, fmt="{:.1f}h"),
    ),
    "412-engineering-data-management": (
        "chart-bom-incidents.png",
        "Bar chart: wrong-BOM / recall-class incidents before and after engineering data management (illustrative)",
        lambda p: chart_before_after_bar(p, "Wrong-version BOM incidents / year (illustrative)", "Incidents", 5, 1, fmt="{:.0f}"),
    ),
    "413-data-management-tools": (
        "chart-tool-integration-effort.png",
        "Bar chart: integration effort — five disconnected tools vs smaller interoperable set (illustrative)",
        lambda p: chart_before_after_bar(p, "Weekly hours spent integrating tools (illustrative)", "Hours", 22, 6, ("5 best-of-breed", "Fewer, interoperable"), fmt="{:.0f}h"),
    ),
    "414-data-lineage": (
        "chart-lineage-minutes.png",
        "Bar chart: minutes to evidence a board metric with lineage vs without (illustrative)",
        lambda p: chart_before_after_bar(p, "Time to evidence a contested metric (illustrative)", "Minutes", 480, 12, fmt="{:.0f}m"),
    ),
    "415-data-management-software": (
        "chart-software-utilization.png",
        "Line chart: data management software utilization — unused license vs warehouse-fit (illustrative)",
        lambda p: chart_adoption_curve(p, "Software utilization: unused vs warehouse-fit (illustrative)"),
    ),
    "416-enterprise-data-management": (
        "chart-customer-view.png",
        "Bar chart: systems contributing to one customer view before and after EDM (illustrative)",
        lambda p: chart_before_after_bar(p, "Systems feeding one customer view (illustrative)", "Systems unified", 1, 6, ("Siloed domains", "Enterprise view"), fmt="{:.0f}"),
    ),
    "417-data-catalog": (
        "chart-discovery-time.png",
        "Bar chart: time for a new analyst to find the authoritative revenue table (illustrative)",
        lambda p: chart_before_after_bar(p, "Time to find authoritative revenue table (illustrative)", "Days", 10, 0.5, fmt="{:.1f}d"),
    ),
    "418-data-management-services": (
        "chart-internal-capability.png",
        "Bar chart: % of changes needing external services — dependency vs upskilled peer (illustrative)",
        lambda p: chart_before_after_bar(p, "Changes needing external services (illustrative)", "% of changes", 85, 25, ("No internal skills", "Upskilled peer"), fmt="{:.0f}%"),
    ),
    "419-customer-data-management": (
        "chart-conflicting-offers.png",
        "Bar chart: conflicting marketing offers per customer before and after CDM (illustrative)",
        lambda p: chart_before_after_bar(p, "Conflicting offers sent per person (illustrative)", "Offers", 3, 1, fmt="{:.0f}"),
    ),
    "420-master-data-management-tools": (
        "chart-golden-record-drift.png",
        "Bar chart: golden-record drift rate with vs without stewardship staffing (illustrative)",
        lambda p: chart_before_after_bar(p, "Golden-record drift rate (illustrative)", "% drifted / quarter", 28, 6, ("No stewardship", "Stewardship staffed"), fmt="{:.0f}%"),
    ),
    "421-cloud-data-management": (
        "chart-multi-cloud-bill.png",
        "Line chart: multi-cloud bill tripling then controlled with tagging and ownership (illustrative)",
        chart_cloud_bill_triple,
    ),
    "422-product-data-management-software": (
        "chart-wrong-version-scrap.png",
        "Bar chart: scrap events from superseded CAD/BOM versions (illustrative)",
        lambda p: chart_before_after_bar(p, "Scrap events from wrong product versions (illustrative)", "Events / year", 4, 0, fmt="{:.0f}"),
    ),
    "423-master-data": (
        "chart-product-counts.png",
        "Grouped bar chart: three product counts to the board reconciled via master data (illustrative)",
        lambda p: chart_grouped_defs(p, "Three product counts reported to the board (illustrative)"),
    ),
    "424-data-management-platform": (
        "chart-integration-overhead.png",
        "Bar chart: weekly integration overhead — five tools vs one platform (illustrative)",
        lambda p: chart_before_after_bar(p, "Weekly hours on tool integration (illustrative)", "Hours", 20, 5, ("Five tools", "One platform"), fmt="{:.0f}h"),
    ),
    "425-master-data-management-software": (
        "chart-mdm-stewardship.png",
        "Bar chart: golden-record quality score with under-resourced vs staffed stewardship (illustrative)",
        lambda p: chart_before_after_bar(p, "Golden-record quality score (illustrative)", "Score 0–100", 52, 88, ("Under-staffed", "Stewardship funded"), fmt="{:.0f}"),
    ),
    "426-what-is-data-management": (
        "chart-report-agreement.png",
        "Bar chart: report agreement rate when customer data is siloed vs managed (illustrative)",
        lambda p: chart_before_after_bar(p, "Reports agreeing on customer metrics (illustrative)", "% agreement", 35, 92, fmt="{:.0f}%"),
    ),
    "427-what-is-master-data-management": (
        "chart-customer-storage-ways.png",
        "Grouped bar chart: customer identity variants by system (CRM, Billing, Support) before vs after MDM (illustrative)",
        lambda p: chart_before_after_bar(
            p,
            "Customer identity variants by system (illustrative)",
            "Variants",
            5,
            1,
            fmt="{:.0f}",
            categories=("CRM", "Billing", "Support"),
        ),
    ),
    "429-what-is-a-data-pipeline": (
        "chart-manual-export-breaks.png",
        "Bar chart: CEO-dashboard breaks from missed manual exports vs automated pipeline (illustrative)",
        lambda p: chart_before_after_bar(p, "Dashboard breaks from missed loads / month (illustrative)", "Breaks", 6, 0, ("Manual exports", "Automated pipeline"), fmt="{:.0f}"),
    ),
    "430-azure-data-factory": (
        "chart-adf-maintainability.png",
        "Bar chart: change lead time — heavy transforms in ADF vs push-down to warehouse (illustrative)",
        lambda p: chart_before_after_bar(p, "Days to change a transformation safely (illustrative)", "Days", 12, 3, ("All logic in ADF", "Warehouse push-down"), fmt="{:.0f}d"),
    ),
    "431-data-engineering-news": (
        "chart-stack-rebuilds.png",
        "Bar chart: stack rebuilds vs features shipped — chasing headlines vs durable trends (illustrative)",
        lambda p: chart_tool_stack_bars(
            p,
            "Yearly outcomes: chase every headline vs filter for durability (illustrative)",
            [("Stack rebuilds\n(chase)", 2), ("Features shipped\n(chase)", 3), ("Stack rebuilds\n(filter)", 0), ("Features shipped\n(filter)", 11)],
            ylabel="Count / year",
        ),
    ),
    "432-data-engineer": (
        "chart-analyst-fix-time.png",
        "Bar chart: % of analyst time fixing broken exports before and after reliable pipelines (illustrative)",
        lambda p: chart_before_after_bar(p, "Analyst time fixing broken exports (illustrative)", "% of time", 50, 10, fmt="{:.0f}%"),
    ),
    "433-data-pipeline": (
        "chart-ordering-failures.png",
        "Bar chart: weekly pipeline ordering failures — cron vs explicit dependencies (illustrative)",
        lambda p: chart_before_after_bar(p, "Ordering failures / week (illustrative)", "Failures", 4, 0.5, ("Independent cron", "Orchestrated deps"), fmt="{:.1f}"),
    ),
    "434-python-for-data-engineering": (
        "chart-idempotent-reruns.png",
        "Bar chart: production failures on re-run — notebook script vs idempotent jobs (illustrative)",
        lambda p: chart_before_after_bar(p, "Failed production re-runs / month (illustrative)", "Failures", 9, 1, ("Notebook script", "Idempotent jobs"), fmt="{:.0f}"),
    ),
    "435-data-engineering-services": (
        "chart-maintainability-score.png",
        "Bar chart: maintainability score — undocumented services build vs documented handoff (illustrative)",
        lambda p: chart_before_after_bar(p, "Internal maintainability score (illustrative)", "Score 0–100", 28, 81, ("Undocumented", "Docs + handover"), fmt="{:.0f}"),
    ),
    "436-databricks-delta-streaming-real-time": (
        "chart-hourly-vs-batch.png",
        "Bar chart: relative cost for hourly dashboard — streaming vs scheduled batch (illustrative)",
        lambda p: chart_before_after_bar(p, "Relative cost for hourly dashboard refresh (illustrative)", "Cost index", 100, 35, ("Always-on stream", "Scheduled batch"), fmt="{:.0f}"),
    ),
    "437-azure-data-factory-complex-transformation": (
        "chart-adf-transform-cost.png",
        "Bar chart: transform cost/performance — Mapping Data Flows vs warehouse joins (illustrative)",
        lambda p: chart_before_after_bar(p, "Relative cost for heavy joins (illustrative)", "Cost index", 100, 40, ("ADF Mapping Flows", "Warehouse push-down"), fmt="{:.0f}"),
    ),
    "438-python-data-engineering-news": (
        "chart-rewrite-churn.png",
        "Bar chart: pipeline rewrites / year — chasing Python news vs change only for measured problems (illustrative)",
        lambda p: chart_before_after_bar(p, "Pipeline rewrites / year (illustrative)", "Rewrites", 8, 2, ("Chase every item", "Measured problems"), fmt="{:.0f}"),
    ),
    "439-what-is-data-engineering": (
        "chart-analysis-breakage.png",
        "Bar chart: analysis breakage incidents before and after investing in data engineering (illustrative)",
        lambda p: chart_before_after_bar(p, "Analysis breakage incidents / quarter (illustrative)", "Incidents", 18, 4, fmt="{:.0f}"),
    ),
    "441-data-engineer-vs-data-scientist": (
        "chart-role-time-split.png",
        "Stacked bar chart: scientist time on pipelines vs modeling when roles are mismatched (illustrative)",
        chart_scientist_time_split,
    ),
    "442-what-do-data-engineers-do": (
        "chart-pipelines-kept-reliable.png",
        "Bar chart: pipelines kept reliable — 'just SQL' misconception vs operational engineering (illustrative)",
        lambda p: chart_before_after_bar(p, "Pipelines kept reliable (illustrative)", "Pipelines", 12, 100, ("'Just wrote SQL'", "Ops + reliability"), fmt="{:.0f}"),
    ),
    "443-what-does-a-data-engineer-do": (
        "chart-role-scope.png",
        "Bar chart: delivery predictability — overscoped hire vs scoped role (illustrative)",
        lambda p: chart_before_after_bar(p, "On-time pipeline deliveries / quarter (illustrative)", "Deliveries", 2, 9, ("Everything at once", "Scoped role"), fmt="{:.0f}"),
    ),
    "444-what-is-dbt-in-data-engineering": (
        "chart-dbt-test-breaks.png",
        "Bar chart: dashboard breaks from untested SQL vs dbt tests + version control (illustrative)",
        lambda p: chart_before_after_bar(p, "Dashboard breaks from bad transforms / month (illustrative)", "Breaks", 7, 1, ("SQL files only", "dbt tests + VCS"), fmt="{:.0f}"),
    ),
    "445-data-orchestration": (
        "chart-orchestration-failures.png",
        "Bar chart: ordering failures — independent cron vs real orchestration (illustrative)",
        lambda p: chart_before_after_bar(p, "Pipeline ordering failures / month (illustrative)", "Failures", 15, 2, ("Independent cron", "Orchestration"), fmt="{:.0f}"),
    ),
    "446-what-is-a-data-engineer": (
        "chart-fragile-vs-reliable.png",
        "Bar chart: production incidents — hire for tool trivia vs reliability mindset (illustrative)",
        lambda p: chart_before_after_bar(p, "Production data incidents / quarter (illustrative)", "Incidents", 16, 3, ("Tool familiarity", "Reliability mindset"), fmt="{:.0f}"),
    ),
    "447-etl-data": (
        "chart-etl-vs-elt.png",
        "Grouped bar chart: stage duration for classic ETL vs ELT (illustrative)",
        chart_etl_vs_elt,
    ),
    "449-what-is-a-data-lake": (
        "chart-lake-usability.png",
        "Bar chart: % of lake datasets actually used — swamp vs cataloged zones (illustrative)",
        lambda p: chart_before_after_bar(p, "Lake datasets used by analysts (illustrative)", "% used", 8, 55, ("Dump / swamp", "Catalog + zones"), fmt="{:.0f}%"),
    ),
    "450-what-is-a-data-warehouse": (
        "chart-revenue-definitions.png",
        "Grouped bar chart: five teams' revenue numbers reconciled in one warehouse (illustrative)",
        lambda p: chart_grouped_defs(p, "Conflicting revenue numbers before one warehouse (illustrative)"),
    ),
    "451-data-warehouse-design": (
        "chart-query-latency.png",
        "Bar chart: report query latency — max-detail model vs right grain + aggregates (illustrative)",
        lambda p: chart_before_after_bar(p, "Typical report query time (illustrative)", "Seconds", 95, 4, ("Max detail", "Right grain"), fmt="{:.0f}s"),
    ),
    "452-data-mesh-architecture": (
        "chart-domain-ownership.png",
        "Bar chart: domains with real ownership — tools-only mesh vs accountability shift (illustrative)",
        lambda p: chart_before_after_bar(p, "Domains with accountable owners (illustrative)", "Domains", 1, 8, ("Tools, central ops", "Domain ownership"), fmt="{:.0f}"),
    ),
    "453-data-lake-architecture": (
        "chart-lake-zones.png",
        "Bar chart: discoverable datasets — flat bucket swamp vs zoned architecture (illustrative)",
        lambda p: chart_before_after_bar(p, "Discoverable, trusted datasets (illustrative)", "% of lake", 10, 70, ("Flat bucket", "Zones + catalog"), fmt="{:.0f}%"),
    ),
    "454-data-lake": (
        "chart-lake-usage.png",
        "Bar chart: analyst queries hitting the lake — dormant raw dump vs cataloged lake (illustrative)",
        lambda p: chart_before_after_bar(p, "Weekly analyst queries on the lake (illustrative)", "Queries", 5, 120, ("No catalog", "Cataloged"), fmt="{:.0f}"),
    ),
    "455-data-lake-vs-data-warehouse": (
        "chart-lake-warehouse-fit.png",
        "Bar chart: analytics fit — forced either/or vs lake for ML + warehouse for reporting (illustrative)",
        chart_lake_vs_warehouse_split,
    ),
    "456-data-mesh": (
        "chart-mesh-accountability.png",
        "Bar chart: cross-domain request cycle time — catalog-only vs real mesh ownership (illustrative)",
        lambda p: chart_before_after_bar(p, "Days to fulfill a cross-domain data request (illustrative)", "Days", 21, 5, ("Catalog only", "Domain ownership"), fmt="{:.0f}d"),
    ),
    "457-enterprise-data-warehouse": (
        "chart-edw-definition-first.png",
        "Bar chart: project progress — build-first stall vs definitions-first EDW (illustrative)",
        lambda p: chart_before_after_bar(p, "EDW milestones completed in year 1 (illustrative)", "Milestones", 2, 9, ("Build first", "Definitions first"), fmt="{:.0f}"),
    ),
    "460-data-lakehouse": (
        "chart-lakehouse-reliability.png",
        "Bar chart: table reliability score — swamp lakehouse vs governed table formats (illustrative)",
        lambda p: chart_before_after_bar(p, "Lakehouse table reliability score (illustrative)", "Score 0–100", 35, 86, ("No formats/gov", "Formats + gov"), fmt="{:.0f}"),
    ),
    "461-azure-data-lake": (
        "chart-adl-usability.png",
        "Bar chart: usable datasets in Azure Data Lake — dump vs cataloged strategy (illustrative)",
        lambda p: chart_before_after_bar(p, "Datasets analysts can find and trust (illustrative)", "% of store", 12, 62, ("Dump only", "Catalog + strategy"), fmt="{:.0f}%"),
    ),
    "462-data-lake-what-is": (
        "chart-governance-question.png",
        "Bar chart: vendor-call readiness — storage-only question vs governance-first question (illustrative)",
        lambda p: chart_before_after_bar(p, "Decision-quality score after vendor call (illustrative)", "Score 0–100", 40, 85, ("'How cheap?'", "'How govern?'"), fmt="{:.0f}"),
    ),
    "463-data-lake-vs-warehouse": (
        "chart-layered-pattern.png",
        "Bar chart: workload coverage — single store vs lake landing + warehouse reporting (illustrative)",
        chart_lake_vs_warehouse_split,
    ),
    "464-data-warehouse-vs-data-lake": (
        "chart-workload-split.png",
        "Bar chart: fit for reporting vs data science — warehouse-only vs warehouse + lake (illustrative)",
        lambda p: chart_tool_stack_bars(
            p,
            "Workload fit: warehouse-only vs warehouse + lake (illustrative)",
            [("Reporting\n(WH only)", 90), ("Data science\n(WH only)", 35), ("Reporting\n(WH+lake)", 90), ("Data science\n(WH+lake)", 85)],
            ylabel="Fit score",
        ),
    ),
    "465-data-warehouse-software": (
        "chart-integration-cost.png",
        "Bar chart: integration cost — market leader vs cloud-matched warehouse software (illustrative)",
        lambda p: chart_before_after_bar(p, "Relative integration cost (illustrative)", "Cost index", 100, 45, ("Market leader", "Cloud-matched"), fmt="{:.0f}"),
    ),
    "466-data-lake-solutions": (
        "chart-swamp-avoidance.png",
        "Bar chart: swamp risk score — storage-first vs catalog+governance from day one (illustrative)",
        lambda p: chart_before_after_bar(p, "Swamp risk score (lower is better, illustrative)", "Risk 0–100", 82, 22, ("Storage first", "Gov from day 1"), fmt="{:.0f}"),
    ),
    "467-what-is-data-lake": (
        "chart-budget-question-quality.png",
        "Bar chart: budget-meeting question quality — vague vs governance-framed (illustrative)",
        lambda p: chart_before_after_bar(p, "Decision-quality of lake budget ask (illustrative)", "Score 0–100", 38, 84, ("Vague ask", "Governed ask"), fmt="{:.0f}"),
    ),
    "470-big-data-analytics-tools": (
        "chart-big-data-layers.png",
        "Bar chart: relative layer investment — storage, processing, query (illustrative stack)",
        lambda p: chart_tool_stack_bars(
            p,
            "Illustrative big-data stack investment by layer",
            [("Storage", 40), ("Processing", 35), ("Query", 25)],
            ylabel="Share of stack effort (%)",
        ),
    ),
    "471-data-visualization-tools": (
        "chart-viz-tool-fit.png",
        "Bar chart: audience fit — one tool for all vs BI + code library split (illustrative)",
        lambda p: chart_before_after_bar(p, "Audience fit score (illustrative)", "Score 0–100", 55, 90, ("One tool for all", "BI + code split"), fmt="{:.0f}"),
    ),
    "472-business-analytics-software": (
        "chart-self-service-adoption.png",
        "Line chart: analyst adoption — IT-only suite vs self-service analytics software (illustrative)",
        lambda p: chart_adoption_curve(p, "Analyst adoption of analytics software (illustrative)"),
    ),
    "473-what-is-data-analytics": (
        "chart-churn-forecast.png",
        "Line chart: moving from descriptive reports to predictive churn forecasting (illustrative)",
        chart_churn_forecast,
    ),
    "474-data-visualization-software": (
        "chart-license-fit.png",
        "Bar chart: annual software cost — enterprise suite for 3 users vs right-sized tool (illustrative)",
        lambda p: chart_before_after_bar(p, "Annual visualization software cost (illustrative)", "Cost index", 100, 22, ("Enterprise suite", "Right-sized"), fmt="{:.0f}"),
    ),
    "475-data-analytics-tools": (
        "chart-tools-by-job.png",
        "Bar chart: relative use by job — prepare, query, communicate (illustrative tool map)",
        lambda p: chart_tool_stack_bars(
            p,
            "Illustrative analytics tool use by job",
            [("Spreadsheet\nprepare", 30), ("SQL\nquery", 40), ("BI\ncommunicate", 30)],
            ylabel="Share of analyst time (%)",
        ),
    ),
    "476-data-analytics-software": (
        "chart-skill-fit-output.png",
        "Bar chart: output index — heavy software nobody uses vs skill-matched tools (illustrative)",
        lambda p: chart_before_after_bar(p, "Analyst output index (illustrative)", "Index", 40, 95, ("Heavy, unused", "Skill-matched"), fmt="{:.0f}"),
    ),
    "477-business-analytics-tools": (
        "chart-use-case-tools.png",
        "Bar chart: coverage by use case — one suite vs monitor + forecast tools (illustrative)",
        lambda p: chart_tool_stack_bars(
            p,
            "Use-case coverage: one suite vs purpose-picked tools (illustrative)",
            [("Monitor\n(suite)", 70), ("Forecast\n(suite)", 45), ("Monitor\n(picked)", 90), ("Forecast\n(picked)", 88)],
            ylabel="Coverage score",
        ),
    ),
    "478-tableau-data-visualization": (
        "chart-dashboard-trust.png",
        "Bar chart: executive trust in Tableau dashboards before and after metric definitions (illustrative)",
        lambda p: chart_before_after_bar(p, "Executives who trust the dashboards (illustrative)", "% trusting", 30, 85, ("Pretty, inconsistent", "Definitions fixed"), fmt="{:.0f}%"),
    ),
    "482-data-analytics-platforms": (
        "chart-platform-governance.png",
        "Bar chart: metric definition consistency across teams — fragmented vs integrated platform (illustrative)",
        lambda p: chart_before_after_bar(p, "Teams sharing one revenue definition (illustrative)", "Teams", 1, 5, ("Fragmented tools", "Integrated platform"), fmt="{:.0f}"),
    ),
    "483-data-analytics-platform": (
        "chart-shared-revenue-def.png",
        "Grouped bar chart: five teams' revenue figures before one analytics platform (illustrative)",
        lambda p: chart_grouped_defs(p, "Five teams, five revenue figures — then one platform (illustrative)"),
    ),
    "487-data-visualization-services": (
        "chart-build-vs-buy-services.png",
        "Bar chart: weeks to first executive dashboard — all in-house vs services then maintain (illustrative)",
        lambda p: chart_before_after_bar(p, "Weeks to first executive dashboard (illustrative)", "Weeks", 16, 5, ("All in-house", "Services → maintain"), fmt="{:.0f}w"),
    ),
}


def find_article(folder: str) -> Path | None:
    for pillar in list(BLOG.glob("pillar2[6-9]-*")) + list(BLOG.glob("pillar30-*")):
        d = pillar / folder
        art = d / "article.md"
        if art.is_file():
            return art
    return None


def insert_chart(art: Path, filename: str, alt: str) -> bool:
    text = art.read_text(encoding="utf-8")
    rel = f"./images/{filename}"
    if filename in text or rel in text:
        return False  # already inserted
    marker = re.compile(
        r"(\*\*Practical example:\*\*[^\n]*\n)",
        re.MULTILINE,
    )
    m = marker.search(text)
    if not m:
        print(f"  WARN no Practical example in {art.parent.name}")
        return False
    insert = f"\n![{alt}]({rel})\n"
    new_text = text[: m.end()] + insert + text[m.end() :]
    art.write_text(new_text, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ok = 0
    fail = 0
    inserted = 0
    for folder, (filename, alt, gen) in CHARTS.items():
        art = find_article(folder)
        if not art:
            print(f"SKIP missing article {folder}")
            fail += 1
            continue
        out = art.parent / "images" / filename
        print(f"▶ {folder} → {filename}")
        if args.dry_run:
            ok += 1
            continue
        try:
            gen(out)
            kb = out.stat().st_size // 1024
            print(f"  OK {out.relative_to(BLOG)} ({kb}KB)")
            if insert_chart(art, filename, alt):
                print("  inserted into article.md")
                inserted += 1
            else:
                print("  chart ref already present (or skip)")
            ok += 1
        except Exception as e:
            print(f"  FAIL {e}")
            fail += 1

    print(f"\nDone: charts={ok} fail={fail} inserts={inserted}")


if __name__ == "__main__":
    main()
