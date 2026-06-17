#!/usr/bin/env python3
"""Restore corrupted FAQ blocks, sync schema.json, trim keyword-stuffed headers."""
from __future__ import annotations

import json
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

FAQ_CORRUPT = re.compile(r"^### .+### ")
MIDLINE_HASH = re.compile(r"[^\n#](#{2,3} )")
GENERIC_FAQ_Q = re.compile(r"\bthis (?:connector )?workflow\b", re.I)

PILLAR7_FAQ: list[tuple[str, str]] = []  # filled below
PILLAR6_FAQ: list[tuple[str, str]] = []


def _init_templates() -> None:
    global PILLAR7_FAQ, PILLAR6_FAQ
    PILLAR7_FAQ = [
        (
            "How does this approach help teams make faster decisions?",
            "{kw} helps teams standardize multi-source analysis into one repeatable flow. Instead of rebuilding logic every cycle, teams reuse validated assumptions, which shortens the path from question to decision-ready output.",
        ),
        (
            "What data sources should be connected first?",
            "Start with the three systems that most directly affect your core KPI: a system of record, a behavioral source, and a financial outcome source. This gives {kw} enough context to connect activity with business impact before expanding scope.",
        ),
        (
            "Can this approach meet strict governance requirements?",
            "Yes. Mature implementations of {kw} use source-level permissions, auditable execution timelines, and reviewer checkpoints. That combination supports speed while keeping compliance and stakeholder trust intact.",
        ),
        (
            "What makes InfiniSynapse a fit for recurring multi-source workflows?",
            "InfiniSynapse is designed for recurring analysis loops where teams need memory, process traceability, and cross-source orchestration. In {kw}, those capabilities reduce repetitive analyst labor and make week-over-week outputs more consistent.",
        ),
        (
            "How long does it take to show ROI?",
            "Most teams see early ROI in 30 days when they focus on one recurring workflow and track cycle time, rework, and decision confidence. {kw} compounds value when operators standardize weekly review, connector hygiene, and reusable memory—not one-off demos.",
        ),
    ]
    PILLAR6_FAQ = [
        (
            "How much data can the pipeline handle before it slows down?",
            "Most spreadsheet-first teams can process medium files quickly, but performance depends on transform complexity, not only row count. Teams should benchmark with a real monthly file and track runtime, review effort, and correction rate before broad rollout.",
        ),
        (
            "How do we validate output quality before sharing results?",
            "Use a three-layer gate: technical checks for types and nulls, business checks for metric definitions, and stakeholder checks for interpretation. Teams that require all three gates cut revision loops and raise trust in AI-assisted reporting.",
        ),
        (
            "What skills does the team need to adopt this approach?",
            "A strong operator does not need advanced coding skills, but does need data literacy, metric ownership, and review discipline. The biggest differentiator is not prompt creativity; it is the ability to define quality criteria clearly.",
        ),
        (
            "When should we move beyond spreadsheet-only AI tools?",
            "Move when recurrence, source complexity, or governance load rises. If teams keep rebuilding prompts each cycle, struggle to connect source systems, or cannot track KPI lineage, they should adopt memory-backed workflows with connectors.",
        ),
        (
            "How does InfiniSynapse fit this analytics workflow?",
            "InfiniSynapse is most useful when teams outgrow one-off spreadsheet conversations and need stable recurring execution. Memory cards preserve prior logic, connectors reduce manual file movement, and recurring KPI runs keep operations consistent.",
        ),
    ]


_init_templates()


def extract_keyword(text: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).strip() if m else ""


def faq_from_schema(schema_path: Path) -> list[tuple[str, str]]:
    if not schema_path.is_file():
        return []
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    for block in data:
        if block.get("@type") == "FAQPage":
            out: list[tuple[str, str]] = []
            for q in block.get("mainEntity", []):
                out.append((q["name"], q["acceptedAnswer"]["text"]))
            return out
    return []


def extract_faq_block(text: str) -> str:
    m = re.search(
        r"^## Frequently Asked Questions\s*\n(.*?)(?=\n## Conclusion|\n---\s*\n## |\Z)",
        text,
        re.S | re.M,
    )
    return m.group(1) if m else ""


def faq_block_corrupt(block: str) -> bool:
    if not block:
        return False
    if FAQ_CORRUPT.search(block):
        return True
    if MIDLINE_HASH.search(block):
        return True
    if "``" in block or "`analytics`" in block:
        return True
    return False


def schema_pairs_corrupt(pairs: list[tuple[str, str]]) -> bool:
    for q, a in pairs:
        if MIDLINE_HASH.search(a) or "###" in a:
            return True
        if "``" in q or "`analytics`" in q:
            return True
    return False


def canonical_faq(pillar_dir: str, kw: str, folder: str) -> list[tuple[str, str]] | None:
    if "pillar7-use-cases" in pillar_dir:
        tpl = PILLAR7_FAQ
    elif "pillar6-ai-excel" in pillar_dir:
        tpl = PILLAR6_FAQ
    elif folder == "096-data-analysis-prompt-template":
        tpl = [
            (
                "What is the ideal length for a data analysis template?",
                "Aim for one screen of core instructions plus optional appendices. Too short means missing controls; too long hurts adoption.",
            ),
            (
                "Can one template work across multiple departments?",
                "Yes, if you separate universal blocks (objective, validation, output) from department-specific variables (metrics, source tables, thresholds).",
            ),
            (
                "How often should a data analysis template be reviewed?",
                "At least quarterly, or after schema changes, source migrations, or major policy updates.",
            ),
            (
                "How does a template connect to data agents?",
                "Templates define the contract—goal, sources, checks, and output format—while data agents handle orchestration, making execution traceable and reusable.",
            ),
        ]
    elif folder == "098-how-to-evaluate-ai-data-analyst":
        tpl = [
            (
                "What are the most critical evaluation criteria for buyers?",
                "Validation rigor, governance controls, rerun consistency, and communication quality are usually the highest-impact criteria.",
            ),
            (
                "How many pilot scenarios are needed for a proper evaluation?",
                "At least four scenarios covering KPI reporting, diagnostics, reconciliation, and executive communication.",
            ),
            (
                "Should evaluation criteria differ by industry?",
                "Yes. Core requirements stay similar, but governance and compliance expectations vary by regulated context.",
            ),
            (
                "How often should evaluation criteria be updated?",
                "Review quarterly or after major connector, schema, or policy changes.",
            ),
        ]
    elif folder == "095-ai-data-analysis-prompts":
        tpl = [
            (
                "How many analysis prompts should a team launch with?",
                "Start with 12-15 prompts tied to your most frequent decisions. Expand only after you can measure reuse, correction loops, and cycle-time impact.",
            ),
            (
                "What makes analysis prompts trustworthy?",
                "Trust comes from explicit metric definitions, source boundaries, independent reconciliation, and confidence statements. Prompt style alone is never enough.",
            ),
            (
                "Should we assign an owner for each prompt family?",
                "Yes. Each prompt family needs a named owner responsible for revisions after schema changes, policy updates, and postmortem findings.",
            ),
            (
                "How do I connect prompts to data agent workflows?",
                "Map each prompt to a named data source, KPI, reviewer, and handoff. This makes orchestration auditable and reusable.",
            ),
        ]
    else:
        return None
    return [(q, a.format(kw=kw)) for q, a in tpl]


def faq_from_article(text: str) -> list[tuple[str, str]]:
    m = re.search(
        r"^## Frequently Asked Questions\s*\n(.*?)(?=\n## Conclusion|\n---\s*\n## |\Z)",
        text,
        re.S | re.M,
    )
    if not m:
        return []
    block = m.group(1).strip()
    pairs: list[tuple[str, str]] = []
    parts = re.split(r"\n(?=### )", block)
    for part in parts:
        part = part.strip()
        if not part.startswith("### "):
            continue
        lines = part.splitlines()
        q = lines[0][4:].strip()
        ans = "\n".join(lines[1:]).strip()
        if q and not FAQ_CORRUPT.search(lines[0]):
            pairs.append((q, ans))
    return pairs


def render_faq_section(pairs: list[tuple[str, str]]) -> str:
    chunks = ["## Frequently Asked Questions", ""]
    for q, a in pairs:
        chunks.extend([f"### {q}", "", a, ""])
    chunks.append("---")
    return "\n".join(chunks)


def replace_faq_section(text: str, pairs: list[tuple[str, str]]) -> str:
    new_block = render_faq_section(pairs)
    if "## Frequently Asked Questions" not in text:
        return text
    return re.sub(
        r"^## Frequently Asked Questions\s*\n.*?(?=\n## Conclusion|\n---\s*(?:\n|$)|\Z)",
        new_block + "\n\n",
        text,
        count=1,
        flags=re.S | re.M,
    )


def shorten_faq_questions(pairs: list[tuple[str, str]], kw: str) -> list[tuple[str, str]]:
    """Short FAQ titles; keep keyword in answers."""
    short_map = [
        (re.compile(r"^How much data can .+ handle before it slows down\?$", re.I), "How much data can the pipeline handle before it slows down?"),
        (re.compile(r"^How does InfiniSynapse fit .+\?$", re.I), "How does InfiniSynapse fit this analytics workflow?"),
        (re.compile(r"^How long does it take to (?:deploy|roll out) .+\?$", re.I), "How long does rollout take?"),
        (re.compile(r"^Do we need a dedicated data engineer for .+\?$", re.I), "Do we need a dedicated data engineer?"),
        (re.compile(r"^How does InfiniSynapse improve trust for .+\?$", re.I), "How does InfiniSynapse improve trust?"),
        (re.compile(r"^What security checks matter before scaling .+\?$", re.I), "What security checks matter before scaling?"),
        (re.compile(r"^How does .+ help .+ make faster decisions\?$", re.I), "How does this approach help teams make faster decisions?"),
        (re.compile(r"^What data sources should be connected first for .+\?$", re.I), "What data sources should be connected first?"),
        (re.compile(r"^Can .+ work with strict governance requirements\?$", re.I), "Can this approach meet strict governance requirements?"),
        (re.compile(r"^What makes InfiniSynapse a fit for recurring multi-source workflows in .+\?$", re.I), "What makes InfiniSynapse a fit for recurring multi-source workflows?"),
        (re.compile(r"^How long does it take to show ROI from .+\?$", re.I), "How long does it take to show ROI?"),
    ]
    out: list[tuple[str, str]] = []
    kw_l = kw.lower()
    for q, a in pairs:
        nq = q
        for pat, repl in short_map:
            if pat.match(q):
                nq = repl
                break
        if kw_l and kw_l in nq.lower() and "?" in nq:
            nq = re.sub(re.escape(kw), "analytics", nq, flags=re.I)
            nq = re.sub(r"\s{2,}", " ", nq).strip()
        out.append((nq, a))
    return out


def repair_merged_h2_lines(text: str, kw: str) -> str:
    """Fix ## Title ## Title… lines corrupted by keyword-stripping scripts."""
    lines = text.splitlines()
    out: list[str] = []
    kw_title = (
        kw.title()
        if len(kw) < 40
        else " ".join(part.title() for part in kw.split()[:4])
    )
    for line in lines:
        m = re.match(r"^## (.+?) ## (.+)$", line)
        if line == "## Common Pitfalls With":
            out.append(f"## Common Pitfalls With {kw_title}")
            continue
        if line.startswith("Common Pitfalls Withst-pass"):
            out.append(
                "**Pitfall 1 — Publishing AI-first-pass SQL for executive metrics.** "
                "AI drafts fast; validation is still human work. Build mandatory review before external distribution."
            )
            continue
        if m:
            left = m.group(1).strip()
            right = m.group(2).strip()
            if "Pitfalls" in left:
                title = f"## Common Pitfalls With {kw_title}"
                body = re.sub(
                    r"^With\w*\s*.*?\*\*",
                    "**Pitfall 1 — Publishing AI-first-pass SQL for executive metrics.**",
                    right,
                    count=1,
                    flags=re.I,
                )
                if "Pitfall 1" not in body and right.startswith("With"):
                    body = f"**{kw}** hit predictable walls:\n\n{right}"
            elif "ROI" in left:
                title = f"## ROI Signals From {kw_title}"
                body = right
            else:
                title = f"## {left}"
                body = right
            out.extend([title, "", body, ""])
            continue
        if not line.startswith("##") and "## ROI Signals From" in line:
            line = re.sub(
                r"After\s*(?:## ROI Signals From\w+.*?\*\*|s## ROI Signals Froms?\*\*)",
                f"After a disciplined **{kw}** rollout, healthy teams usually see:",
                line,
                flags=re.I,
            )
        if line in ("## ROI Signals From this approach", "## ROI Signals From"):
            line = f"## ROI Signals From {kw_title}"
        out.append(line)
    return "\n".join(out)


def trim_keyword_headers(text: str, kw: str) -> str:
    if not kw:
        return text
    kw_l = kw.lower()
    known_short = {
        rf'## What "good" looks like for {re.escape(kw)}': '## What "good" looks like in practice',
        rf"## What \"good\" looks like in {re.escape(kw)}": '## What "good" looks like in practice',
        rf"## Why {re.escape(kw)} matters now": "## Why this matters now",
        rf"## Pain Points for {re.escape(kw)}": "## Pain Points for operators",
        rf"## Workflow Playbook for {re.escape(kw)}": "## Workflow Playbook",
        rf"## 30-Day Rollout Plan for {re.escape(kw)}": "## 30-Day Rollout Plan",
    }
    for pat, repl in known_short.items():
        text = re.sub(pat, repl, text, flags=re.I)

    matches = list(re.finditer(r"^(#{2,3})\s+(.+)$", text, re.M))
    kw_matches = [m for m in matches if kw_l in m.group(2).lower()]
    if len(kw_matches) < 3:
        return text

    keep_pos = {kw_matches[0].start(), kw_matches[1].start()}
    for m in reversed(kw_matches):
        if m.start() in keep_pos:
            continue
        level, title = m.group(1), m.group(2)
        if level == "###" and "?" in title:
            new_title = re.sub(re.escape(kw), "analytics", title, flags=re.I)
        else:
            new_title = re.sub(re.escape(kw), "", title, flags=re.I)
        new_title = re.sub(r"\s{2,}", " ", new_title).strip(" :")
        if not new_title or len(new_title) < 8:
            new_title = "Practical notes"
        text = text[: m.start()] + f"{level} {new_title}" + text[m.end() :]
    return text


def sync_schema_faq(schema_path: Path, pairs: list[tuple[str, str]]) -> bool:
    if not schema_path.is_file() or not pairs:
        return False
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    changed = False
    for block in data:
        if block.get("@type") != "FAQPage":
            continue
        entities = []
        for q, a in pairs:
            entities.append(
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
            )
        if block.get("mainEntity") != entities:
            block["mainEntity"] = entities
            changed = True
    if changed:
        schema_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def process_article(article_path: Path) -> tuple[bool, bool]:
    """Returns (article_changed, schema_changed)."""
    schema_path = article_path.parent / "schema.json"
    original = article_path.read_text(encoding="utf-8")
    kw = extract_keyword(original)
    text = original
    article_changed = False
    pillar_dir = article_path.parent.parent.name
    folder = article_path.parent.name

    faq_block = extract_faq_block(text)
    schema_pairs = faq_from_schema(schema_path)
    article_pairs = faq_from_article(text)

    stale_faq = any(p in faq_block for p in (
        "performs best when teams prioritize repeatability over one-off demos",
    ))
    if faq_block_corrupt(faq_block) or schema_pairs_corrupt(schema_pairs) or stale_faq:
        pairs: list[tuple[str, str]] | None = None
        if schema_pairs and not schema_pairs_corrupt(schema_pairs) and not stale_faq:
            pairs = schema_pairs
        if pairs is None:
            pairs = canonical_faq(pillar_dir, kw, folder)
        if pairs:
            text = replace_faq_section(text, pairs)
            article_changed = True
            article_pairs = pairs

    if article_pairs and not schema_pairs_corrupt(article_pairs):
        shortened = shorten_faq_questions(article_pairs, kw)
        if shortened != article_pairs:
            text = replace_faq_section(text, shortened)
            article_changed = True
            article_pairs = shortened

    repaired = repair_merged_h2_lines(text, kw)
    if repaired != text:
        text = repaired
        article_changed = True

    trimmed = trim_keyword_headers(text, kw)
    if trimmed != text:
        text = trimmed
        article_changed = True

    if article_changed:
        article_path.write_text(text, encoding="utf-8")
        article_pairs = faq_from_article(text)

    schema_changed = False
    if article_pairs and not schema_pairs_corrupt(article_pairs):
        schema_text = schema_path.read_text(encoding="utf-8") if schema_path.is_file() else ""
        schema_dirty = schema_pairs_corrupt(faq_from_schema(schema_path)) or GENERIC_FAQ_Q.search(schema_text)
        if article_changed or schema_dirty:
            schema_changed = sync_schema_faq(schema_path, article_pairs)

    return article_changed, schema_changed


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
            if pillar.is_dir():
                targets.extend(sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")))

    art_n = schema_n = 0
    for art in targets:
        ac, sc = process_article(art)
        if ac:
            art_n += 1
            print(f"article: {art.parent.name}")
        if sc:
            schema_n += 1
            print(f"schema:  {art.parent.name}")
    print(f"\nUpdated {art_n} articles, {schema_n} schema.json files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
