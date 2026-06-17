#!/usr/bin/env python3
"""Audit blog articles: >=5 external authority links, all HTTP 200.

External = markdown link URL whose host does not contain 'infinisynapse'.
"""
import re
import ssl
import sys
import urllib.request
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


def external_links(text: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for _, url in re.findall(r"\[([^\]]*)\]\((https?://[^)]+)\)", text):
        if "infinisynapse" in urlparse(url).netloc.lower():
            continue
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def check_url(url: str, retries: int = 3):
    ctx = ssl.create_default_context()
    last_err = ""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                return r.status
        except Exception as e:
            last_err = str(e)[:60]
            if attempt + 1 < retries:
                continue
    return last_err


def audit_pillar(pillar: Path) -> tuple[list[dict], list[tuple[str, str]]]:
    rows = []
    url_status = {}
    for article in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
        text = article.read_text(encoding="utf-8")
        links = external_links(text)
        rows.append(
            {
                "folder": article.parent.name,
                "count": len(links),
                "ok_count": len(links) >= 5,
                "links": links,
            }
        )
        for url in links:
            if url not in url_status:
                url_status[url] = check_url(url)
    bad_urls = [(u, s) for u, s in url_status.items() if s != 200]
    return rows, bad_urls


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    fail = 0
    all_bad = {}
    for pillar in targets:
        if not pillar.is_dir():
            print(f"SKIP {pillar}")
            continue
        rows, bad = audit_pillar(pillar)
        print(f"\n{pillar.name}")
        print(f"{'Folder':<45} {'Ext':>4}  OK")
        print("-" * 55)
        for r in rows:
            ok = r["ok_count"]
            if not ok:
                fail += 1
            print(f"{r['folder']:<45} {r['count']:>4}  {'✓' if ok else '✗'}")
        for u, s in bad:
            all_bad[u] = s
    if all_bad:
        print("\nURLs not HTTP 200:")
        for u, s in sorted(all_bad.items()):
            print(f"  {s} | {u}")
        fail += len(all_bad)
    total = sum(len(list(p.glob("[0-9][0-9][0-9]-*/article.md"))) for p in targets if p.is_dir())
    print(f"\nArticles checked: {total} | Link-count failures: {fail and 'see above' or 0}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
