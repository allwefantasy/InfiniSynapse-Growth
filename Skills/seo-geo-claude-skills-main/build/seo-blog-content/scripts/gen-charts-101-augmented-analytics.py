#!/usr/bin/env python3
"""Charts for 101-augmented-analytics.

Figure 1 — four-pillar pipeline into the analyst approval gate.
Figure 2 — archetype x dimension 0-2 heatmap (must match the scorecard table in article.md).
Figure 3 — 30/60/90 rollout timeline with exit criteria.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[5]
OUT = (
    ROOT
    / "SEO/Blog/Pillar 1-15/articles/pillar1-ai-native-data-analysis"
    / "101-augmented-analytics/images"
)
OUT.mkdir(parents=True, exist_ok=True)

INK = "#1F2937"
BRAND = "#5B5BFF"
TEAL = "#0F766E"
AMBER = "#B45309"
GREY = "#9CA3AF"

DIMS = [
    "Metric\ngrounding",
    "Explain-\nability",
    "Human\nworkflow",
    "Access\ncontrol",
    "Integra-\ntion",
    "Audit\ntrail",
]
ARCHETYPES = [
    "BI-native copilots",
    "Notebook AI assist",
    "Warehouse-native NL",
    "AI-native Data Agents",
]
# Mirrors the "Archetype scores" table in article.md. Keep both in sync.
SCORES = np.array(
    [
        [2, 1, 2, 2, 2, 1],
        [1, 2, 2, 1, 1, 2],
        [2, 2, 1, 2, 1, 2],
        [2, 2, 1, 2, 2, 2],
    ],
    dtype=float,
)


def _box(ax, x, y, w, h, text, face, edge, fontsize=10, weight="normal", tc=INK):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=face,
            edgecolor=edge,
            linewidth=1.4,
        )
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=tc,
        weight=weight,
    )


def pillars() -> None:
    fig, ax = plt.subplots(figsize=(11.0, 6.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    ax.text(
        0.2,
        5.85,
        "The 4 pillars of augmented analytics — every path ends at the same approval gate",
        fontsize=13,
        weight="bold",
        color=INK,
    )
    ax.text(
        0.2,
        5.5,
        "Automated by the platform (left)  →  owned by a named human (right)",
        fontsize=9.5,
        color=GREY,
    )

    pillars_ = [
        ("Data prep", "Profiling, typing,\njoin hints", "Pipeline approval"),
        ("Insight discovery", "Anomalies, drivers,\nclusters", "Which insights publish"),
        ("Natural-language query", "Question → SQL /\ngoverned metrics", "Metric definitions"),
        ("Narrative / AutoML", "Draft explanations,\nmodel suggestions", "Sign-off & caveats"),
    ]
    top = 4.55
    step = 1.06
    for i, (name, auto, human) in enumerate(pillars_):
        y = top - i * step
        _box(ax, 0.2, y, 2.35, 0.86, f"{name}\n", "#EEF2FF", BRAND, 9.5, "bold")
        ax.text(1.375, y + 0.30, auto, ha="center", va="center", fontsize=8.2, color=INK)
        ax.add_patch(
            FancyArrowPatch(
                (2.62, y + 0.43),
                (4.28, y + 0.43),
                arrowstyle="-|>",
                mutation_scale=13,
                color=GREY,
                linewidth=1.2,
            )
        )
        _box(ax, 4.35, y + 0.06, 2.25, 0.74, human, "#FFFFFF", GREY, 8.6)
        ax.add_patch(
            FancyArrowPatch(
                (6.68, y + 0.43),
                (7.55, 2.85),
                arrowstyle="-|>",
                mutation_scale=13,
                color=TEAL,
                linewidth=1.2,
                connectionstyle="arc3,rad=0.12",
            )
        )

    _box(
        ax,
        7.62,
        2.10,
        1.55,
        1.55,
        "Analyst\napproval\ngate",
        "#ECFDF5",
        TEAL,
        10.5,
        "bold",
        TEAL,
    )
    ax.add_patch(
        FancyArrowPatch(
            (9.22, 2.87),
            (9.85, 2.87),
            arrowstyle="-|>",
            mutation_scale=13,
            color=TEAL,
            linewidth=1.4,
        )
    )
    _box(ax, 9.9, 2.35, 1.0, 1.05, "Published\ninsight", "#FFFFFF", TEAL, 9, "bold")

    ax.text(
        0.2,
        0.42,
        "Bypassing the gate on any pillar means the platform is selling autonomy, not augmentation.",
        fontsize=9,
        color=AMBER,
        style="italic",
    )
    fig.tight_layout()
    fig.savefig(OUT / "chart-augmented-analytics-pillars.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def heatmap() -> None:
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    im = ax.imshow(SCORES, cmap="BuPu", vmin=0, vmax=2.6, aspect="auto")

    ax.set_xticks(range(len(DIMS)))
    ax.set_xticklabels(DIMS, fontsize=9)
    ax.set_yticks(range(len(ARCHETYPES)))
    ax.set_yticklabels(ARCHETYPES, fontsize=9.5)
    ax.set_xticks(np.arange(-0.5, len(DIMS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(ARCHETYPES), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)

    for i in range(SCORES.shape[0]):
        for j in range(SCORES.shape[1]):
            v = SCORES[i, j]
            ax.text(
                j,
                i,
                f"{int(v)}",
                ha="center",
                va="center",
                fontsize=12,
                weight="bold",
                color="white" if v >= 2 else INK,
            )
        ax.annotate(
            f"total {int(SCORES[i].sum())}/12",
            xy=(1.015, i),
            xycoords=("axes fraction", "data"),
            ha="left",
            va="center",
            fontsize=9,
            weight="bold",
            color=INK,
            annotation_clip=False,
        )

    ax.set_title(
        "Augmented analytics buyer scorecard — typical score by archetype (0–2)",
        fontsize=12,
        pad=12,
    )
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2], fraction=0.03, pad=0.16)
    cbar.ax.set_yticklabels(["0 absent", "1 partial", "2 unattended"], fontsize=8)
    fig.subplots_adjust(bottom=0.24)
    fig.text(
        0.06,
        0.045,
        "Archetype-level reading from vendor docs + our pilots — not a product ranking. "
        "Fill your own grid before buying.",
        fontsize=8.6,
        color=GREY,
        style="italic",
    )
    fig.savefig(
        OUT / "chart-augmented-analytics-scorecard-heatmap.png", dpi=160, bbox_inches="tight"
    )
    plt.close(fig)


def timeline() -> None:
    fig, ax = plt.subplots(figsize=(10.6, 4.6))
    windows = [
        (0, 30, "Days 1–30 · Metric contracts", BRAND,
         "Exit: same question → same total in BI and NL"),
        (30, 30, "Days 31–60 · Approval workflow + audit logs", TEAL,
         "Exit: override rate 5–15%; P95 answer < 8s warm"),
        (60, 30, "Days 61–90 · Expand seats, optional agentic mode", AMBER,
         "Exit: rerun consistent within 48h; no unreviewed auto-publish"),
    ]
    for i, (start, width, label, color, exit_text) in enumerate(windows):
        y = 2.0 - i * 0.85
        ax.broken_barh([(start, width)], (y, 0.34), facecolors=color, alpha=0.9)
        ax.text(start, y + 0.44, label, va="bottom", fontsize=10, color=color, weight="bold")
        ax.text(95, y + 0.17, exit_text, va="center", fontsize=9, color=INK)
        ax.plot(
            [start + width, start + width],
            [y - 0.06, y + 0.40],
            color=GREY,
            linewidth=1,
            linestyle="--",
        )

    ax.set_xlim(0, 250)
    ax.set_ylim(0.20, 2.75)
    ax.set_yticks([])
    ax.set_xticks([0, 30, 60, 90])
    ax.set_xticklabels(["Day 0", "Day 30", "Day 60", "Day 90"], fontsize=9)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.set_title(
        "Augmented analytics rollout — 30 / 60 / 90 windows and their exit criteria",
        fontsize=12,
        loc="left",
        pad=14,
    )
    fig.subplots_adjust(bottom=0.22)
    fig.text(
        0.06,
        0.05,
        "Do not open the next window until the current exit criterion passes on your own stack.",
        fontsize=9,
        color=GREY,
        style="italic",
    )
    fig.savefig(
        OUT / "chart-augmented-analytics-rollout-timeline.png", dpi=160, bbox_inches="tight"
    )
    plt.close(fig)


if __name__ == "__main__":
    pillars()
    heatmap()
    timeline()
    for f in sorted(OUT.glob("chart-augmented-analytics-*.png")):
        print("wrote", f)
