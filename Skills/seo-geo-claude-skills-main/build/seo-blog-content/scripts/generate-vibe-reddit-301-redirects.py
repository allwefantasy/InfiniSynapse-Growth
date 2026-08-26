#!/usr/bin/env python3
"""Generate 301 redirect map for Reddit GEO slug changes (Pillar 16–20)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))
OUT = BLOG / "vibe-reddit-301-redirects.csv"
OUT_NGINX = BLOG / "vibe-reddit-301-redirects.nginx.conf"


def main() -> int:
    rows: list[dict[str, str]] = []
    for pillar in PILLARS:
        reg = pillar / "articles_registry.json"
        if not reg.is_file():
            continue
        data = json.loads(reg.read_text(encoding="utf-8"))
        for art in data.get("articles", []):
            new_slug = art["slug"]
            if not new_slug.endswith("-reddit"):
                continue
            old_slug = new_slug[: -len("-reddit")]
            rows.append(
                {
                    "id": art["id"],
                    "folder": art["folder"],
                    "pillar": pillar.name,
                    "keyword": art.get("keyword", ""),
                    "old_slug": old_slug,
                    "new_slug": new_slug,
                    "old_url_en": f"/en/blog/{old_slug}",
                    "new_url_en": f"/en/blog/{new_slug}",
                    "old_url_zh": f"/zh/blog/{old_slug}",
                    "new_url_zh": f"/zh/blog/{new_slug}",
                    "old_canonical": f"https://infinisynapse.com/en/blog/{old_slug}",
                    "new_canonical": f"https://infinisynapse.com/en/blog/{new_slug}",
                }
            )

    rows.sort(key=lambda r: int(r["id"]))
    fields = list(rows[0].keys()) if rows else []
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    nginx_lines = [
        "# Vibe Coding series (Pillar 16–20) Reddit GEO slug redirects",
        f"# Generated for {len(rows)} articles",
        "",
    ]
    for r in rows:
        nginx_lines.append(
            f"rewrite ^/en/blog/{r['old_slug']}$ {r['new_url_en']} permanent;"
        )
        nginx_lines.append(
            f"rewrite ^/zh/blog/{r['old_slug']}$ {r['new_url_zh']} permanent;"
        )
    OUT_NGINX.write_text("\n".join(nginx_lines) + "\n", encoding="utf-8")

    print(f"wrote {len(rows)} redirects -> {OUT.name}")
    print(f"nginx snippet -> {OUT_NGINX.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
