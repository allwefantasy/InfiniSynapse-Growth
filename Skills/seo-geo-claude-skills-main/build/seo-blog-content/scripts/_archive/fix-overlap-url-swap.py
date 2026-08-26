#!/usr/bin/env python3
"""Swap external URLs in-place to minimize pairwise overlap (no paragraph stripping)."""
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


def norm(u: str) -> str:
    return u.rstrip("/").lower()


def extract_urls(text: str) -> list[str]:
    urls = []
    for _, u in re.findall(r"\[([^\]]*)\]\((https?://[^)]+)\)", text):
        if "infinisynapse" not in u:
            urls.append(u)
    return urls


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


def apply_urls(text: str, urls: list[str]) -> str:
    ext_links = [(m.group(1), m.group(2)) for m in re.finditer(r"\[([^\]]*)\]\((https?://[^)]+)\)", text) if "infinisynapse" not in m.group(2)]
    if not ext_links:
        return text
    for i, (label, old) in enumerate(ext_links):
        new = urls[i % len(urls)]
        text = text.replace(f"[{label}]({old})", f"[{label}]({new})", 1)
    return text


def main() -> None:
    pool = [norm(s["url"]) for s in _hdr.HIGH_DR_SOURCES if "cortex-analyst" not in s.get("url", "")]
    paths: dict[str, Path] = {}
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            paths[art.parent.name] = art

    articles = list(paths.keys())
    best_assign: dict[str, set[str]] = {}
    best_v = 10**9
    rng = random.Random(7)
    for trial in range(20000):
        assign: dict[str, set[str]] = {}
        shuffled = pool[:]
        rng.shuffle(shuffled)
        idx = 0
        for name in articles:
            text = paths[name].read_text(encoding="utf-8")
            n = max(5, len(extract_urls(text)))
            group = set()
            while len(group) < n:
                group.add(shuffled[idx % len(shuffled)])
                idx += 1
            assign[name] = group
        v = violation_count(assign)
        if v < best_v:
            best_v = v
            best_assign = {k: set(v) for k, v in assign.items()}
        if best_v == 0:
            break
    print(f"Best violations: {best_v}")
    for name, urlset in best_assign.items():
        text = paths[name].read_text(encoding="utf-8")
        urls = list(urlset)
        rng.shuffle(urls)
        paths[name].write_text(apply_urls(text, urls), encoding="utf-8")


if __name__ == "__main__":
    main()
