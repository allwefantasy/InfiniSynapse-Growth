#!/usr/bin/env python3
"""Generate pillar-hub-section-checklist.csv — required Ultimate Guide sections per Hub."""
from __future__ import annotations

import csv
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BLOG = ROOT / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
OUT = BLOG / "pillar-hub-section-checklist.csv"

_spec = importlib.util.spec_from_file_location("reg", SCRIPTS / "cluster-link-registry.py")
reg = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(reg)

REQUIRED_H2 = [
    "TL;DR",
    "definition_or_what",
    "core_framework",
    "methodology_comparison",
    "tool_landscape",
    "workflow_implementation",
    "case_or_production",
    "scorecard_or_choose",
    "failure_modes",
    "cluster_guides_table",
    "faq",
    "conclusion",
]

H2_PATTERNS: dict[str, list[str]] = {
    "definition_or_what": [
        r"what .+ means",
        r"key definition",
        r"^## definition",
        r"^## why ",
    ],
    "core_framework": [
        r"five core",
        r"core requirements",
        r"architecture",
        r"framework",
        r"operational scorecard",
        r"core components",
    ],
    "methodology_comparison": [
        r"category split",
        r"vs ",
        r"comparison",
        r"methodology",
        r"solution categories",
    ],
    "tool_landscape": [
        r"tool landscape",
        r"buyer scorecard",
        r"vendor",
        r"tools for",
    ],
    "workflow_implementation": [
        r"workflow",
        r"implementation",
        r"step-by-step",
        r"roadmap",
        r"playbook",
    ],
    "case_or_production": [
        r"case",
        r"production pattern",
        r"real-world",
        r"infiniSynapse production",
    ],
    "scorecard_or_choose": [
        r"how to choose",
        r"buyer scorecard",
        r"evaluation",
        r"starting point",
    ],
    "failure_modes": [
        r"failure",
        r"pitfall",
    ],
}


def body_words(md: str) -> int:
    text = md.split("## TL;DR", 1)[-1] if "## TL;DR" in md else md
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return len(re.findall(r"[A-Za-z0-9']+", text))


def has_section(md: str, key: str) -> bool:
    if key == "TL;DR":
        return "## TL;DR" in md
    if key == "cluster_guides_table":
        return "## Cluster guides in this pillar" in md
    if key == "faq":
        return "## Frequently Asked Questions" in md
    if key == "conclusion":
        return "## Conclusion" in md
    low = md.lower()
    return any(re.search(p, low) for p in H2_PATTERNS.get(key, []))


def main() -> None:
    rows = []
    for pillar_dir in reg.PILLAR_DIRS:
        hub_folder = reg.PRIMARY_HUB[pillar_dir.name]
        md_path = pillar_dir / hub_folder / "article.md"
        md = md_path.read_text(encoding="utf-8")
        wc = body_words(md)
        missing = [k for k in REQUIRED_H2 if not has_section(md, k)]
        h2n = len(re.findall(r"^## ", md, re.M))
        rows.append(
            {
                "pillar_dir": pillar_dir.name,
                "hub_folder": hub_folder,
                "hub_slug": reg.slug_from_folder(hub_folder),
                "word_count": wc,
                "h2_count": h2n,
                "word_count_ok": "yes" if wc >= 2000 else "no",
                "missing_sections": "; ".join(missing) if missing else "",
                "structure_pass": "yes" if not missing and wc >= 2000 else "review",
            }
        )

    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    pass_n = sum(1 for r in rows if r["structure_pass"] == "yes")
    print(f"Wrote {OUT}")
    print(f"  structure pass: {pass_n}/{len(rows)}")


if __name__ == "__main__":
    main()
