#!/usr/bin/env python3
"""CORE-EEAT quick scan for Pillar 1 + Pillar 3 blog articles.

Checks aligned with seo-geo-claude-skills-main on-page auditor § CORE-EEAT Quick Scan
and core-eeat-benchmark.md veto-adjacent items (T04, C01, R10 proxies).
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

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

CHECKS = [
    ("T04", "Brand/disclosure byline", r"We build InfiniSynapse|InfiniSynapse Data Team"),
    ("R06", "Last updated 2026", r"Last updated:\s*2026"),
    ("C02", "TL;DR section", r"^## TL;DR\s*$"),
    ("C04", "Key Definition block", r"Key Definition|> \*\*[^*]+\*\*"),
    ("C09", "FAQ (>=4 questions)", None),
    ("R02", "External citations (>=3, density)", None),
    ("R08", "Internal links (>=3)", None),
    ("Exp01", "Hands-on / first-person", r"We (build|evaluate|evaluated|work|maintain|apply)|hands-on|Evaluation basis"),
    ("E02", "Framework / original signal", r"scorecard|framework|five.pillar|30.day|\d+%|\d+ minutes"),
    ("Ept01", "Schema author", None),
    ("O05", "schema.json present", None),
    ("O01", "Table of Contents", r"## Table of Contents"),
]


def wc_body(text: str) -> int:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"`([^`]+)`", r"\1", body)
    body = re.sub(r"^#+\s+", "", body, flags=re.M)
    body = re.sub(r"\*\*([^*]+)\*\*", r"\1", body)
    body = re.sub(r"\|", " ", body)
    return len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", body))


def external_links(text: str) -> list[str]:
    seen = set()
    out = []
    for _, url in re.findall(r"\[([^\]]*)\]\((https?://[^)]+)\)", text):
        if "infinisynapse" in urlparse(url).netloc.lower():
            continue
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def internal_links(text: str) -> int:
    """Count unique internal blog links (relative /blog/ paths or absolute infinisynapse.com/.../blog/)."""
    rel = set(re.findall(r"(?:\]\(|href=)((?:/(?:en|zh)/blog/|/blog/)[^)\s\"']+)", text))
    abs_urls = set()
    for url in re.findall(r"\]\((https?://[^)]+)\)", text):
        host = urlparse(url).netloc.lower()
        if "infinisynapse.com" in host and "/blog/" in url:
            abs_urls.add(url.rstrip("/"))
    return len(rel | abs_urls)


def audit_article(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fails = []
    passes = []

    for cid, label, pattern in CHECKS:
        ok = False
        if cid == "C09":
            ok = ("## Frequently Asked Questions" in text or "## FAQ" in text) and len(
                re.findall(r"^### .+\?\s*$", text, re.M)
            ) >= 4
        elif cid == "R02":
            ext = external_links(text)
            w = wc_body(text)
            ok = len(ext) >= 5 and len(ext) >= max(5, int(w / 500))
        elif cid == "R08":
            ok = internal_links(text) >= 3
        elif cid == "Ept01":
            sp = path.parent / "schema.json"
            ok = False
            if sp.exists():
                for obj in json.loads(sp.read_text(encoding="utf-8")):
                    if obj.get("@type") == "BlogPosting" and obj.get("author", {}).get("name"):
                        ok = True
        elif cid == "O05":
            ok = (path.parent / "schema.json").exists()
        else:
            ok = bool(re.search(pattern, text, re.M | re.I))

        if ok:
            passes.append(cid)
        else:
            fails.append(f"{cid}: {label}")

    return {
        "folder": path.parent.name,
        "pass": len(fails) == 0,
        "score": f"{len(passes)}/{len(CHECKS)}",
        "fails": fails,
    }


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    total = 0
    fail_n = 0
    for pillar in targets:
        if not pillar.is_dir():
            continue
        print(f"\n{pillar.name}")
        print(f"{'Folder':<45} {'Score':>7}  OK")
        print("-" * 58)
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            r = audit_article(art)
            total += 1
            if not r["pass"]:
                fail_n += 1
            mark = "✓" if r["pass"] else "✗"
            print(f"{r['folder']:<45} {r['score']:>7}  {mark}")
            if r["fails"]:
                for f in r["fails"]:
                    print(f"    · {f}")
    print(f"\nTotal: {total} | EEAT quick pass: {total - fail_n} | Fail: {fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
