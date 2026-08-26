#!/usr/bin/env python3
"""Charts for 027-ai-excel-data-analysis-tools (≥2 dimensions)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
OUT = (
    ROOT
    / "SEO/Blog/Pillar 1-15/articles/pillar3-ai-analyst-tools"
    / "027-ai-excel-data-analysis-tools/images"
)
OUT.mkdir(parents=True, exist_ok=True)

TOOLS = [
    "Copilot\nExcel",
    "ChatGPT\nADA",
    "Claude",
    "Gemini\nSheets",
    "Julius",
    "Power BI\nCopilot",
    "Rows /\ncopilots",
    "InfiniSynapse",
]
DIMS = ["Clean", "Formula", "Pivot", "Chart", "Repeat", "Govern"]
# 0–2 scores matching the published scorecard in article.md
SCORES = np.array(
    [
        [2, 2, 2, 2, 1, 2],  # Copilot
        [2, 2, 2, 2, 1, 0],  # ChatGPT
        [2, 2, 1, 1, 1, 0],  # Claude
        [2, 1, 2, 1, 1, 1],  # Gemini
        [1, 1, 1, 2, 1, 0],  # Julius
        [1, 1, 2, 2, 1, 2],  # Power BI
        [1, 2, 1, 1, 1, 1],  # Rows
        [2, 1, 2, 1, 2, 2],  # InfiniSynapse
    ],
    dtype=float,
)


def radar() -> None:
    pick = [0, 1, 5, 7]  # Copilot, ChatGPT, Power BI, InfiniSynapse
    labels = ["Copilot in Excel", "ChatGPT ADA", "Power BI Copilot", "InfiniSynapse"]
    data = SCORES[pick]
    n = len(DIMS)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(8.0, 7.0), subplot_kw=dict(polar=True))
    colors = ["#0F766E", "#B45309", "#1D4ED8", "#5B5BFF"]
    for row, label, color in zip(data, labels, colors):
        vals = row.tolist() + row.tolist()[:1]
        ax.plot(angles, vals, color=color, linewidth=2, label=label)
        ax.fill(angles, vals, color=color, alpha=0.12)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMS, fontsize=10)
    ax.set_yticks([0, 1, 2])
    ax.set_ylim(0, 2)
    ax.set_rlabel_position(28)
    ax.set_title(
        "Excel AI scorecard radar — 4 tools × 6 dimensions (0–2)",
        pad=16,
        fontsize=12,
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1.38, 1.12), fontsize=9, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "chart-excel-ai-scorecard-radar.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def grouped_totals() -> None:
    totals = SCORES.sum(axis=1)
    repeat = SCORES[:, 4]
    govern = SCORES[:, 5]
    x = np.arange(len(TOOLS))
    w = 0.28
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.bar(x - w, totals, w, label="Total (max 12)", color="#5B5BFF")
    ax.bar(x, repeat, w, label="Repeatability (0–2)", color="#0F766E")
    ax.bar(x + w, govern, w, label="Governance (0–2)", color="#B45309")
    ax.set_xticks(x)
    ax.set_xticklabels(TOOLS, fontsize=8)
    ax.set_ylim(0, 12)
    ax.set_ylabel("Score")
    ax.set_title("First-party pilot scores — total vs repeatability vs governance")
    ax.legend(frameon=False, fontsize=9)
    ax.axhline(9, color="#9CA3AF", linewidth=0.8, linestyle="--")
    fig.tight_layout()
    fig.savefig(OUT / "chart-excel-ai-score-totals.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    radar()
    grouped_totals()
    print("wrote", OUT / "chart-excel-ai-scorecard-radar.png")
    print("wrote", OUT / "chart-excel-ai-score-totals.png")
