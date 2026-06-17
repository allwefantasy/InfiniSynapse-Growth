#!/usr/bin/env python3
"""Restore **Target keyword** metadata stripped by aggressive line cleanup."""
from __future__ import annotations

import json
import re
from pathlib import Path

BLOG = Path(__file__).parent
PLAN = BLOG.parent / "100页主题集群规划-v1-替换后主关键词版.md"
MANIFEST = BLOG / "pillar-manifests" / "pillar4-8-articles.json"

PILLAR_DIRS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]


def parse_plan_keywords(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    blocks = re.split(r"(?=^### \d{3}\.)", text, flags=re.M)
    for block in blocks:
        m_id = re.match(r"^### (\d{3})\.", block)
        if not m_id:
            continue
        art_id = m_id.group(1)
        m_kw = re.search(r"^\| ([^|]+) \|", block, re.M)
        if not m_kw:
            continue
        kw = m_kw.group(1).strip()
        if kw in {"关键词", ":---"}:
            # skip header row; take first data row after header
            rows = re.findall(r"^\| ([^|]+) \|", block, re.M)
            data = [r.strip() for r in rows if r.strip() not in {"关键词", ":---"}]
            if data:
                kw = data[0]
        out[art_id] = kw
    return out


def parse_manifest_keywords(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for pillar in data["pillars"]:
        for art in pillar["articles"]:
            out[art["id"]] = art["keyword"]
    return out


def restore_article(path: Path, keyword: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if re.search(r"\*\*Target keyword\*\*:", text):
        return False
    m = re.search(r"(\*\*Slug\*\*:[^\n]+\n\n)", text)
    if not m:
        return False
    insert = f"{m.group(1)}**Target keyword**: `{keyword}`\n"
    new_text = text[: m.start()] + insert + text[m.end() :]
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    kws = parse_plan_keywords(PLAN)
    kws.update(parse_manifest_keywords(MANIFEST))
    changed = 0
    for pillar in PILLAR_DIRS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            art_id = art.parent.name[:3]
            kw = kws.get(art_id)
            if not kw:
                print(f"MISSING keyword map: {art.parent.name}")
                continue
            if restore_article(art, kw):
                changed += 1
                print(f"restored: {art.parent.name} -> {kw}")
    print(f"\nRestored {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
