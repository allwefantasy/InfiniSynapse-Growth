#!/usr/bin/env python3
"""EEAT reinforcement for Pillar 26–30:
1) Insert missing Key Definition blocks (7 articles)
2) Add Scope note (limitations) after How We* sections when missing
3) Idempotent — safe to re-run
"""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"

KEY_DEFS: dict[str, tuple[str, str]] = {
    # folder -> (anchor snippet unique to file, key definition block to insert AFTER that snippet's paragraph)
    "434-python-for-data-engineering": (
        "**Python for data engineering** dominates because it combines readability, a vast library ecosystem, and the ability to glue disparate tools together. An engineer can connect to a database, call an API, transform data, and orchestrate the flow all in one accessible language.",
        "\n\n> **Key Definition**: **Python for data engineering** is the practice of using Python — with libraries such as pandas, PySpark, and orchestration clients — to build, test, and operate reliable data pipelines and transformations in production, not merely to explore data in notebooks.\n",
    ),
    "438-python-data-engineering-news": (
        "Not everything labeled **python data engineering news** matters. A new micro-library rarely changes practice; a shift in the default data-manipulation engine or a new interoperability standard does.",
        "\n\n> **Key Definition**: **python data engineering news** worth acting on is any development that durably changes how engineers should write, run, or operate Python-based pipelines and data jobs — as opposed to incremental library releases that do not alter day-to-day practice.\n",
    ),
    "441-data-engineer-vs-data-scientist": (
        "To understand **data engineer vs data scientist**, start with each role on its own. A data engineer builds and operates the pipelines, storage, and infrastructure that make data reliable and available.",
        "\n\n> **Key Definition**: the **data engineer vs data scientist** distinction separates who builds reliable data systems (the engineer) from who builds models and insight on top of that data (the scientist) — complementary roles that fail when one person is expected to own both without clear sequencing.\n",
    ),
    "442-what-do-data-engineers-do": (
        "At its core, what data engineers do is build systems that reliably move and prepare data. They connect to sources, write transformations, organize storage, and orchestrate the whole flow so it runs dependably.",
        "\n\n> **Key Definition**: what data engineers do is design, build, and operate the pipelines, storage, and quality controls that move and prepare data so analysts, applications, and models can depend on it every day — with reliability, not one-off scripts, as the measure of the job.\n",
    ),
    "443-what-does-a-data-engineer-do": (
        "No matter the context, what does a data engineer do always includes a core: building pipelines that move data, transforming it into usable form, and keeping the whole flow reliable.",
        "\n\n> **Key Definition**: answering what does a data engineer do means describing a role that ingests, transforms, stores, and serves data through tested pipelines and infrastructure, with ownership of reliability that scales from a startup's first jobs to an enterprise platform team.\n",
    ),
    "446-what-is-a-data-engineer": (
        "At its core, the answer to what is a data engineer is a builder of reliable data systems. They connect to sources, transform data, organize storage, and orchestrate the flow — but more fundamentally, they take responsibility for data being trustworthy.",
        "\n\n> **Key Definition**: a **data engineer** is a professional who designs, builds, and maintains the systems that ingest, store, transform, and serve data reliably — so the rest of the organization can analyze and act without constantly repairing broken inputs.\n",
    ),
    "455-data-lake-vs-data-warehouse": (
        "To settle **data lake vs data warehouse**, start with each on its own. A data lake stores raw data of any type cheaply, applying schema on read for maximum flexibility. A data warehouse stores structured, modeled data, applying schema on write for consistency and trust.",
        "\n\n> **Key Definition**: **data lake vs data warehouse** is the choice between flexible, low-cost raw storage (the lake) and structured, governed analytical storage (the warehouse) — most modern stacks use both, matching each to the workload rather than forcing a single pattern.\n",
    ),
}

LIMIT_PAT = re.compile(
    r"\b(limitation|overkill|does not replace|not a substitute|we only tested|"
    r"this guide does not|out of scope|when this doesn|Scope note)\b",
    re.I,
)

METHOD_H2 = re.compile(
    r"^## How We[^\n]*\n",
    re.M,
)


def find_article(folder: str) -> Path | None:
    for pillar in list(BLOG.glob("pillar2[6-9]-*")) + list(BLOG.glob("pillar30-*")):
        art = pillar / folder / "article.md"
        if art.is_file():
            return art
    return None


def insert_key_definitions() -> int:
    n = 0
    for folder, (anchor, block) in KEY_DEFS.items():
        art = find_article(folder)
        if not art:
            print(f"MISSING {folder}")
            continue
        text = art.read_text(encoding="utf-8")
        if "Key Definition" in text:
            print(f"skip KD (exists) {folder}")
            continue
        if anchor not in text:
            print(f"ANCHOR NOT FOUND {folder}")
            continue
        # insert after the anchor paragraph (anchor ends mid-section; add after full paragraph)
        idx = text.find(anchor) + len(anchor)
        # skip trailing whitespace/newlines already after paragraph
        new_text = text[:idx] + block + text[idx:]
        art.write_text(new_text, encoding="utf-8")
        print(f"KD+ {folder}")
        n += 1
    return n


def target_keyword(text: str, folder: str) -> str:
    m = re.search(r"\*\*Direct answer:\*\*\s*\*\*([^*]+)\*\*", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"\*\*Who this is for\*\*:[^\n]*\*\*([^*]{3,70})\*\*", text)
    if m and "you'll learn" not in m.group(1).lower():
        return m.group(1).strip()
    skip = {"direct answer:", "who this is for", "what you'll learn", "target keyword"}
    start = text.find("## TL;DR")
    window = text[start : start + 1200] if start >= 0 else text[:1500]
    for m in re.finditer(r"\*\*([^*]{3,70})\*\*", window):
        phrase = m.group(1).strip()
        if phrase.lower().rstrip(":") in skip or phrase.lower().startswith("direct answer"):
            continue
        if "you'll learn" in phrase.lower():
            continue
        return phrase
    return re.sub(r"^\d+-", "", folder).replace("-", " ")


def scope_note(kw: str) -> str:
    return (
        f"\n**Scope note:** This guide reflects patterns we see when mid-market and enterprise teams "
        f"work with {kw} in 2026. It is not a substitute for legal counsel, vendor runbooks, or a "
        f"formal survey of every industry — and when a smaller toolset or lighter process would serve, "
        f"a full program is overkill.\n"
    )


def insert_scope_notes() -> int:
    n = 0
    for pillar in list(BLOG.glob("pillar2[6-9]-*")) + list(BLOG.glob("pillar30-*")):
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            if LIMIT_PAT.search(text):
                continue
            m = METHOD_H2.search(text)
            if not m:
                print(f"no method H2 {art.parent.name}")
                continue
            # find end of method section = next ## heading
            start = m.end()
            nxt = re.search(r"^## ", text[start:], re.M)
            if not nxt:
                continue
            insert_at = start + nxt.start()
            kw = target_keyword(text, art.parent.name)
            # avoid stuffing: use lighter phrasing if kw is very long
            if len(kw) > 45:
                kw = "this topic"
            note = scope_note(kw)
            new_text = text[:insert_at] + note + "\n" + text[insert_at:]
            art.write_text(new_text, encoding="utf-8")
            print(f"Scope+ {art.parent.name}")
            n += 1
    return n


def main():
    kd = insert_key_definitions()
    sc = insert_scope_notes()
    print(f"\nDone: key_definitions={kd} scope_notes={sc}")


if __name__ == "__main__":
    main()
