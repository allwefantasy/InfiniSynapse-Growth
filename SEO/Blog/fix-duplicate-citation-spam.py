#!/usr/bin/env python3
"""Remove duplicate weave sentences and diversify repeated external URLs in one article."""
from __future__ import annotations

import importlib.util
import re
import sys
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

_hdr_spec = importlib.util.spec_from_file_location("hdr", BLOG / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_hdr_spec)
assert _hdr_spec and _hdr_spec.loader
_hdr_spec.loader.exec_module(_hdr)

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def urls_in(text: str) -> set[str]:
    return {u for _, u in LINK_RE.findall(text)}


def alt_url(current: str, used: set[str]) -> str | None:
    for src in _hdr.HIGH_DR_SOURCES:
        u = src["url"]
        if u == current or u in used or "infinisynapse" in urlparse(u).netloc:
            continue
        return u
    return None


def dedupe_sentences(text: str) -> str:
    """Drop exact duplicate sentences (>40 chars) after first occurrence."""
    lines = text.splitlines()
    seen: set[str] = set()
    out: list[str] = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code or line.startswith("#") or line.startswith("|") or line.startswith("!["):
            out.append(line)
            continue
        parts = SENT_SPLIT.split(line)
        kept: list[str] = []
        for s in parts:
            key = re.sub(r"\s+", " ", s.strip()).lower()
            if len(key) > 40 and key in seen:
                continue
            if len(key) > 40:
                seen.add(key)
            kept.append(s)
        out.append(" ".join(kept) if kept else line)
    return "\n".join(out)


def diversify_hot_urls(text: str, max_per_url: int = 2) -> str:
    """Replace excess links to the same external URL with pool alternatives."""
    counts: dict[str, int] = {}
    used = urls_in(text)

    def repl(m: re.Match[str]) -> str:
        label, url = m.group(1), m.group(2)
        if "infinisynapse" in urlparse(url).netloc.lower():
            return m.group(0)
        counts[url] = counts.get(url, 0) + 1
        if counts[url] <= max_per_url:
            return m.group(0)
        new_u = alt_url(url, used)
        if not new_u:
            return m.group(0)
        used.add(new_u)
        for src in _hdr.HIGH_DR_SOURCES:
            if src["url"] == new_u:
                return f"[{src['label']}]({new_u})"
        return f"[{label}]({new_u})"

    return LINK_RE.sub(repl, text)


def fix(text: str) -> str:
    return dedupe_sentences(text)


def main() -> int:
    targets: list[Path] = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            p = Path(arg)
            if p.is_dir():
                targets.extend(sorted(p.glob("[0-9][0-9][0-9]-*/article.md")))
            elif p.is_file():
                targets.append(p)
    else:
        for pillar in PILLARS:
            targets.extend(sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")))

    changed = 0
    for art in targets:
        original = art.read_text(encoding="utf-8")
        new = fix(original)
        if new != original:
            art.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  {art.parent.name}")
    print(f"\nUpdated {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
