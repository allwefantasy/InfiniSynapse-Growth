#!/usr/bin/env python3
"""Audit keyword stuffing in H1 / Meta Description (title + description only)."""
from __future__ import annotations

import re
import sys
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

INFINI_FOR_KW = re.compile(
    r"Connect .+ to InfiniSynapse for .+ with setup checklist",
    re.I,
)
GUIDE_TO_KW = re.compile(
    r"^(Practical|Implementation) guide to .+ with pain points",
    re.I,
)
TITLE_MAX = 90


def extract_keyword(text: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).strip().lower() if m else ""


def extract_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_desc(text: str) -> str:
    m = re.search(r"\*\*Meta Description\*\*:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def prefix_overlap(h1: str, desc: str, kw: str) -> bool:
    if not h1 or not desc or not kw:
        return False
    kwt = kw.title()
    h = h1.split(":")[0].strip().lower()
    d = desc.split(":")[0].strip().lower()
    if len(h) < 12:
        return False
    return h == d or (h.startswith(kw) and d.startswith(kw) and h[:40] == d[:40])


def audit_article(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    kw = extract_keyword(text)
    if not kw:
        return ["missing Target keyword"]
    h1 = extract_h1(text)
    desc = extract_desc(text)
    fails: list[str] = []

    if kw not in h1.lower():
        fails.append("H1 missing keyword")
    if kw not in desc.lower():
        fails.append("description missing keyword")
    if h1.lower().count(kw) >= 2:
        fails.append("keyword repeated in H1")
    if desc.lower().count(kw) >= 2:
        fails.append("keyword repeated in description")
    if INFINI_FOR_KW.search(desc):
        fails.append("InfiniSynapse-for-keyword template in description")
    if GUIDE_TO_KW.search(desc):
        fails.append("guide-to-keyword template in description")
    if prefix_overlap(h1, desc, kw):
        fails.append("H1/description duplicate prefix")
    if len(h1) > TITLE_MAX:
        fails.append(f"H1 too long ({len(h1)} chars)")
    if re.search(r" for " + re.escape(kw) + r" with setup checklist", desc, re.I):
        fails.append("for-keyword-setup template in description")

    return fails


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    total = fail_n = 0
    for pillar in targets:
        if not pillar.is_dir():
            continue
        print(f"\n{pillar.name}")
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            fails = audit_article(art)
            total += 1
            ok = not fails
            if not ok:
                fail_n += 1
            print(f"  {art.parent.name:<45} {'✓' if ok else '✗'}")
            for f in fails:
                print(f"      · {f}")
    print(f"\nTotal: {total} | Pass: {total - fail_n} | Fail: {fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
