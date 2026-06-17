#!/usr/bin/env python3
"""Move tail-only external citations into middle narrative sections."""
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
    BLOG / "pillar2-data-agent-vs-alternatives",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

SKIP = re.compile(r"related reading|conclusion|production debugging|operational readiness", re.I)


def is_external(url: str) -> bool:
    return "infinisynapse" not in urlparse(url).netloc.lower()


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def source_for_url(url: str) -> dict | None:
    h = urlparse(url).netloc.lower()
    for src in _hdr.HIGH_DR_SOURCES:
        if urlparse(src["url"]).netloc.lower() in h:
            return src
    return None


def tail_only_urls(text: str) -> list[str]:
    body = body_from_tldr(text)
    lines = body.splitlines()
    total = len(lines)
    tail_start = int(total * 0.85)
    tail_urls: set[str] = set()
    head_urls: set[str] = set()
    offset = text.find(body)
    for i, line in enumerate(lines, 1):
        for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", line):
            if not is_external(u):
                continue
            if i >= tail_start:
                tail_urls.add(u)
            else:
                head_urls.add(u)
    return list(tail_urls - head_urls)


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


def weave_mid(text: str, src: dict) -> str:
    body = body_from_tldr(text)
    spans = section_spans(body)
    if len(spans) < 2:
        return text
    mid = spans[len(spans) // 2]
    tldr_off = text.find(body)
    start, end = tldr_off + mid[1], tldr_off + mid[2]
    section = text[start:end]
    pe = _weave.first_paragraph_end(section)
    if pe is None:
        return text
    insert_at = start + pe
    sentence = src["weave"].format(url=src["url"])
    if sentence in text:
        return text
    prefix = text[:insert_at].rstrip()
    last = prefix.splitlines()[-1] if prefix else ""
    if last.strip().startswith("|") or last.strip() == "---":
        return text
    if prefix.endswith(":"):
        prefix = prefix[:-1] + "."
    if not prefix.endswith((".", "!", "?")):
        prefix += "."
    return prefix + " " + sentence + "\n\n" + text[insert_at:].lstrip()


def strip_tail_sentence(text: str, url: str) -> str:
    """Remove one narrative sentence containing url from Production Debugging section."""
    m = re.search(r"(## Production Debugging Notes\n.*?)(?=\n## |\Z)", text, re.S)
    if not m:
        return text
    block = m.group(1)
    lines = block.splitlines()
    new_lines = []
    removed = False
    for line in lines:
        if not removed and url in line and len(line) > 80:
            # keep line without the citation sentence fragment if duplicated
            cleaned = re.sub(
                r"\s*(That practice aligns with|The \[Stanford HAI AI Index\]|Dialect quirks matter\. Teams).*",
                "",
                line,
            )
            if url not in cleaned:
                if cleaned.strip():
                    new_lines.append(cleaned)
                removed = True
                continue
        new_lines.append(line)
    if not removed:
        return text
    return text[: m.start()] + "\n".join(new_lines) + text[m.end() :]


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    urls = tail_only_urls(text)
    if not urls:
        return False
    new_text = text
    for url in urls[:2]:
        src = source_for_url(url)
        if not src:
            continue
        updated = weave_mid(new_text, src)
        if updated != new_text:
            new_text = updated
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if process(art):
                n += 1
                print(f"fixed: {art.parent.name}")
    print(f"\nFixed {n} articles")


if __name__ == "__main__":
    main()
