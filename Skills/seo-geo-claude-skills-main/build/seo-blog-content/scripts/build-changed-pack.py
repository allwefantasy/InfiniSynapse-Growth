#!/usr/bin/env python3
"""Package selected hand-polished articles for CMS delivery.

Each article folder ships: article.md, article.publish.md, meta-tags.html,
head.html, schema.json, images/ (if present).
Plus changed-articles.csv + README + zip archive.
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import zipfile
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
OUT = BLOG / "changed-articles-pack"
ARTS = OUT / "articles"
PLAN = BLOG / "blog-vibe-coding-topics-plan.csv"
FILES = ("article.md", "meta-tags.html", "head.html", "schema.json")
IMG_GLOBS = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif", "*.svg")


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


def find_art(aid: str) -> Path | None:
    return next(iter(BLOG.glob(f"pillar*/{aid}-*/")), None)


def load_plan() -> dict[str, dict]:
    if not PLAN.is_file():
        return {}
    with PLAN.open(encoding="utf-8-sig") as f:
        return {r["编号"]: r for r in csv.DictReader(f)}


def read_slug(art: Path, plan_row: dict | None) -> str:
    text = (art / "article.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Slug\*\*:\s*`(?:/blog/)?([^`]+)`", text)
    if m:
        return m.group(1).strip("/")
    if plan_row:
        slug = plan_row["slug"].strip()
        kw = plan_row["关键词"].strip().lower()
        skip = {"prod system", "webhook relay service api data model", "database application programming interface"}
        if kw not in skip and not slug.endswith("-reddit"):
            return f"{slug}-reddit"
        return slug
    return art.name.split("-", 1)[-1]


def copy_article(art: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    md = (art / "article.md").read_text(encoding="utf-8")
    publish = strip_body_h1(md)
    (dest / "article.md").write_text(md, encoding="utf-8")
    (dest / "article.publish.md").write_text(publish, encoding="utf-8")
    (art / "article.publish.md").write_text(publish, encoding="utf-8")
    for name in FILES:
        if name == "article.md":
            continue
        src = art / name
        if src.is_file():
            shutil.copy2(src, dest / name)
    imgdir = art / "images"
    if imgdir.is_dir():
        (dest / "images").mkdir(exist_ok=True)
        for pat in IMG_GLOBS:
            for img in imgdir.glob(pat):
                shutil.copy2(img, dest / "images" / img.name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Package hand-polished articles for CMS delivery")
    parser.add_argument("ids", nargs="+", help="Article IDs, e.g. 220 273")
    parser.add_argument("--note", default="手改完成 · QuickCreator EEAT 优化", help="变更说明")
    args = parser.parse_args()

    plan = load_plan()
    if OUT.exists():
        shutil.rmtree(OUT)
    ARTS.mkdir(parents=True)

    rows = []
    for raw_id in args.ids:
        aid = raw_id.zfill(3) if raw_id.isdigit() else raw_id
        art = find_art(aid)
        if not art:
            print(f"WARN: {aid} not found")
            continue
        dest = ARTS / art.name
        copy_article(art, dest)
        prow = plan.get(aid, {})
        slug = read_slug(art, prow or None)
        rows.append({
            "文章编号": aid,
            "slug": slug,
            "完整URL": f"https://infinisynapse.com/en/blog/{slug}",
            "英文标题": prow.get("关键词", art.name.split("-", 1)[-1]),
            "pillar": prow.get("pillar_folder", ""),
            "变更说明": args.note,
            "内容目录": f"articles/{art.name}",
            "部署文件": "head.html + article.publish.md（正文）；meta-tags.html / schema.json 可选",
        })

    if not rows:
        print("No articles packaged.")
        return 1

    fields = list(rows[0].keys())
    with (OUT / "changed-articles.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    ids_str = "、".join(r["文章编号"] for r in rows)
    note = f"""# 手改文章交付包（{len(rows)} 篇）

> 文章编号：{ids_str}

## 部署步骤

对每篇（见 `changed-articles.csv`）：

1. **`head.html`** → 注入页面 `<head>`（修复 chrome-extension 内链需 CMS 全量重导）
2. **`article.publish.md`** → CMS 正文（无 H1）
3. **`images/`** → 上传 hero 图（若目录存在）
4. `meta-tags.html` / `schema.json` → 仅当 CMS 从源文件读 meta 时再覆盖

URL 不变（`https://infinisynapse.com/en/blog/{{slug}}`）。

## 清单

见 `changed-articles.csv`。
"""
    (OUT / "README.md").write_text(note, encoding="utf-8")

    zip_path = BLOG / "changed-articles-pack.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in OUT.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(BLOG))

    mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Built {OUT} with {len(rows)} articles -> {zip_path} ({mb:.2f} MB)")
    for r in rows:
        print(f"  {r['文章编号']} {r['slug']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
