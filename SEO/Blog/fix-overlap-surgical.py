#!/usr/bin/env python3
"""Pairwise surgical overlap fix — one shared-URL swap per step, only if violations decrease."""
from __future__ import annotations

import importlib.util
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

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
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")

_spec = importlib.util.spec_from_file_location("ext_audit", BLOG / "audit-external-links.py")
_ext = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_ext)

_hdr_spec = importlib.util.spec_from_file_location("hdr", BLOG / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_hdr_spec)
assert _hdr_spec and _hdr_spec.loader
_hdr_spec.loader.exec_module(_hdr)


def norm(url: str) -> str:
    return url.rstrip("/").lower()


def overlap_rate(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def article_path(slug: str) -> Path | None:
    for pillar in PILLARS:
        p = pillar / slug / "article.md"
        if p.is_file():
            return p
    return None


def collect_articles() -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for pillar in PILLARS:
        if not pillar.is_dir():
            continue
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            urls = {norm(u) for u in _ext.external_links(art.read_text(encoding="utf-8"))}
            out[art.parent.name] = urls
    return out


def violations(articles: dict[str, set[str]]) -> list[tuple[float, str, str]]:
    out: list[tuple[float, str, str]] = []
    for a, b in combinations(sorted(articles), 2):
        rate = overlap_rate(articles[a], articles[b])
        if rate > MAX_OVERLAP:
            out.append((rate, a, b))
    out.sort(reverse=True)
    return out


def global_usage(articles: dict[str, set[str]]) -> Counter[str]:
    c: Counter[str] = Counter()
    for urls in articles.values():
        for u in urls:
            c[u] += 1
    return c


def swap_url(path: Path, old_url: str, new_src: dict) -> bool:
    text = path.read_text(encoding="utf-8")
    old_n = norm(old_url)
    replaced = False

    def repl(m: re.Match[str]) -> str:
        nonlocal replaced
        if norm(m.group(2)) == old_n and not replaced:
            replaced = True
            return f"[{m.group(1)}]({new_src['url']})"
        return m.group(0)

    new_text = LINK_RE.sub(repl, text)
    if replaced:
        path.write_text(new_text, encoding="utf-8")
    return replaced


def try_fix_pair(
    a: str,
    b: str,
    articles: dict[str, set[str]],
    usage: Counter[str],
) -> bool:
    shared = sorted(articles[a] & articles[b], key=lambda u: (-usage[u], u))
    if not shared:
        return False
    viol_counts = Counter()
    for rate, x, y in violations(articles):
        viol_counts[x] += 1
        viol_counts[y] += 1
    target = a if viol_counts[a] >= viol_counts[b] else b
    partner = b if target == a else a
    path = article_path(target)
    if not path:
        return False
    forbidden = articles[partner]
    pool = _hdr.HIGH_DR_SOURCES
    for old in shared:
        candidates = []
        for src in pool:
            u = norm(src["url"])
            if u in forbidden or u in articles[target] or "infinisynapse" in u:
                continue
            candidates.append((usage[u], u, src))
        candidates.sort(key=lambda x: (x[0], x[1]))
        for _, _, src in candidates:
            before = len(violations(articles))
            original = path.read_text(encoding="utf-8")
            if not swap_url(path, old, src):
                continue
            after = len(violations(collect_articles()))
            if after < before:
                print(f"  {target}: {old} -> {src['url']}  ({before}->{after})")
                return True
            path.write_text(original, encoding="utf-8")
            articles = collect_articles()
    return False


def main() -> int:
    max_rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    for round_i in range(1, max_rounds + 1):
        articles = collect_articles()
        viols = violations(articles)
        if not viols:
            print(f"Done in {round_i - 1} rounds — 0 violations.")
            return 0
        usage = global_usage(articles)
        rate, a, b = viols[0]
        print(f"Round {round_i}: {len(viols)} violations, worst {rate:.0%} {a} vs {b}")
        if not try_fix_pair(a, b, articles, usage):
            print("  No improving swap found.")
            break
    articles = collect_articles()
    remaining = violations(articles)
    print(f"\nRemaining: {len(remaining)}")
    for rate, a, b in remaining[:20]:
        print(f"  {rate:.0%}\t{a} vs {b}")
    return 1 if remaining else 0


if __name__ == "__main__":
    raise SystemExit(main())
