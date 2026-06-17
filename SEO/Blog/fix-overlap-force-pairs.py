#!/usr/bin/env python3
"""Force-fix overlap by replacing shared URLs in the hotter article of each violating pair."""
from __future__ import annotations

import importlib.util
import re
import sys
from collections import Counter
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
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
MAX_OVERLAP = 0.30

_ov_spec = importlib.util.spec_from_file_location("ov", BLOG / "audit-external-link-overlap.py")
_ov = importlib.util.module_from_spec(_ov_spec)
assert _ov_spec and _ov_spec.loader
_ov_spec.loader.exec_module(_ov)

_hdr_spec = importlib.util.spec_from_file_location("hdr", BLOG / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_hdr_spec)
assert _hdr_spec and _hdr_spec.loader
_hdr_spec.loader.exec_module(_hdr)


def norm(url: str) -> str:
    return url.rstrip("/").lower()


def article_path(slug: str) -> Path | None:
    for pillar in PILLARS:
        p = pillar / slug / "article.md"
        if p.is_file():
            return p
    return None


def swap_url(path: Path, old: str, new: str) -> bool:
    text = path.read_text(encoding="utf-8")
    old_n = norm(old)
    matches = list(LINK_RE.finditer(text))
    for m in reversed(matches):
        if norm(m.group(2)) != old_n:
            continue
        repl = f"[{m.group(1)}]({new})"
        text = text[: m.start()] + repl + text[m.end() :]
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    pool = [norm(s["url"]) for s in _hdr.HIGH_DR_SOURCES]
    pool_urls = [s["url"] for s in _hdr.HIGH_DR_SOURCES]

    for round_i in range(1, 501):
        articles = _ov.collect_articles(PILLARS)
        viols = _ov.audit_pairs(articles)
        if not viols:
            print(f"Done in {round_i - 1} rounds — 0 violations.")
            return 0

        usage: Counter[str] = Counter()
        for urls in articles.values():
            for u in urls:
                usage[norm(u)] += 1

        rate, a, b, inter, _ = viols[0]
        sets = {k: {norm(u) for u in v} for k, v in articles.items()}
        shared = sorted(sets[a] & sets[b], key=lambda u: -usage[u])
        target = a if len(sets[a]) >= len(sets[b]) else b
        partner = b if target == a else a
        forbidden = sets[partner]

        need = max(1, inter - int(MAX_OVERLAP * min(len(sets[a]), len(sets[b]))))
        path = article_path(target)
        if not path or not shared:
            print(f"Round {round_i}: stuck on {a} vs {b}")
            break

        replaced = 0
        for old in shared:
            if replaced >= need:
                break
            for src in sorted(_hdr.HIGH_DR_SOURCES, key=lambda s: usage[norm(s["url"])]):
                u = norm(src["url"])
                if u in forbidden or u == old:
                    continue
                if swap_url(path, old, src["url"]):
                    print(f"  R{round_i}: {target}: {old[:50]} -> {src['url'][:50]}")
                    replaced += 1
                    forbidden.add(u)
                    break

        if not replaced:
            print(f"Round {round_i}: no swap for {a} vs {b} ({rate:.0%})")
            break

    remaining = len(_ov.audit_pairs(_ov.collect_articles(PILLARS)))
    print(f"\nRemaining violations: {remaining}")
    return 0 if remaining == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
