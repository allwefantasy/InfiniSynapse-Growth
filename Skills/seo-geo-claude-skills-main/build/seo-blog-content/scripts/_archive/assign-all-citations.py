#!/usr/bin/env python3
"""Assign external URL sets to all pillar10/11 articles minimizing pairwise overlap."""
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

PILLARS = [ROOT / "SEO/Blog/pillar10-mcp-data-access", ROOT / "SEO/Blog/pillar11-agentic-analytics"]
CLUSTER_ONLY = {
    "130-effective-context-engineering-for-ai-agents",
    "131-data-access",
    "132-data-accessibility",
    "133-data-accessing",
    "134-data-access-management",
    "135-access-management",
    "137-agent-analytics-official",
    "138-analytics-agent",
    "139-proactive-insight-generation-anomaly-detection",
    "142-ai-agents-for-analytics",
    "143-agent-analytics",
}
MAX_OVERLAP = 0.30
PER = 7


def norm(u: str) -> str:
    return u.rstrip("/").lower()


def overlap_rate(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def violation_count(assign: dict[str, set[str]]) -> int:
    n = 0
    keys = list(assign.keys())
    for i, j in combinations(keys, 2):
        if overlap_rate(assign[i], assign[j]) > MAX_OVERLAP:
            n += 1
    return n


def replace_urls(path: Path, urls: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    idx = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal idx
        if "infinisynapse" in m.group(2):
            return m.group(0)
        new_u = urls[idx % len(urls)]
        idx += 1
        return f"[{m.group(1)}]({new_u})"

    new_text = re.sub(r"\[([^\]]*)\]\((https?://[^)]+)\)", repl, text)
    path.write_text(new_text, encoding="utf-8")


def collect_forbidden_urls() -> set[str]:
    forbidden: set[str] = set()
    for pillar in PILLARS:
        for art in pillar.glob("[0-9][0-9][0-9]-*/article.md"):
            if art.parent.name in CLUSTER_ONLY:
                continue
            for m in re.finditer(r"\[([^\]]*)\]\((https?://[^)]+)\)", art.read_text(encoding="utf-8")):
                if "infinisynapse" not in m.group(2):
                    forbidden.add(norm(m.group(2)))
    return forbidden


def main() -> None:
    pool = [norm(s["url"]) for s in _hdr.HIGH_DR_SOURCES if "cortex-analyst" not in s.get("url", "")]
    forbidden = collect_forbidden_urls()
    pool = [u for u in pool if u not in forbidden]
    paths: dict[str, Path] = {}
    counts: dict[str, int] = {}
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            name = art.parent.name
            if name not in CLUSTER_ONLY:
                continue
            paths[name] = art
            n = len(
                [
                    m.group(2)
                    for m in re.finditer(r"\[([^\]]*)\]\((https?://[^)]+)\)", art.read_text(encoding="utf-8"))
                    if "infinisynapse" not in m.group(2)
                ]
            )
            counts[name] = PER

    articles = list(paths.keys())
    best: dict[str, set[str]] = {}
    best_v = 10**9
    rng = random.Random(99)
    for _ in range(150000):
        assign: dict[str, set[str]] = {}
        shuffled = pool[:]
        rng.shuffle(shuffled)
        idx = 0
        for name in articles:
            k = counts[name]
            g: set[str] = set()
            while len(g) < k:
                g.add(shuffled[idx % len(shuffled)])
                idx += 1
            assign[name] = g
        v = violation_count(assign)
        if v < best_v:
            best_v = v
            best = {k: set(v) for k, v in assign.items()}
        if best_v == 0:
            break
    print(f"Best violations: {best_v}")
    for name, urlset in best.items():
        urls = list(urlset)
        rng.shuffle(urls)
        replace_urls(paths[name], urls)
        print(f"  {name}: {len(urlset)} urls")


if __name__ == "__main__":
    main()
