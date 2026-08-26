#!/usr/bin/env python3
"""Remove duplicate / miswired weave boilerplate injected by overlap fixes."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from urllib.parse import urlparse

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

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")

_hdr_spec = importlib.util.spec_from_file_location("hdr", BLOG / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_hdr_spec)
assert _hdr_spec and _hdr_spec.loader
_hdr_spec.loader.exec_module(_hdr)

# First ~45 chars of each weave (before the markdown link) for dedupe keys.
WEAVE_PREFIXES: list[str] = []
for src in _hdr.HIGH_DR_SOURCES:
    weave = src.get("weave", "")
    if not weave:
        continue
    before_link = weave.split("[", 1)[0].strip()
    if len(before_link) >= 20:
        WEAVE_PREFIXES.append(before_link)

# Anchor label fragment -> expected URL host substring.
ANCHOR_HOST: list[tuple[str, str]] = [
    ("RFC 4180", "rfc-editor.org"),
    ("Stanford HAI", "hai.stanford.edu"),
    ("IBM augmented", "ibm.com"),
    ("MariaDB", "mariadb.com"),
    ("Elastic", "elastic.co"),
    ("AWS Well-Architected", "amazon.com"),
    ("Supabase", "supabase.com"),
    ("Snowflake Cortex", "snowflake.com"),
    ("Redis", "redis.io"),
    ("BIRD", "bird-bench"),
    ("Spider NL2SQL", "yale-lily.github.io"),
    ("OWASP", "owasp.org"),
    ("NIST AI", "nist.gov"),
    ("ENISA", "enisa.europa.eu"),
    ("Google SRE", "sre.google"),
    ("Wikipedia data warehouse", "wikipedia.org"),
    ("Wikipedia ETL", "wikipedia.org"),
    ("conceptual data", "wikipedia.org"),
    ("Microsoft data architecture", "learn.microsoft.com"),
    ("Google Cloud", "cloud.google.com"),
    ("ISO/IEC", "iso.org"),
    ("PostgreSQL", "postgresql.org"),
    ("MongoDB", "mongodb.com"),
    ("BigQuery", "cloud.google.com"),
    ("ClickHouse", "clickhouse.com"),
    ("OpenTelemetry", "opentelemetry.io"),
    ("Databricks", "databricks.com"),
]


def weave_key(line: str) -> str | None:
    stripped = line.strip()
    for prefix in WEAVE_PREFIXES:
        if stripped.startswith(prefix) or prefix in stripped:
            return prefix
    return None


def miswired(line: str) -> bool:
    for anchor_hint, host_hint in ANCHOR_HOST:
        for label, url in LINK_RE.findall(line):
            if anchor_hint.lower() in label.lower():
                host = urlparse(url).netloc.lower()
                if host_hint not in host and "wikipedia.org" not in host_hint:
                    return True
                if host_hint == "wikipedia.org" and "wikipedia.org" not in host:
                    return True
    return False


def clean(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    seen_weave: set[str] = set()
    out: list[str] = []
    removed = 0

    for line in lines:
        stripped = line.strip()
        if (
            not stripped
            or stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith("![")
            or stripped.startswith("```")
            or stripped.startswith(">")
            or stripped.startswith("- ")
            or stripped.startswith("* ")
        ):
            out.append(line)
            continue

        if miswired(line):
            removed += 1
            continue

        key = weave_key(line)
        if key:
            if key in seen_weave:
                removed += 1
                continue
            seen_weave.add(key)

        out.append(line)

    # Collapse 3+ consecutive blank lines
    collapsed: list[str] = []
    blank_run = 0
    for line in out:
        if not line.strip():
            blank_run += 1
            if blank_run <= 2:
                collapsed.append(line)
        else:
            blank_run = 0
            collapsed.append(line)

    return "\n".join(collapsed) + ("\n" if text.endswith("\n") else ""), removed


def main() -> int:
    total_removed = 0
    changed = 0
    for pillar in PILLARS:
        if not pillar.is_dir():
            continue
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            original = art.read_text(encoding="utf-8")
            new, n = clean(original)
            if new != original:
                art.write_text(new, encoding="utf-8")
                changed += 1
                total_removed += n
                print(f"  {art.parent.name}: removed {n} lines")
    print(f"\nUpdated {changed} articles, removed {total_removed} boilerplate lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
