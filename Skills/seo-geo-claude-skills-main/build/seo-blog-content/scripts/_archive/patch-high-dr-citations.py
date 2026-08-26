#!/usr/bin/env python3
"""Patch articles to >=5 unique high-DR authority citations woven into narrative prose."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

BLOG = Path(__file__).parent

_hdr_spec = importlib.util.spec_from_file_location("hdr", BLOG / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_hdr_spec)
assert _hdr_spec and _hdr_spec.loader
_hdr_spec.loader.exec_module(_hdr)

HIGH_DR_SOURCES = _hdr.HIGH_DR_SOURCES
MIN_HIGH_DR_CITATIONS = _hdr.MIN_HIGH_DR_CITATIONS
PILLAR_EXTRA_IDS = _hdr.PILLAR_EXTRA_IDS
source_by_id = _hdr.source_by_id
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

_spec = importlib.util.spec_from_file_location("weave", BLOG / "weave-external-citations.py")
_weave = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_weave)

SKIP_SECTIONS = _weave.SKIP_SECTIONS


def fix_corrupt_hr_rules(text: str) -> str:
    """Remove accidental `--- ` prefix before woven citation sentences."""
    for src in HIGH_DR_SOURCES:
        frag = src["weave"].format(url=src["url"]).split("[", 1)[0].strip()[:30]
        if not frag:
            continue
        text = re.sub(rf"^---\s+({re.escape(frag)}.+)$", r"\1", text, flags=re.M)
    return text


def present_urls(text: str) -> set[str]:
    return {
        u
        for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", text)
        if "infinisynapse" not in u.lower()
    }


def high_dr_count(urls: set[str]) -> int:
    hosts = set()
    for url in urls:
        h = _weave.host_key(url)
        for src in HIGH_DR_SOURCES:
            if _weave.host_key(src["url"]) == h or h in src["url"]:
                hosts.add(src["id"])
                break
    return len(hosts)


def pick_missing(pillar_name: str, present: set[str], need: int) -> list[dict]:
    order = PILLAR_EXTRA_IDS.get(pillar_name, [])
    # Base trio always eligible if missing
    for sid in ["stanford-hai", "ibm-augmented", "nist-ai-rmf", "ms-data-arch"]:
        if sid not in order:
            order.append(sid)
    picks: list[dict] = []
    for sid in order:
        src = source_by_id(sid)
        if src["url"] in present:
            continue
        if any(_weave.host_key(src["url"]) == _weave.host_key(u) for u in present):
            continue
        picks.append(src)
        present.add(src["url"])
        if len(picks) >= need:
            break
    # Fallback: any remaining approved source
    if len(picks) < need:
        for src in HIGH_DR_SOURCES:
            if src["url"] in present:
                continue
            if src in picks:
                continue
            picks.append(src)
            present.add(src["url"])
            if len(picks) >= need:
                break
    return picks


def weave_source(text: str, src: dict) -> str:
    sentence = src["weave"].format(url=src["url"])
    if sentence in text:
        return text
    # Reuse weave machinery with custom template
    old = dict(_weave.WEAVE)
    key = _weave.host_key(src["url"])
    _weave.WEAVE[key] = src["weave"]
    try:
        return _weave.weave_into_section(text, src["url"], src["label"])
    finally:
        _weave.WEAVE.clear()
        _weave.WEAVE.update(old)


def section_spans(text: str) -> list[tuple[str, int, int]]:
    headers = list(re.finditer(r"^## ([^\n]+)$", text, re.M))
    spans: list[tuple[str, int, int]] = []
    for i, h in enumerate(headers):
        title = h.group(1).strip()
        if SKIP_SECTIONS.search(title):
            continue
        start = h.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        spans.append((title, start, end))
    return spans


def score_section(title: str, hints: list[str]) -> int:
    tl = title.lower()
    return sum(2 for h in hints if re.search(h, tl))


def weave_with_hints(text: str, src: dict) -> str:
    sentence = src["weave"].format(url=src["url"])
    if sentence in text or src["url"] in _weave.narrative_text(text):
        return text
    spans = section_spans(text)
    ranked = sorted(spans, key=lambda s: score_section(s[0], src["hints"]), reverse=True)
    for title, start, end in ranked:
        if score_section(title, src["hints"]) == 0 and ranked.index((title, start, end)) > 2:
            break
        section = text[start:end]
        pe = _weave.first_paragraph_end(section)
        if pe is None:
            continue
        insert_at = start + pe
        before = text[max(0, insert_at - 500) : insert_at]
        if src["url"] in before:
            return text
        prefix = text[:insert_at].rstrip()
        if prefix.endswith(":"):
            prefix = prefix[:-1] + "."
        if not prefix.endswith((".", "!", "?")):
            prefix += "."
        return prefix + " " + sentence + "\n\n" + text[insert_at:].lstrip()
    return weave_source(text, src)


def patch_article(path: Path, pillar_name: str) -> bool:
    original = path.read_text(encoding="utf-8")
    text = fix_corrupt_hr_rules(original)
    urls = present_urls(text)
    have = high_dr_count(urls)
    need = max(0, MIN_HIGH_DR_CITATIONS - have)
    if need:
        for src in pick_missing(pillar_name, set(urls), need):
            text = weave_with_hints(text, src)
            urls = present_urls(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if patch_article(art, pillar.name):
                changed += 1
                print(f"patched: {art.parent.name}")
    print(f"\nPatched {changed} articles")


if __name__ == "__main__":
    main()
