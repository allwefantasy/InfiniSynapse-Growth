#!/usr/bin/env python3
"""Render the framework comparison matrix for 388-data-governance-frameworks.

chart-framework-comparison-matrix.png — six published models x five selection
dimensions, scored 0-3 from each model's own primary documentation. Supports the
"Where NIST Fits" section: no model scores high everywhere, so regulated programs
run a discipline-based backbone plus a NIST control overlay.

Follows references/body-data-chart-rules.md: >=2 data dimensions, illustrative
labelling, white background, teal/blue/rose functional palette.

Usage:
  python3 gen-charts-388-data-governance-frameworks.py
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
    / "pillar26-data-governance-quality"
    / "388-data-governance-frameworks"
    / "images"
)

INK = "#1a1f2e"
MUTED = "#5c6578"

MODELS = [
    "DAMA-DMBOK",
    "DCAM",
    "ISO/IEC 38505",
    "CMMI DMM",
    "NIST Privacy\nFramework",
    "NIST AI RMF",
]

DIMENSIONS = [
    "Breadth of\ncoverage",
    "Audit /\nevidence fit",
    "Maturity\nscoring",
    "AI-era\nrelevance",
    "Low cost\nto adopt",
]

# 0 = not addressed, 1 = partial, 2 = solid, 3 = the model's core strength.
# Read from each body's own primary publication, not from vendor summaries.
SCORES = np.array(
    [
        [3, 1, 1, 1, 2],  # DAMA-DMBOK
        [2, 3, 3, 1, 1],  # DCAM
        [1, 2, 1, 1, 2],  # ISO/IEC 38505
        [2, 2, 3, 1, 2],  # CMMI DMM
        [1, 3, 1, 2, 2],  # NIST Privacy Framework
        [1, 2, 1, 3, 3],  # NIST AI RMF
    ],
    dtype=float,
)


def save(fig, name: str) -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGES / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {IMAGES / name}")


def comparison_matrix() -> None:
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    im = ax.imshow(SCORES, cmap="GnBu", vmin=0, vmax=3.6, aspect="auto")

    ax.set_xticks(range(len(DIMENSIONS)))
    ax.set_xticklabels(DIMENSIONS, fontsize=9.5, color=INK)
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels(MODELS, fontsize=9.5, color=INK)
    ax.set_xticks(np.arange(-0.5, len(DIMENSIONS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(MODELS), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2.5)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(which="major", length=0)
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

    ax.set_title(
        "Data governance frameworks — strength by selection dimension (0–3)",
        fontsize=12.5,
        color=INK,
        pad=14,
    )

    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3], fraction=0.032, pad=0.03)
    cbar.ax.set_yticklabels(
        ["0 not addressed", "1 partial", "2 solid", "3 core strength"], fontsize=8.5
    )
    cbar.outline.set_visible(False)

    fig.subplots_adjust(bottom=0.2)
    fig.text(
        0.03,
        -0.02,
        "Scored from each body's own primary publication. A model-fit map, not a ranking — "
        "no model scores high on every dimension,\nwhich is why regulated programs pair a "
        "discipline-based backbone with a NIST control overlay.",
        fontsize=8.8,
        color=MUTED,
        style="italic",
    )

    save(fig, "chart-framework-comparison-matrix.png")


if __name__ == "__main__":
    comparison_matrix()
