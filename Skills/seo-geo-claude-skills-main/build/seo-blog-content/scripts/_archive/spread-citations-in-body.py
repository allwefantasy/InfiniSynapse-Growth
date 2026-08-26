#!/usr/bin/env python3
"""Ensure external citations appear in early + middle body, not only TL;DR tail."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from urllib.parse import urlparse

BLOG = Path(__file__).parent
_hdr_spec = importlib.util.spec_from_file_location("hdr", BLOG / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_hdr_spec)
assert _hdr_spec and _hdr_spec.loader
_hdr_spec.loader.exec_module(_hdr)

_weave_spec = importlib.util.spec_from_file_location("weave", BLOG / "weave-external-citations.py")
_weave = importlib.util.module_from_spec(_weave_spec)
assert _weave_spec and _weave_spec.loader
_weave_spec.loader.exec_module(_weave)

PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

SKIP = re.compile(r"related reading|conclusion|faq|frequently asked|table of contents", re.I)


def is_external(url: str) -> bool:
    return "infinisynapse" not in urlparse(url).netloc.lower()


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def section_spans(text: str) -> list[tuple[str, int, int]]:
    headers = list(re.finditer(r"^## ([^\n]+)$", text, re.M))
    spans = []
    for i, h in enumerate(headers):
        title = h.group(1).strip()
        if SKIP.search(title):
            continue
        start = h.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        spans.append((title, start, end))
    return spans


def urls_in_range(text: str, start: int, end: int) -> set[str]:
    chunk = text[start:end]
    return {u for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", chunk) if is_external(u)}


def pick_source_for_pillar(pillar_name: str, present_hosts: set[str]) -> dict | None:
    order = _hdr.PILLAR_EXTRA_IDS.get(pillar_name, [])
    for sid in order + [s["id"] for s in _hdr.HIGH_DR_SOURCES]:
        src = _hdr.source_by_id(sid) if sid in {s["id"] for s in _hdr.HIGH_DR_SOURCES} else None
        if src is None:
            try:
                src = _hdr.source_by_id(sid)
            except KeyError:
                continue
        host = urlparse(src["url"]).netloc.lower()
        if host in present_hosts or src["url"] in present_hosts:
            continue
        return src
    return None


def weave_into_span(text: str, start: int, end: int, src: dict) -> str:
    section = text[start:end]
    pe = _weave.first_paragraph_end(section)
    if pe is None:
        return text
    # Do not glue citations onto horizontal rules or table rows
    insert_line_start = section[:pe].rstrip().splitlines()[-1] if section[:pe].strip() else ""
    if insert_line_start.strip() in ("---", "") or insert_line_start.strip().startswith("|"):
        return text
    insert_at = start + pe
    sentence = src["weave"].format(url=src["url"])
    if sentence in text or src["url"] in text[start:end]:
        return text
    prefix = text[:insert_at].rstrip()
    if prefix.endswith(":"):
        prefix = prefix[:-1] + "."
    if not prefix.endswith((".", "!", "?")):
        prefix += "."
    return prefix + " " + sentence + "\n\n" + text[insert_at:].lstrip()


def needs_spread(text: str) -> tuple[bool, int, int]:
    body = body_from_tldr(text)
    spans = section_spans(body)
    if len(spans) < 3:
        return False, 0, 0
    n = len(spans)
    early_end = spans[n // 3][2]
    mid_end = spans[(2 * n) // 3][2]
    early = urls_in_range(body, 0, early_end)
    mid = urls_in_range(body, early_end, mid_end) - early
    return len(early) < 2 or len(mid) < 1, len(early), len(mid)


def process(path: Path, pillar_name: str) -> bool:
    text = path.read_text(encoding="utf-8")
    flag, _, _ = needs_spread(text)
    if not flag:
        return False
    body = body_from_tldr(text)
    spans = section_spans(body)
    n = len(spans)
    tldr_offset = text.find(body)
    early_idx = n // 4
    mid_idx = n // 2
    present = {urlparse(u).netloc.lower() for u in urls_in_range(body, 0, len(body))}

    new_text = text
    for idx in (early_idx, mid_idx):
        src = pick_source_for_pillar(pillar_name, present)
        if not src:
            break
        title, start, end = spans[idx]
        abs_start = tldr_offset + start
        abs_end = tldr_offset + end
        updated = weave_into_span(new_text, abs_start, abs_end, src)
        if updated != new_text:
            present.add(urlparse(src["url"]).netloc.lower())
            new_text = updated

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if process(art, pillar.name):
                n += 1
                print(f"spread: {art.parent.name}")
    print(f"\nSpread citations in {n} articles")


if __name__ == "__main__":
    main()
