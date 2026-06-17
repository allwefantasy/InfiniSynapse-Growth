#!/usr/bin/env python3
"""Ensure >=5 unique external inline links in article body (TL;DR onward)."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

BLOG = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("acq", BLOG / "audit-content-quality.py")
_mod = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_mod)

PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

CITATIONS = [
    ("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework"),
    ("Stanford HAI AI Index", "https://hai.stanford.edu/ai-index"),
    ("IBM augmented analytics overview", "https://www.ibm.com/topics/augmented-analytics"),
]


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    body = _mod.body_from_tldr(text)
    present = {
        u
        for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", body)
        if "infinisynapse" not in u.lower()
    }
    if len(present) >= 5:
        return False
    missing = [(l, u) for l, u in CITATIONS if u not in present]
    if not missing:
        return False
    label, url = missing[0]
    sentence = (
        f"Governance expectations for production analytics align with the "
        f"[{label}]({url}), which we reference when designing reviewer checkpoints."
    )
    m = re.search(r"(## TL;DR\n\n.*?)(\n\n## )", text, re.S)
    if not m:
        return False
    insert_at = m.end(1)
    if sentence in text:
        return False
    new_text = text[:insert_at] + "\n\n" + sentence + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if patch(art):
                changed += 1
                print(f"patched: {art.parent.name}")
    print(f"Patched {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
