#!/usr/bin/env python3
"""Render the two body data charts for 409-data-catalog-platforms.

1. chart-catalog-fill-rate.png  — month x rollout approach (2 series, values match body copy)
2. chart-category-fit-radar.png — six weighted criteria x three platform categories

Both follow references/body-data-chart-rules.md: >=2 data dimensions, illustrative
labelling, white background, teal/blue/rose functional palette.

Usage:
  python3 gen-charts-409-data-catalog-platforms.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
IMAGES = (
    ROOT
    / "SEO"
    / "Blog"
    / "pillar27-master-data-catalog-lineage"
    / "409-data-catalog-platforms"
    / "images"
)

INK = "#1a1f2e"
MUTED = "#5c6578"
GRID = "#e8ebf0"
TEAL = "#0d9488"
SLATE = "#94a3b8"
BLUE = "#2563eb"
ROSE = "#e11d48"


def save(fig, name: str) -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGES / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {IMAGES / name}")


def fill_rate_chart() -> None:
    """Manual-entry vs automated-discovery fill rate; anchors 35% @ m6 and 88% @ m4."""
    months = np.arange(1, 13)
    manual = np.array([6, 12, 19, 25, 31, 35, 37, 38, 39, 40, 40, 41], dtype=float)
    automated = np.array([22, 46, 71, 88, 91, 93, 94, 94, 95, 95, 96, 96], dtype=float)

    fig, ax = plt.subplots(figsize=(9.0, 5.1))
    ax.plot(months, manual, marker="o", color=SLATE, linewidth=2.4,
            label="Manual entry first")
    ax.plot(months, automated, marker="s", color=TEAL, linewidth=2.4,
            label="Automated discovery first")

    for x, y, txt, colour, va in (
        (6, 35, "35% by month 6", MUTED, "top"),
        (4, 88, "88% by month 4", TEAL, "bottom"),
    ):
        ax.annotate(
            txt,
            xy=(x, y),
            xytext=(x + 0.4, y - 9 if va == "top" else y + 5),
            fontsize=10,
            fontweight="600",
            color=colour,
        )
        ax.plot([x], [y], marker="o", markersize=9, markerfacecolor="white",
                markeredgecolor=colour, markeredgewidth=2, zorder=5)

    ax.set_title(
        "Catalog fill rate for priority tables (illustrative)",
        fontsize=13.5, fontweight="600", color=INK, pad=12,
    )
    ax.set_xlabel("Month after kickoff", fontsize=10, color=MUTED)
    ax.set_ylabel("Priority tables with owner + definition (%)", fontsize=10, color=MUTED)
    ax.set_xticks(months)
    ax.set_ylim(0, 105)
    ax.legend(frameon=False, fontsize=10, loc="lower right")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    save(fig, "chart-catalog-fill-rate.png")


def category_fit_radar() -> None:
    """Six weighted criteria x three catalog categories, scored 1-3 from the body matrix."""
    criteria = [
        "Auto discovery\n& refresh (25%)",
        "Lineage depth\n(20%)",
        "Stewardship UX\n(15%)",
        "Governance hooks\n(15%)",
        "Cross-stack fit\n(15%)",
        "Machine-readable\nmetadata (10%)",
    ]
    series = {
        "Standalone (Alation, Collibra)": [2.5, 3.0, 3.0, 2.5, 3.0, 2.2],
        "Cloud-embedded (Purview, UC, Glue)": [3.0, 2.4, 1.7, 2.7, 1.5, 2.1],
        "Open metadata (DataHub)": [2.5, 3.0, 2.0, 2.0, 2.5, 3.0],
    }
    colours = (TEAL, BLUE, ROSE)

    angles = np.linspace(0, 2 * np.pi, len(criteria), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7.6, 7.0), subplot_kw={"polar": True})
    for (label, values), colour in zip(series.items(), colours):
        vals = values + values[:1]
        ax.plot(angles, vals, color=colour, linewidth=2.2, label=label)
        ax.fill(angles, vals, color=colour, alpha=0.10)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(criteria, fontsize=9.5, color=INK)
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Limited", "Moderate", "Strong"], fontsize=9, color=MUTED)
    ax.set_rlabel_position(30)
    ax.set_ylim(0, 3.2)
    ax.grid(color=GRID, linewidth=0.9)
    ax.spines["polar"].set_color(GRID)
    ax.set_title(
        "Relative fit by catalog category (editorial ratings, 1–3)",
        fontsize=13.5, fontweight="600", color=INK, pad=26,
    )
    ax.legend(
        frameon=False, fontsize=9.5, loc="upper center", bbox_to_anchor=(0.5, -0.06)
    )
    save(fig, "chart-category-fit-radar.png")


if __name__ == "__main__":
    fill_rate_chart()
    category_fit_radar()
