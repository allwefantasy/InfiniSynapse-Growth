#!/usr/bin/env python3
"""Assign disjoint high-DR URL sets to pillar10/pillar11 articles to pass overlap audit."""
from __future__ import annotations

import importlib.util
import random
import re
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HDR_PATH = ROOT / "Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/high-dr-authority-sources.py"
_spec = importlib.util.spec_from_file_location("hdr", HDR_PATH)
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)

PILLARS = [
    ROOT / "SEO/Blog/pillar10-mcp-data-access",
    ROOT / "SEO/Blog/pillar11-agentic-analytics",
]
MAX_OVERLAP = 0.30
PER_ARTICLE = 7


def norm(u: str) -> str:
    return u.rstrip("/").lower()


def overlap_rate(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def violation_count(assign: dict[str, list[dict]]) -> int:
    n = 0
    keys = list(assign.keys())
    for i, j in combinations(keys, 2):
        sa = {norm(s["url"]) for s in assign[i]}
        sb = {norm(s["url"]) for s in assign[j]}
        if overlap_rate(sa, sb) > MAX_OVERLAP:
            n += 1
    return n


def best_assignment(articles: list[str], pool: list[dict], trials: int = 5000) -> dict[str, list[dict]]:
    best: dict[str, list[dict]] = {}
    best_v = 10**9
    rng = random.Random(42)
    for _ in range(trials):
        assign: dict[str, list[dict]] = {}
        shuffled = pool[:]
        rng.shuffle(shuffled)
        idx = 0
        for art in articles:
            group = []
            for _ in range(PER_ARTICLE):
                group.append(shuffled[idx % len(shuffled)])
                idx += 1
            assign[art] = group
        v = violation_count(assign)
        if v < best_v:
            best_v = v
            best = {k: v[:] for k, v in assign.items()}
        if best_v == 0:
            break
    print(f"Best violations: {best_v} after search")
    return best


def replace_external_weaves(text: str, sources: list[dict]) -> str:
    """Remove existing external-link narrative paragraphs in body and inject assigned weaves."""
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    if not m:
        return text
    head, body = text[:m.start()], text[m.start():]
    # strip lines that contain external http links (keep internal /en/blog/)
    lines = body.splitlines()
    cleaned = []
    for line in lines:
        if re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", line):
            if "infinisynapse" in line:
                cleaned.append(line)
            continue
        cleaned.append(line)
    body = "\n".join(cleaned)
    # insert weaves after key section markers
    weaves = [s["weave"].format(url=s["url"]) for s in sources]
    markers = [
        "## Why This Matters in 2026",
        "## Definition",
        "## Governed Access vs Ad-Hoc Prompts",
        "## Agent Loops vs Copilots vs Dashboards",
        "## Core Components",
        "## Core Capabilities",
        "## Architecture Reference Model",
        "## Production Validation Notes",
        "## Proof-of-Value Metrics",
    ]
    wi = 0
    for marker in markers:
        if marker not in body or wi >= len(weaves):
            continue
        body = body.replace(marker, f"{weaves[wi]}\n\n---\n\n{marker}", 1)
        wi += 1
    while wi < len(weaves):
        marker = "## Stakeholder Rollout Notes"
        if marker in body:
            body = body.replace(marker, f"{weaves[wi]}\n\n{marker}", 1)
            wi += 1
        else:
            break
    return head + body


def main() -> None:
    pool = [s for s in _hdr.HIGH_DR_SOURCES if "cortex-analyst" not in s.get("url", "")]
    articles: list[str] = []
    paths: dict[str, Path] = {}
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            articles.append(art.parent.name)
            paths[art.parent.name] = art

    assign = best_assignment(articles, pool)
    for name, sources in assign.items():
        path = paths[name]
        text = path.read_text(encoding="utf-8")
        new_text = replace_external_weaves(text, sources)
        path.write_text(new_text, encoding="utf-8")
        print(f"updated {name} ({len(sources)} cites)")


if __name__ == "__main__":
    main()
