#!/usr/bin/env python3
"""Build programmer handoff pack for Pillar 21–25 (88 data-analysis articles)."""
from __future__ import annotations

import csv
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from article_keyword_meta import read_meta

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
OUT = BLOG / "p21-25-handoff-pack"
ARTS = OUT / "articles"
PILLARS = sorted(BLOG.glob("pillar2[1-5]-*"))

FILES = ("article.md", "meta-tags.html", "head.html", "schema.json")
IMG_GLOBS = ("*.png", "*.jpg", "*.jpeg", "*.webp")

HUB_FOLDERS = {
    "300-data-analysis-complete-guide",
    "317-python-data-analysis-guide",
    "334-data-analysis-tools-guide",
    "352-data-analyst-guide",
    "370-data-analyst-certification-guide",
}


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


def h1_title(art: Path) -> str:
    for line in art.joinpath("article.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return art.name


def deploy_slug(art: Path) -> str:
    meta = read_meta(art / "article.md")
    slug = meta.get("slug", "")
    if slug.startswith("/blog/"):
        return slug.split("/blog/", 1)[1]
    if slug.startswith("/en/blog/"):
        return slug.split("/en/blog/", 1)[1]
    head = art / "head.html"
    if head.is_file():
        m = re.search(r"/en/blog/([^\"'<>]+)", head.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    meta_html = art / "meta-tags.html"
    if meta_html.is_file():
        m = re.search(
            r'canonical" href="https://infinisynapse\.com/en/blog/([^"]+)"',
            meta_html.read_text(encoding="utf-8"),
        )
        if m:
            return m.group(1)
    return art.name.split("-", 1)[-1]


def copy_article(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        f = src / name
        if f.is_file():
            shutil.copy2(f, dest / name)
    md = src / "article.md"
    if md.is_file():
        body = strip_body_h1(md.read_text(encoding="utf-8"))
        (dest / "article.publish.md").write_text(body, encoding="utf-8")
    imgdir = src / "images"
    if imgdir.is_dir():
        (dest / "images").mkdir(exist_ok=True)
        for pat in IMG_GLOBS:
            for img in imgdir.glob(pat):
                shutil.copy2(img, dest / "images" / img.name)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    ARTS.mkdir(parents=True)

    rows: list[dict] = []
    seo_subset: list[dict] = []

    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            if not (art / "article.md").is_file():
                continue
            aid = art.name.split("-")[0]
            slug = deploy_slug(art)
            meta = read_meta(art / "article.md")
            dest = ARTS / pillar.name / art.name
            copy_article(art, dest)

            is_hub = art.name in HUB_FOLDERS
            title = h1_title(art)
            url = f"https://infinisynapse.com/en/blog/{slug}"

            rows.append({
                "文章编号": aid,
                "slug": slug,
                "完整URL": url,
                "英文标题": title,
                "目标关键词": meta.get("target_keyword", ""),
                "支柱": pillar.name,
                "类型": "Hub" if is_hub else "Cluster",
                "变更类型": "新发文章",
                "源目录": f"{pillar.name}/{art.name}",
                "交付目录": f"articles/{pillar.name}/{art.name}",
                "部署文件": "article.publish.md; head.html; meta-tags.html; schema.json; images/",
            })

            if (art / "head.html").is_file():
                seo_subset.append({
                    "id": aid,
                    "folder": art.name,
                    "pillar": pillar.name,
                    "slug": slug,
                    "url": url,
                    "title": title,
                    "target_keyword": meta.get("target_keyword", ""),
                })

    with (OUT / "deploy-manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    (OUT / "seo-meta-p21-25.json").write_text(
        json.dumps({"count": len(seo_subset), "articles": seo_subset}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )

    for name in ("sitemap.xml", "pillar21-25-topic-cluster-architecture_20260708.md"):
        src = BLOG / name
        if src.is_file():
            shutil.copy2(src, OUT / name)

    readme = f"""# Pillar 21–25 · 数据分析集群 · 程序员交付包（{len(rows)} 篇）

新发 **88 篇** SEO 博客（Pillar 21–25，编号 300–387）。包内已含更新后的 **`sitemap.xml`**（在现有线上 sitemap 基础上合并本批次 URL）。

## 包内结构

```
p21-25-handoff-pack/
├── README.md
├── deploy-manifest.csv              ← 88 篇部署清单
├── seo-meta-p21-25.json             ← slug / URL / 标题索引
├── sitemap.xml                      ← 全站 sitemap（含新文章，替换线上）
├── pillar21-25-topic-cluster-architecture_20260708.md
└── articles/
    └── pillar{{21-25}}-{{theme}}/
        └── {{编号}}-{{slug}}/
            ├── article.md             ← 源稿（含 H1，对照用）
            ├── article.publish.md     ← 发布正文（已去 H1）
            ├── head.html              ← 注入 <head>（canonical/og/twitter/JSON-LD）
            ├── meta-tags.html
            ├── schema.json
            └── images/                ← hero + og-cover + 正文数据表图
```

## Hub 页（priority 0.9）

| 编号 | slug |
|------|------|
| 300 | data-analysis-complete-guide |
| 317 | python-data-analysis-guide |
| 334 | data-analysis-tools-guide |
| 352 | data-analyst-guide |
| 370 | data-analyst-certification-guide |

## 部署步骤

1. **`deploy-manifest.csv`** — 按 `完整URL` 在 CMS 创建 88 个新路由。
2. **正文** — 使用 `article.publish.md`（无 H1）；页面 H1 = CMS 标题 = manifest `英文标题`。
3. **`head.html`** — 整段注入页面 `<head>`（canonical、description、og、twitter、JSON-LD）。
4. **`images/`** — 上传 hero（`hero-*.png` 1200×630）及正文表图（`table-*.png`）。
5. **`sitemap.xml`** — 替换 `https://infinisynapse.com/sitemap.xml`（全量 {len(rows)} 篇新 URL 已合并）。
6. GSC → Sitemaps → 重新提交 sitemap URL。

## URL 规范

- Canonical：`https://infinisynapse.com/en/blog/{{slug}}`（无尾斜杠）
- Locale：仅 `/en/blog/`（`/zh/blog/` 未上线则不收录）

## 验证

```bash
curl -sI "https://infinisynapse.com/en/blog/data-analysis-complete-guide" | head -5
curl -s "https://infinisynapse.com/en/blog/data-analysis-complete-guide" | grep -i canonical
```
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    zip_path = BLOG / "p21-25-handoff-pack.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in OUT.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(BLOG))

    mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Built {len(rows)} articles -> {OUT}")
    print(f"Zip: {zip_path} ({mb:.1f} MB)")


if __name__ == "__main__":
    main()
