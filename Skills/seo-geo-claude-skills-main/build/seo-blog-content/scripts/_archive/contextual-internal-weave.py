#!/usr/bin/env python3
"""Contextual single-link internal weave helpers (no cluster list paragraphs)."""
from __future__ import annotations

import re

LIST_WEAVE_INTROS = (
    "Within this topic cluster",
    "To continue in this cluster",
    "For the next step in this cluster",
    "Readers building on this guide",
    "For adjacent depth in the same cluster",
)

LIST_WEAVE_OUTROS = (
    "as you operationalize this workflow",
    "when you extend this workflow across the cluster",
    "for the surrounding workflow context",
)

COMMA_BLOG_CHAIN = re.compile(
    r"(\[[^\]]+\]\(/blog/[^)]+\))(?:,\s*(?:and\s+)?\[[^\]]+\]\(/blog/[^)]+\))+",
    re.I,
)

LIST_WEAVE_RE = re.compile(
    r"^\s*(?:"
    + "|".join(re.escape(x) for x in LIST_WEAVE_INTROS)
    + r")[^\n]*(?:"
    + "|".join(re.escape(x) for x in LIST_WEAVE_OUTROS)
    + r")[^\n]*\s*$",
    re.I | re.M,
)

STOP_TOKENS = {
    "to", "ai", "an", "the", "for", "with", "in", "how", "what", "is", "a", "data",
    "analysis", "connect", "analyst", "tools", "vs", "best", "and", "of", "on", "or",
    "from", "your", "using", "guide", "2026", "review", "alternatives", "evaluate",
}

NOUN_ALIASES: dict[str, tuple[str, ...]] = {
    "postgres": ("postgresql", "postgres"),
    "mysql": ("mysql",),
    "snowflake": ("snowflake", "warehouse"),
    "bigquery": ("bigquery",),
    "databricks": ("databricks", "lakehouse"),
    "mongodb": ("mongodb", "mongo", "document"),
    "supabase": ("supabase",),
    "clickhouse": ("clickhouse", "olap"),
    "redshift": ("redshift",),
    "stripe": ("stripe", "payments", "billing"),
    "shopify": ("shopify", "ecommerce"),
    "csv": ("csv", "file export", "spreadsheet export"),
    "excel": ("excel", "spreadsheet"),
    "sheets": ("google sheets", "spreadsheet"),
    "airtable": ("airtable",),
    "notion": ("notion",),
    "nl2sql": ("nl2sql", "text-to-sql", "natural language"),
    "sql": ("sql", "query"),
    "prompt": ("prompt", "template"),
    "glossary": ("glossary", "terminology"),
    "finance": ("finance", "fp&a"),
    "marketing": ("marketing", "campaign"),
    "healthcare": ("healthcare", "hipaa"),
    "saas": ("saas", "subscription"),
    "product": ("product manager", "roadmap"),
    "engineer": ("data engineer", "pipeline"),
    "cto": ("cto", "executive"),
    "founder": ("founder", "startup"),
    "logistics": ("logistics", "supply chain"),
    "operations": ("operations", "ops"),
    "ecommerce": ("ecommerce", "retail"),
}


def decomma_internal_link_runs(text: str) -> str:
    """Keep first /blog/ link in comma chains; drop sibling links from same clause."""

    def _one_link(m: re.Match[str]) -> str:
        return m.group(1)

    return COMMA_BLOG_CHAIN.sub(_one_link, text)


def split_dense_blog_lines(text: str) -> str:
    """Break single lines that contain 3+ /blog/ links across multiple sentences."""
    chunks: list[str] = []
    for line in text.splitlines():
        if line.count("](/blog/") >= 3 and ". " in line:
            parts = re.split(r"(?<=\.)\s+", line)
            if sum(p.count("](/blog/") for p in parts) >= 3:
                chunks.extend(parts)
                chunks.append("")
                continue
        chunks.append(line)
    return "\n".join(chunks)


def remove_cluster_list_paragraphs(text: str) -> str:
    """Strip formulaic multi-link cluster paragraphs."""
    lines = text.splitlines()
    kept: list[str] = []
    for line in lines:
        low = line.lower()
        if LIST_WEAVE_RE.match(line):
            continue
        if any(intro.lower() in low for intro in LIST_WEAVE_INTROS):
            if line.count("](/blog/") >= 2:
                continue
        if any(outro in low for outro in LIST_WEAVE_OUTROS):
            continue
        kept.append(line)
    out = "\n".join(kept)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def short_title(title: str) -> str:
    t = title.strip()
    if len(t) <= 52:
        return t
    if ":" in t:
        return t.split(":")[0].strip()
    return t[:49].rstrip() + "…"


def slug_noun(slug: str) -> str:
    for key, _ in NOUN_ALIASES.items():
        if key in slug:
            return key.replace("nl2sql", "NL2SQL").title()
    tokens = [t for t in slug.split("-") if t not in STOP_TOKENS and len(t) > 2]
    if not tokens:
        return "this topic"
    return tokens[0].title()


def keywords_for_slug(slug: str) -> list[str]:
    kws: list[str] = []
    for key, aliases in NOUN_ALIASES.items():
        if key in slug:
            kws.extend(aliases)
    for t in slug.split("-"):
        if t not in STOP_TOKENS and len(t) > 2:
            kws.append(t)
    return list(dict.fromkeys(kws))


def is_embeddable_paragraph(para: str) -> bool:
    s = para.strip()
    if not s or len(s) < 60:
        return False
    if s.startswith(
        ("##", "|", "```", ">", "![", "**Slug", "**Target", "---", "1. [", "- ", "* ")
    ):
        return False
    if re.match(r"^\d+\.\s", s):
        return False
    if s.count("](/blog/") >= 2:
        return False
    return True


def split_paragraphs(text: str) -> list[tuple[int, int, str]]:
    """Return (start, end, paragraph) for double-newline blocks."""
    blocks: list[tuple[int, int, str]] = []
    for m in re.finditer(r"\n\n+", text):
        pass
    pos = 0
    for chunk in re.split(r"(\n\n+)", text):
        if not chunk:
            continue
        if re.fullmatch(r"\n\n+", chunk):
            pos += len(chunk)
            continue
        start = pos
        end = pos + len(chunk)
        blocks.append((start, end, chunk))
        pos = end
    return blocks


def pick_anchor_index(
    blocks: list[tuple[int, int, str]], keywords: list[str], seed: int, used: set[int]
) -> int | None:
    candidates: list[tuple[float, int]] = []
    embeddable = [
        (i, b)
        for i, b in enumerate(blocks)
        if is_embeddable_paragraph(b[2]) and i not in used and "](/blog/" not in b[2]
    ]
    if not embeddable:
        embeddable = [
            (i, b) for i, b in enumerate(blocks) if is_embeddable_paragraph(b[2]) and i not in used
        ]
    if not embeddable:
        return None
    for i, (_, _, para) in embeddable:
        low = para.lower()
        score = sum(2.0 for k in keywords if k in low)
        if "connector" in low or "workflow" in low or "memory" in low:
            score += 0.5
        if "multi-source" in low or "governance" in low or "stack" in low:
            score += 0.5
        if "](/blog/" in para:
            score -= 1.0
        candidates.append((score, i))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    top_score = candidates[0][0]
    top = [i for s, i in candidates if s >= max(0.5, top_score - 0.5)]
    return top[seed % len(top)]


def contextual_sentence(title: str, url: str, slug: str, seed: int) -> str:
    link = f"[{short_title(title)}]({url})"
    noun = slug_noun(slug)
    variants = [
        f"If {noun} is in scope for your team, reuse the same memory-and-trace checklist in {link}.",
        f"Analysts wiring {noun} into production reviews can follow the parallel walkthrough in {link}.",
        f"The credential, preflight, and SQL-trace pattern above also applies to {noun}—see {link} for source-specific steps.",
        f"When {noun} joins a multi-source stack, align connector scope and review gates using {link}.",
        f"Teams standardizing governance across sources often keep {link} beside this runbook for {noun} handoffs.",
    ]
    return variants[seed % len(variants)]


def insert_after_paragraph(text: str, para_index: int, sentence: str) -> str:
    blocks = split_paragraphs(text)
    if para_index < 0 or para_index >= len(blocks):
        return text.rstrip() + "\n\n" + sentence + "\n"
    _, end, para = blocks[para_index]
    if sentence in para or sentence in text:
        return text
    return text[:end] + "\n\n" + sentence + text[end:]


WEAVE_SPLIT = re.compile(
    r"(?<=\.)\s+(?=(?:If |Analysts wiring |The credential, preflight|When |Teams standardizing))",
)


def split_stacked_weaves(text: str) -> str:
    chunks: list[str] = []
    for line in text.splitlines():
        if line.count("](/blog/") >= 2 and WEAVE_SPLIT.search(line):
            parts = WEAVE_SPLIT.split(line)
            for i, part in enumerate(parts):
                chunks.append(part)
                if i < len(parts) - 1:
                    chunks.append("")
            continue
        chunks.append(line)
    return "\n".join(chunks)


def normalize_internal_prose(text: str) -> str:
    text = remove_cluster_list_paragraphs(text)
    text = decomma_internal_link_runs(text)
    text = split_dense_blog_lines(text)
    text = split_stacked_weaves(text)
    return re.sub(r"\n{3,}", "\n\n", text)


def embed_link(text: str, title: str, url: str, seed: int, used: set[int]) -> tuple[str, set[int]]:
    slug = url.replace("/blog/", "").strip("/")
    if slug in {m.group(1) for m in re.finditer(r"\]\(/blog/([^)]+)\)", text)}:
        return text, used
    sentence = contextual_sentence(title, url, slug, seed)
    if sentence in text:
        return text, used
    blocks = split_paragraphs(text)
    idx = pick_anchor_index(blocks, keywords_for_slug(slug), seed, used)
    if idx is None:
        m = re.search(r"\n(## (?:Conclusion|Frequently Asked Questions))\s*\n", text)
        if m:
            return text[: m.start()] + "\n\n" + sentence + "\n" + text[m.start() :], used
        return text.rstrip() + "\n\n" + sentence + "\n", used
    used.add(idx)
    return insert_after_paragraph(text, idx, sentence), used
