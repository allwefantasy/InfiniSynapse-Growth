#!/usr/bin/env python3
"""Audit pairwise external-link overlap across pillar articles (must be <= 30%)."""
from __future__ import annotations

import importlib.util
import re
import sys
from itertools import combinations
from pathlib import Path
from urllib.parse import urlparse

BLOG = Path(__file__).parent
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar2-data-agent-vs-alternatives",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

MAX_OVERLAP = 0.30

_spec = importlib.util.spec_from_file_location("ext_audit", BLOG / "audit-external-links.py")
_ext = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_ext)


def norm(url: str) -> str:
    return url.rstrip("/").lower()


def overlap_rate(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def collect_articles(targets: list[Path]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for pillar in targets:
        if not pillar.is_dir():
            continue
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            urls = {norm(u) for u in _ext.external_links(art.read_text(encoding="utf-8"))}
            out[art.parent.name] = urls
    return out


def audit_pairs(articles: dict[str, set[str]]) -> list[tuple[float, str, str, int, int]]:
    violations: list[tuple[float, str, str, int, int]] = []
    for a, b in combinations(sorted(articles), 2):
        sa, sb = articles[a], articles[b]
        rate = overlap_rate(sa, sb)
        if rate > MAX_OVERLAP:
            violations.append((rate, a, b, len(sa & sb), min(len(sa), len(sb))))
    violations.sort(reverse=True)
    return violations


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    articles = collect_articles(targets)
    violations = audit_pairs(articles)
    pairs = len(list(combinations(articles, 2)))
    print(f"Articles: {len(articles)} | Pairs: {pairs}")
    print(f"Violations (>{MAX_OVERLAP:.0%}): {len(violations)}")
    if violations:
        print("\nWorst 20 pairs:")
        for rate, a, b, inter, denom in violations[:20]:
            print(f"  {rate:.0%}\t{a} vs {b}\t({inter}/{denom})")
    worst = violations[0] if violations else None
    if worst:
        print(f"\nMax overlap: {worst[0]:.0%} — {worst[1]} vs {worst[2]}")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
