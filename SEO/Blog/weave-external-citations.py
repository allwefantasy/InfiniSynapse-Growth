#!/usr/bin/env python3
"""Weave external authority links from TL;DR eval blocks into narrative section prose."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

BLOG = Path(__file__).parent
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

SKIP_SECTIONS = re.compile(
    r"table of contents|related reading|conclusion|faq|frequently asked",
    re.I,
)

HOST_SECTION_HINTS: dict[str, list[str]] = {
    "nist.gov": [r"governance", r"security", r"quality", r"compliance", r"risk", r"trust"],
    "hai.stanford.edu": [r"why", r"matters", r"adoption", r"enterprise", r"trend", r"landscape"],
    "ibm.com": [r"evaluat", r"method", r"operational", r"workflow", r"definition", r"scorecard"],
    "learn.microsoft.com": [r"architect", r"connect", r"infrastructure", r"platform", r"deploy"],
}

WEAVE: dict[str, str] = {
    "nist.gov": (
        "Production rollouts should align access and review controls with the "
        "[NIST AI Risk Management Framework]({url}), especially when recurring queries touch live schemas."
    ),
    "hai.stanford.edu": (
        "Adoption benchmarks in the [Stanford HAI AI Index]({url}) track the same shift from pilot "
        "demos to governed analytics loops we see in customer rollouts."
    ),
    "ibm.com": (
        "The move from dashboard-first BI to augmented workflows—described in "
        "[IBM's augmented analytics overview]({url})—frames how teams should evaluate tooling here."
    ),
    "learn.microsoft.com": (
        "Multi-source connector design should follow [Microsoft's data architecture guidance]({url}) "
        "so domain boundaries and metric contracts stay explicit as scope grows."
    ),
}


def is_external(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return bool(host) and "infinisynapse" not in host


def host_key(url: str) -> str:
    host = urlparse(url).netloc.lower()
    for key in WEAVE:
        if key in host:
            return key
    return host


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def external_urls_in(text: str) -> set[str]:
    return {u for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", text) if is_external(u)}


def eval_only_urls(text: str) -> list[tuple[str, str]]:
    body = body_from_tldr(text)
    narrative = "\n".join(
        ln
        for ln in body.splitlines()
        if not ln.strip().startswith("> **Evaluation basis**")
    )
    in_narr = external_urls_in(narrative)
    eval_lines = [ln for ln in body.splitlines() if ln.strip().startswith("> **Evaluation")]
    eval_text = "\n".join(eval_lines)
    out: list[tuple[str, str]] = []
    for anchor, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", eval_text):
        if is_external(url) and url not in in_narr:
            out.append((anchor, url))
    return out


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


def pick_section(title: str, url: str) -> int:
    key = host_key(url)
    hints = HOST_SECTION_HINTS.get(key, [])
    score = 0
    tl = title.lower()
    for h in hints:
        if re.search(h, tl):
            score += 2
    return score


def first_paragraph_end(section_text: str) -> int | None:
    lines = section_text.splitlines()
    para: list[str] = []
    offset = 0
    for line in lines:
        if not line.strip():
            if para:
                return offset
            offset += len(line) + 1
            continue
        if line.strip().startswith("#") or line.strip().startswith("|") or line.strip().startswith("!["):
            offset += len(line) + 1
            continue
        if line.strip().startswith(">"):
            offset += len(line) + 1
            continue
        para.append(line)
        offset += len(line) + 1
    if para:
        return offset
    return None


def narrative_text(text: str) -> str:
    body = body_from_tldr(text)
    return "\n".join(
        ln
        for ln in body.splitlines()
        if not ln.strip().startswith("> **Evaluation basis**")
    )


def weave_into_section(text: str, url: str, anchor: str) -> str:
    key = host_key(url)
    template = WEAVE.get(key)
    if not template:
        template = (
            f"Industry context from [{anchor}]({{url}}) reinforces the governance and repeatability "
            "expectations outlined in this guide."
        )
    sentence = template.format(url=url)
    if sentence in text or url in narrative_text(text):
        return text

    spans = section_spans(text)
    if not spans:
        return text

    ranked = sorted(spans, key=lambda s: pick_section(s[0], url), reverse=True)
    for title, start, end in ranked:
        if pick_section(title, url) == 0 and ranked.index((title, start, end)) > 0:
            break
        section = text[start:end]
        pe = first_paragraph_end(section)
        if pe is None:
            continue
        insert_at = start + pe
        # Avoid double-insert in same paragraph
        before = text[max(0, insert_at - 400) : insert_at]
        if url in before:
            return text
        prefix = text[:insert_at].rstrip()
        if prefix.endswith(":"):
            prefix = prefix[:-1] + "."
        if not prefix.endswith((".", "!", "?")):
            prefix += "."
        return prefix + " " + sentence + "\n\n" + text[insert_at:].lstrip()

    # Fallback: after TL;DR eval block
    m = re.search(r"(> \*\*Evaluation basis\*\*[^\n]*\n\n)", text)
    if m and url not in text[m.end() : m.end() + 800]:
        return text[: m.end()] + sentence + "\n\n" + text[m.end() :]
    return text


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for anchor, url in eval_only_urls(text):
        text = weave_into_section(text, url, anchor)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if process(art):
                changed += 1
                print(f"woven: {art.parent.name}")
    print(f"\nWoven citations into {changed} articles")


if __name__ == "__main__":
    main()
