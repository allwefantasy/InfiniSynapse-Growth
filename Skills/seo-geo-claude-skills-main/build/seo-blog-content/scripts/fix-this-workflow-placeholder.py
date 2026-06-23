#!/usr/bin/env python3
"""Replace generic 'this workflow' placeholders with the article Target keyword."""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
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

GENERIC_WORKFLOW = re.compile(r"\bthis workflow\b", re.I)
GENERIC_CONNECTOR = re.compile(r"\bthis connector workflow\b", re.I)


def extract_keyword(text: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).strip() if m else ""


def extract_h1(text: str) -> str:
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def source_label(h1: str) -> str:
    for pat in (
        r"Connect (\w[\w\s-]+?) to",
        r"Analyze (\w[\w\s-]+?) Data",
        r"for (\w[\w\s-]+?) in",
        r"for (\w[\w\s-]+?) in 2026",
        r"in (\w[\w\s-]+?) \(",
    ):
        m = re.search(pat, h1, re.I)
        if m:
            return m.group(1).strip()
    return ""


def keyword_phrase(kw: str, h1: str, *, bold: bool = True) -> str:
    """Prefer full Target keyword; shorten only when grammatically unwieldy."""
    label = kw
    if len(kw) > 48:
        src = source_label(h1)
        if src:
            label = f"{src.lower()} connector analytics"
        else:
            label = " ".join(kw.split()[:5])
    return f"**{label}**" if bold else label


def fix_faq_headers(text: str, kw: str, h1: str) -> str:
    src = source_label(h1)

    def sub_header(m: re.Match[str]) -> str:
        return m.group(0).replace("??", "?")

    text = re.sub(r"^### .+\?\?.*$", sub_header, text, flags=re.M)

    # FAQ titles stay short; Target keyword belongs in answers and body prose.
    replacements = [
        (r"^### How long does it take to (?:deploy|roll out) .+\?$", "### How long does rollout take?"),
        (r"^### Do we need a dedicated data engineer for .+\?$", "### Do we need a dedicated data engineer?"),
        (r"^### How does InfiniSynapse improve trust for .+\?$", "### How does InfiniSynapse improve trust?"),
        (r"^### What security checks matter before scaling .+\?$", "### What security checks matter before scaling?"),
    ]
    if src:
        replacements.append(
            (
                r"^### Can .+ combine .+ with files and APIs\?$",
                f"### Can {src} combine with files and APIs?",
            )
        )
    else:
        replacements.append(
            (r"^### Can .+ combine .+ with files and APIs\?$", "### Can this connector combine with files and APIs?")
        )
    for pat, repl in replacements:
        text = re.sub(pat, repl, text, flags=re.M | re.I)

    kw_l = kw.lower()
    kw_header_lines = [ln for ln in text.splitlines() if ln.startswith("### ") and kw_l in ln.lower()]
    if len(kw_header_lines) >= 4:
        out: list[str] = []
        for line in text.splitlines():
            if line.startswith("### ") and kw_l in line.lower():
                title = line[4:].strip()
                title = re.sub(re.escape(kw), "analytics", title, flags=re.I)
                title = re.sub(r"\banalytics analytics\b", "analytics", title, flags=re.I)
                title = re.sub(r"\s{2,}", " ", title).strip()
                out.append("### " + title)
            else:
                out.append(line)
        text = "\n".join(out)
    return text


def fix_body_phrases(text: str, kw: str, h1: str) -> str:
    b = keyword_phrase(kw, h1)
    b_plain = keyword_phrase(kw, h1, bold=False)
    src = source_label(h1)

    fixed_phrases = [
        (r"A mature workflow for \*\*this workflow\*\*", f"A mature {b} practice"),
        (r"turns \*\*this workflow\*\* into", f"turns {b} into"),
        (r"treat \*\*this workflow\*\* as", f"treat {b} as"),
        (r"teams that scale \*\*this workflow\*\*", f"teams that scale {b}"),
        (r"pattern for \*\*this workflow\*\*", f"pattern for {b}"),
        (r"when \*\*this workflow\*\* outputs", f"when {b} outputs"),
        (r"\*\*this workflow\*\* should include", f"{b} should include"),
        (r"collaborate on \*\*this workflow\*\*", f"collaborate on {b}"),
        (r"review \*\*this workflow\*\* outcomes", f"review {b} outcomes"),
        (r"A production operating model for \*\*this workflow\*\*", f"A production operating model for {b}"),
        (r"where \*\*this workflow\*\* shifts", f"where {b} shifts"),
        (r"accelerator for \*\*this workflow\*\* at scale", f"accelerator for {b} at scale"),
        (r"\*\*this connector workflow\*\* outputs", f"{b} outputs"),
        (r"When \*\*this connector workflow\*\* questions", f"When {b} questions"),
    ]
    for pat, repl in fixed_phrases:
        text = re.sub(pat, repl, text, flags=re.I)

    # FAQ answers and remaining plain occurrences
    if src:
        text = re.sub(
            rf"Most teams deploy this workflow with {re.escape(src)}",
            f"Most teams deploy {b_plain}",
            text,
            flags=re.I,
        )
        text = re.sub(
            rf"allow this workflow to merge {re.escape(src)}",
            f"allow {b_plain} to merge {src}",
            text,
            flags=re.I,
        )
    text = re.sub(r"this workflow can be run", f"{b_plain} can be run", text, flags=re.I)
    text = re.sub(r"so this workflow outputs", f"so {b_plain} outputs", text, flags=re.I)
    text = re.sub(r"scaling this workflow beyond", f"scaling {b_plain} beyond", text, flags=re.I)
    text = re.sub(r"for this workflow\?\?", f"for {b_plain}?", text, flags=re.I)
    text = re.sub(r"for this workflow\?", f"for {b_plain}?", text, flags=re.I)

    # Residual generic placeholders
    text = GENERIC_CONNECTOR.sub(b_plain, text)
    text = GENERIC_WORKFLOW.sub(b_plain, text)
    return text


def process(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    kw = extract_keyword(original)
    if not kw:
        return False
    h1 = extract_h1(original)
    text = fix_faq_headers(original, kw, h1)
    if GENERIC_WORKFLOW.search(text) or GENERIC_CONNECTOR.search(text):
        text = fix_body_phrases(text, kw, h1)
    if text == original:
        return False
    path.write_text(text, encoding="utf-8")
    return True


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
        targets = []
        for pillar in PILLARS:
            if pillar.is_dir():
                targets.extend(sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")))

    changed = 0
    for art in targets:
        if process(art):
            changed += 1
            print(f"fixed: {art.parent.name}")
    print(f"\nUpdated {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
