#!/usr/bin/env python3
"""Build vibe-coding-handoff-pack for articles 203-299."""
from __future__ import annotations

import csv
import re
import shutil
import zipfile
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
OUT = BLOG / "vibe-coding-handoff-pack"
ARTS = OUT / "articles"
PLAN = BLOG / "blog-vibe-coding-topics-plan.csv"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))

FILES = ("article.md", "meta-tags.html", "head.html", "schema.json")
IMG_GLOBS = ("*.png", "*.jpg", "*.jpeg", "*.webp")


def strip_body_h1(md: str) -> str:
    lines = md.splitlines(keepends=True)
    in_fence = False
    for i, raw in enumerate(lines):
        line = raw.rstrip("\n")
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^#{2,6}\s", line):
            return md
        if re.match(r"^#\s+\S", line):
            del lines[i]
            if i < len(lines) and lines[i].strip() == "":
                del lines[i]
            return "".join(lines)
    return md


SKIP_REDDIT = {
    "prod system",
    "webhook relay service api data model",
    "database application programming interface",
}


def deploy_slug(row: dict) -> str:
    s = row["slug"].strip()
    kw = row["关键词"].strip().lower()
    if kw in SKIP_REDDIT:
        return s
    return s if s.endswith("-reddit") else f"{s}-reddit"


def read_article_slug(art_dir: Path) -> str:
    text = (art_dir / "article.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Slug\*\*:\s*`(?:/blog/)?([^`]+)`", text)
    return m.group(1).strip("/") if m else ""


def read_article_keyword(art_dir: Path, fallback: str) -> str:
    text = (art_dir / "article.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).strip() if m else fallback


def load_plan() -> list[dict]:
    with PLAN.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    ARTS.mkdir(parents=True)

    rows: list[dict] = []
    for row in load_plan():
        aid = row["编号"]
        slug = row["slug"]
        pillar = row["pillar_folder"]
        src = BLOG / pillar / f"{aid}-{slug}"
        if not (src / "article.md").is_file():
            continue
        dest = ARTS / pillar / f"{aid}-{slug}"
        dest.mkdir(parents=True, exist_ok=True)
        for name in FILES:
            f = src / name
            if f.is_file():
                if name == "article.md":
                    body = strip_body_h1(f.read_text(encoding="utf-8"))
                    (dest / "article.publish.md").write_text(body, encoding="utf-8")
                    (dest / name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
                else:
                    shutil.copy2(f, dest / name)
        imgdir = src / "images"
        if imgdir.is_dir():
            (dest / "images").mkdir(exist_ok=True)
            for pat in IMG_GLOBS:
                for img in imgdir.glob(pat):
                    shutil.copy2(img, dest / "images" / img.name)

        live_slug = read_article_slug(src) or deploy_slug(row)
        live_kw = read_article_keyword(src, row["关键词"])

        rows.append(
            {
                "id": aid,
                "slug": live_slug,
                "url": f"https://infinisynapse.com/en/blog/{live_slug}",
                "keyword": live_kw,
                "pillar": pillar,
                "priority": row.get("优先级", ""),
                "is_hub": "Hub" in row.get("备注", ""),
                "path": f"articles/{pillar}/{aid}-{slug}",
            }
        )

    for name in ("blog-index-import-master.json", "sitemap.xml", "blog-vibe-coding-topics-plan.csv"):
        src = BLOG / name
        if src.is_file():
            shutil.copy2(src, OUT / name)

    for name in ("vibe-reddit-301-redirects.csv", "vibe-reddit-301-redirects.nginx.conf"):
        src = BLOG / name
        if src.is_file():
            shutil.copy2(src, OUT / name)

    with (OUT / "deploy-manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    readme = """# Vibe Coding SEO · 97 Articles Handoff Pack

Complete series from `Skills/seo-geo-claude-skills-main/build/seo-blog-content/references/seo_pillar_strategy_vibe_coding_api.md`.

## Deploy

1. Use `deploy-manifest.csv` for URL → folder mapping.
2. **CMS title** = H1 from source `article.md`; **body** = `article.publish.md` (no H1).
3. Inject `head.html` into page `<head>`.
4. Upload hero images from `images/` (`hero-{slug}.png`, 1200×630).
5. Replace site `sitemap.xml` and merge `blog-index-import-master.json` posts.
6. Deploy `vibe-reddit-301-redirects.nginx.conf` (or CMS equivalent) for 94 legacy URLs.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    zip_path = BLOG / "vibe-coding-handoff-pack.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in OUT.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(BLOG))

    mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Built {len(rows)} articles -> {zip_path} ({mb:.1f} MB)")


if __name__ == "__main__":
    main()
