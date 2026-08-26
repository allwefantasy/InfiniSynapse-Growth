#!/usr/bin/env python3
"""Embed all links naturally: remove CMS tables, fix bare bullets, product entry lines."""
from __future__ import annotations

import re
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

RELATED_INTROS = [
    "For foundational context, see",
    "To compare tooling options, read",
    "For workflow patterns, review",
    "On architecture and memory, see",
    "For adjacent depth, explore",
    "To extend this guide, read",
    "For connector setup, see",
    "On evaluation criteria, read",
    "When hiring or upskilling, review",
    "For platform comparisons, read",
]

SLUG_TITLE = {
    "connect-postgres-to-ai-data-analyst": "Connect Postgres to AI Data Analyst",
    "connect-supabase-to-ai-data-analyst": "Connect Supabase to AI Data Analyst",
}


def remove_internal_link_recommendations(text: str) -> str:
    return re.sub(
        r"\n## Internal Link Recommendations\n.*?(?=\n---\s*\n|\Z)",
        "",
        text,
        flags=re.S,
    )


def fix_bare_related_bullets(text: str) -> str:
    """`- [Title](/blog/x) — description` → prose bullet."""
    idx = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal idx
        title, url, desc = m.group(1).strip(), m.group(2), m.group(3).strip()
        intro = RELATED_INTROS[idx % len(RELATED_INTROS)]
        idx += 1
        desc_clean = desc.rstrip(".")
        return f"- {intro} [{title}]({url}) — {desc_clean}."

    text = re.sub(
        r"^-\s+\[([^\]]+)\]\((/blog/[^)]+)\)\s*—\s*(.+?)\s*$",
        repl,
        text,
        flags=re.M,
    )
    return text


def fix_slug_anchor_bullets(text: str) -> str:
    """`[045 · connect postgres to ai data analyst](/blog/...)` → proper title."""

    def repl(m: re.Match[str]) -> str:
        slug = m.group(1)
        title = SLUG_TITLE.get(slug, slug.replace("-", " ").title())
        return f"[{title}](/blog/{slug})"

    return re.sub(
        r"\[\d+\s*·\s*([a-z0-9-]+)\]\(/blog/\1\)",
        repl,
        text,
        flags=re.I,
    )


def fix_product_entry_line(text: str) -> str:
    text = re.sub(
        r"\n\*\*Product entry\*\*:\s+\[app\.infinisynapse\.cn\]\(https://app\.infinisynapse\.cn\)\s*\n",
        "\n\nYou can try the same workflow on the [InfiniSynapse web app](https://app.infinisynapse.cn) with a free tier.\n",
        text,
    )
    text = re.sub(
        r"(free tier\.)\n(---)",
        r"\1\n\n\2",
        text,
    )
    text = re.sub(
        r"\[app\.infinisynapse\.cn\]\(https://app\.infinisynapse\.cn\)",
        "[the InfiniSynapse web app](https://app.infinisynapse.cn)",
        text,
    )
    return text


def fix_process(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original
    text = remove_internal_link_recommendations(text)
    text = fix_bare_related_bullets(text)
    text = fix_slug_anchor_bullets(text)
    text = fix_product_entry_line(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if fix_process(art):
                changed += 1
                print(f"fixed: {art.parent.name}")
    print(f"\nUpdated {changed} articles")


if __name__ == "__main__":
    main()
