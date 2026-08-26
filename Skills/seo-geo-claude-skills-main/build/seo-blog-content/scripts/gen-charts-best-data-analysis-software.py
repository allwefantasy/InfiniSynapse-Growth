#!/usr/bin/env python3
"""Charts for /use-cases/best-data-analysis-software (≥2 dimensions each)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / "SEO/Blog/use-cases/best-data-analysis-software/images"
OUT.mkdir(parents=True, exist_ok=True)

TOOLS = [
    "InfiniSynapse",
    "Power BI",
    "Tableau",
    "Looker",
    "Hex",
    "Mode",
    "Sisense",
    "Julius AI",
]
DIMS = [
    "AI / NL",
    "Source\nbreadth",
    "Scale",
    "Reporting",
    "Learning",
    "Pricing",
    "Deployment",
]
# rows match TOOLS order; columns match DIMS
SCORES = np.array(
    [
        [5, 5, 4, 3, 4, 3, 5],  # InfiniSynapse
        [3, 4, 4, 5, 4, 5, 3],  # Power BI
        [3, 4, 4, 5, 3, 4, 4],  # Tableau
        [3, 4, 5, 4, 2, 2, 2],  # Looker
        [3, 3, 4, 4, 3, 4, 2],  # Hex
        [3, 3, 4, 4, 2, 4, 2],  # Mode
        [3, 4, 4, 4, 2, 2, 4],  # Sisense
        [4, 2, 2, 3, 5, 5, 1],  # Julius AI
    ],
    dtype=float,
)

TASKS = [
    "Agg",
    "Rank",
    "Time+",
    "Cohort",
    "Multi-src",
    "Diagnose",
    "Unstruct",
    "Mixed",
    "Ambiguity",
    "Schema",
    "Narrative",
    "Multi-step",
]
# columns = tools in protocol-table order
HEAT_TOOLS = [
    "InfiniSynapse",
    "Tableau",
    "Power BI",
    "Looker",
    "Julius AI",
    "Hex",
    "Mode",
    "Sisense",
]
HEAT = np.array(
    [
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0],
        [1.0, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 0.5],
        [1.0, 0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5],
        [1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5],
        [1.0, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5],
        [1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5],
        [0.5, 0.0, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0],
    ],
    dtype=float,
)


def radar() -> None:
    # Top-4 tools for readability (still multi-series × multi-dimension)
    pick = [0, 1, 2, 7]  # InfiniSynapse, Power BI, Tableau, Julius
    labels = [TOOLS[i] for i in pick]
    data = SCORES[pick]
    n = len(DIMS)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8.2, 7.2), subplot_kw=dict(polar=True))
    colors = ["#5B5BFF", "#0F766E", "#B45309", "#9333EA"]
    for row, label, color in zip(data, labels, colors):
        vals = row.tolist() + row.tolist()[:1]
        ax.plot(angles, vals, color=color, linewidth=2, label=label)
        ax.fill(angles, vals, color=color, alpha=0.12)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMS, fontsize=9)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)
    ax.set_rlabel_position(28)
    ax.set_title(
        "Category-fit radar — 7 weighted dimensions × 4 tools (1–5)",
        pad=18,
        fontsize=12,
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.12), fontsize=9, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "chart-category-fit-radar.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def heatmap() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 6.8))
    im = ax.imshow(HEAT, cmap="YlGnBu", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(HEAT_TOOLS)))
    ax.set_xticklabels(HEAT_TOOLS, rotation=30, ha="right", fontsize=9)
    ax.set_yticks(range(len(TASKS)))
    ax.set_yticklabels([f"{i+1}. {t}" for i, t in enumerate(TASKS)], fontsize=9)
    for y in range(HEAT.shape[0]):
        for x in range(HEAT.shape[1]):
            v = HEAT[y, x]
            ax.text(
                x,
                y,
                f"{v:g}",
                ha="center",
                va="center",
                color="white" if v >= 0.75 else "#111827",
                fontsize=8,
            )
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("Task score (0 / 0.5 / 1.0)")
    ax.set_title("12-task NL-analysis protocol heatmap — task × tool")
    fig.tight_layout()
    fig.savefig(OUT / "chart-protocol-heatmap.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    radar()
    heatmap()
    print("wrote", OUT / "chart-category-fit-radar.png")
    print("wrote", OUT / "chart-protocol-heatmap.png")
