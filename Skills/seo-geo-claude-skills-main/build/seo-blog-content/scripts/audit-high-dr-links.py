#!/usr/bin/env python3
"""Audit: >=5 unique high-DR authority citations, embedded in narrative prose."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
_spec = importlib.util.spec_from_file_location("hdr", Path(__file__).parent / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)

_spec2 = importlib.util.spec_from_file_location("inline", Path(__file__).parent / "audit-inline-external-links.py")
_inline = importlib.util.module_from_spec(_spec2)
assert _spec2 and _spec2.loader
_spec2.loader.exec_module(_inline)

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


def match_source_id(url: str) -> str | None:
    h = urlparse(url).netloc.lower()
    for src in _hdr.HIGH_DR_SOURCES:
        sh = urlparse(src["url"]).netloc.lower()
        if sh in h or h in sh:
            return src["id"]
    return None


def audit_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fails: list[str] = []
    body = _inline.body_from_tldr(text)
    narrative = "\n".join(
        ln
        for ln in body.splitlines()
        if not ln.strip().startswith("> **Evaluation basis**")
    )

    ids: set[str] = set()
    for _, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", narrative):
        if "infinisynapse" in urlparse(url).netloc.lower():
            continue
        sid = match_source_id(url)
        if sid:
            ids.add(sid)

    if len(ids) < _hdr.MIN_HIGH_DR_CITATIONS:
        fails.append(f"only {len(ids)} high-DR citations in narrative (need >= {_hdr.MIN_HIGH_DR_CITATIONS})")

    inline_fails = _inline.audit_file(path)
    fails.extend(inline_fails)
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
            fails = audit_file(art)
            total += 1
            ok = not fails
            if not ok:
                fail_n += 1
            print(f"  {art.parent.name:<45} {'✓' if ok else '✗'}")
            for f in fails[:4]:
                print(f"      · {f}")
    print(f"\nTotal: {total} | Pass: {total - fail_n} | Fail: {fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
