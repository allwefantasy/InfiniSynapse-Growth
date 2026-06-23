#!/usr/bin/env python3
"""Sync word-count, keyword-density, EEAT, and external-link gate status into audit.md files."""
import importlib.util
import re
import sys
from datetime import date
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]


def load_audit_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


wc_mod = load_audit_module("audit_wordcount", Path(__file__).parent / "audit-wordcount.py")
eeat_mod = load_audit_module("audit_eeat", Path(__file__).parent / "audit-eeat.py")


def ext_link_count(text: str) -> int:
    from urllib.parse import urlparse

    seen = set()
    for _, url in re.findall(r"\[([^\]]*)\]\((https?://[^)]+)\)", text):
        if "infinisynapse" in urlparse(url).netloc.lower():
            continue
        seen.add(url)
    return len(seen)


def gate_section(
    wc: int,
    kc: int,
    den: float,
    eeat_score: str,
    eeat_pass: bool,
    ext_n: int,
    sync_date: str,
) -> str:
    wc_ok = 2000 <= wc <= 2500
    den_ok = 1.2 <= den <= 1.7
    ext_ok = ext_n >= 5
    all_ok = wc_ok and den_ok and eeat_pass and ext_ok
    return (
        f"\n## Content Gate Status (synced {sync_date})\n\n"
        "| Gate | Status | Value |\n"
        "|---|---|---|\n"
        f"| Word count (TL;DR→end) | {'✅ Pass' if wc_ok else '❌ Fail'} | {wc:,} |\n"
        f"| Keyword density | {'✅ Pass' if den_ok else '❌ Fail'} | {den:.2f}% ({kc} hits) |\n"
        f"| EEAT quick scan | {'✅ Pass' if eeat_pass else '❌ Fail'} | {eeat_score} |\n"
        f"| External links (unique) | {'✅ Pass' if ext_ok else '❌ Fail'} | {ext_n} |\n"
        f"| **All deploy gates** | **{'✅ PASS' if all_ok else '❌ FAIL'}** | — |\n"
    )


def sync_audit(audit_path: Path, metrics: dict) -> bool:
    text = audit_path.read_text(encoding="utf-8")
    sync_date = metrics["sync_date"]
    section = gate_section(
        metrics["wc"],
        metrics["kc"],
        metrics["den"],
        metrics["eeat_score"],
        metrics["eeat_pass"],
        metrics["ext_n"],
        sync_date,
    )

    if re.search(r"^## Content Gate Status \(synced .+\)\s*$", text, re.M):
        text = re.sub(
            r"\n## Content Gate Status \(synced .+\)[\s\S]*?(?=\n## |\Z)",
            section,
            text,
            count=1,
        )
    else:
        m = re.search(r"\n---\n\n## ", text)
        insert_at = m.start() if m else len(text)
        text = text[:insert_at] + section + text[insert_at:]

    text = re.sub(
        r"(\*\*Word Count\*\*\s*\|\s*)~?[\d,]+",
        rf"\g<1>{metrics['wc']:,}",
        text,
    )
    text = re.sub(
        r"(audit_date:\s*)[\d-]+",
        rf"\g<1>{sync_date}",
        text,
        count=1,
    )

    text = re.sub(r"> \*\*Verdict: SHIP\*\*\*", "> **Verdict: SHIP**", text, count=1)

    img_dir = audit_path.parent / "images"
    hero_ok = any(
        p.stat().st_size > 1000
        for p in img_dir.glob("hero*.png")
    ) if img_dir.is_dir() else False
    if hero_ok and metrics["all_ok"]:
        text = re.sub(
            r"> \*\*Verdict: SHIP\*\*(?:\s*\*[^*]+\*)?",
            "> **Verdict: SHIP**",
            text,
            count=1,
        )
        for pat, repl in [
            (
                r"- \[ \] (?:Design hero[^\n]*|Add hero[^\n]*|Ship hero[^\n]*|Hero image[^\n]*|Produce hero[^\n]*)\n",
                "- [x] Hero and OG cover rendered\n",
            ),
            (
                r"- \[ \] (?:Design hero and decision visuals|Add deployment architecture visual[^\n]*|Add hero and [^\n]*visuals[^\n]*|Design neutral comparison visuals|Produce hero and decision-flow images)\n",
                "- [x] Body / decision visuals rendered\n",
            ),
        ]:
            text = re.sub(pat, repl, text, count=1)

    audit_path.write_text(text, encoding="utf-8")
    return True


def metrics_for(article: Path) -> dict:
    text = article.read_text(encoding="utf-8")
    kw_m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    keyword = kw_m.group(1) if kw_m else ""
    raw = wc_mod.extract_body_raw(text)
    wc = wc_mod.word_count(raw)
    kc = wc_mod.kw_count(raw, keyword) if keyword else 0
    den = (kc / wc * 100) if wc else 0.0
    eeat = eeat_mod.audit_article(article)
    ext_n = ext_link_count(text)
    sync_date = date.today().isoformat()
    all_ok = (
        2000 <= wc <= 2500
        and 1.2 <= den <= 1.7
        and eeat["pass"]
        and ext_n >= 5
    )
    return {
        "wc": wc,
        "kc": kc,
        "den": den,
        "eeat_score": eeat["score"],
        "eeat_pass": eeat["pass"],
        "ext_n": ext_n,
        "sync_date": sync_date,
        "all_ok": all_ok,
    }


def main() -> int:
    updated = 0
    for pillar in PILLARS:
        for article in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            audit = article.parent / "audit.md"
            if not audit.exists():
                continue
            m = metrics_for(article)
            sync_audit(audit, m)
            updated += 1
            print(f"  {article.parent.name}: wc={m['wc']} den={m['den']:.2f}% eeat={m['eeat_score']}")
    print(f"\nSynced {updated} audit.md files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
