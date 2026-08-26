#!/usr/bin/env python3
"""Render the per-tool criteria heatmap for 005-best-agentic-analytics.

chart-agentic-analytics-tool-criteria-heatmap.png — six tools x eight evaluation
criteria, scored 0-3, with per-tool totals out of 24. Values are identical to the
scorecard table in the article body.

The report flagged that the eight criteria were defined but never scored per tool,
and that the only existing chart grouped by tool *class* rather than by product.
This chart closes both gaps and makes the first-party losses visible (Julius wins
time-to-answer; three competitors outscore InfiniSynapse on governance).

Follows references/body-data-chart-rules.md: >=2 data dimensions, illustrative
labelling, white background, teal/blue/rose functional palette.

Usage:
  python3 gen-charts-005-best-agentic-analytics.py
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
    / "Pillar 1-15"
    / "articles"
    / "pillar1-ai-native-data-analysis"
    / "005-best-agentic-analytics"
    / "images"
)

INK = "#1a1f2e"
MUTED = "#5c6578"

TOOLS = [
    "ThoughtSpot\nSpotter",
    "Hex\nMagic",
    "Databricks\nGenie",
    "Julius\nAI",
    "Fabric\nCopilot",
    "InfiniSynapse\n(first-party)",
]

CRITERIA = [
    "Autonomy depth",
    "Process transparency",
    "Knowledge accumulation",
    "Multi-source execution",
    "Self-correction",
    "Governance",
    "Entry points",
    "Time-to-answer",
]

# rows = criteria, cols = tools. Identical to the article's scorecard table.
# 0 absent | 1 partial or manual | 2 solid | 3 unattended, production-grade
SCORES = np.array(
    [
        [2, 2, 2, 2, 1, 3],  # Autonomy depth
        [2, 3, 2, 2, 1, 3],  # Process transparency
        [1, 1, 1, 0, 1, 3],  # Knowledge accumulation
        [1, 2, 1, 1, 2, 3],  # Multi-source execution
        [1, 1, 1, 1, 1, 3],  # Self-correction
        [3, 2, 3, 1, 3, 2],  # Governance
        [2, 2, 2, 2, 2, 3],  # Entry points
        [2, 2, 2, 3, 2, 2],  # Time-to-defensible-answer
    ],
    dtype=float,
)


def save(fig, name: str) -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGES / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {IMAGES / name}")


def tool_criteria_heatmap() -> None:
    fig, ax = plt.subplots(figsize=(10.4, 6.4))
    im = ax.imshow(SCORES, cmap="GnBu", vmin=0, vmax=3.6, aspect="auto")

    ax.set_xticks(range(len(TOOLS)))
    ax.set_xticklabels(TOOLS, fontsize=9.5, color=INK)
    ax.set_yticks(range(len(CRITERIA)))
    ax.set_yticklabels(CRITERIA, fontsize=9.5, color=INK)
    ax.set_xticks(np.arange(-0.5, len(TOOLS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(CRITERIA), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2.5)
    ax.tick_params(which="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    for i in range(SCORES.shape[0]):
        for j in range(SCORES.shape[1]):
            v = SCORES[i, j]
            ax.text(
                j,
                i,
                f"{int(v)}",
                ha="center",
                va="center",
                fontsize=12.5,
                weight="bold",
                color="white" if v >= 3 else INK,
            )

    totals = SCORES.sum(axis=0)
    for j, total in enumerate(totals):
        ax.annotate(
            f"{int(total)}/24",
            xy=(j, -0.72),
            xycoords=("data", "data"),
            ha="center",
            va="center",
            fontsize=10.5,
            weight="bold",
            color=INK,
            annotation_clip=False,
        )
    ax.annotate(
        "total",
        xy=(-0.62, -0.72),
        xycoords=("data", "data"),
        ha="right",
        va="center",
        fontsize=9.5,
        style="italic",
        color=MUTED,
        annotation_clip=False,
    )

    ax.set_title(
        "Agentic analytics tools — score by evaluation criterion (0–3)",
        fontsize=13,
        color=INK,
        pad=34,
    )

    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3], fraction=0.03, pad=0.03)
    cbar.ax.set_yticklabels(
        ["0 absent", "1 partial", "2 solid", "3 unattended"], fontsize=8.5
    )
    cbar.outline.set_visible(False)

    fig.text(
        0.03,
        -0.03,
        "Ten cold runs per tool, one synthetic 12-table e-commerce schema, Q1–Q2 2026. First-party and unaudited — "
        "InfiniSynapse is scored by its own vendor\nand loses time-to-answer to Julius and governance to ThoughtSpot, "
        "Genie and Fabric. A POC template, not a market ranking.",
        fontsize=8.8,
        color=MUTED,
        style="italic",
    )

    save(fig, "chart-agentic-analytics-tool-criteria-heatmap.png")


if __name__ == "__main__":
    tool_criteria_heatmap()
