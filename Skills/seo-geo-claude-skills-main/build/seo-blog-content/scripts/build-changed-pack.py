#!/usr/bin/env python3
"""Package ONLY the keyword-realigned articles (this batch) for delivery.

Each article folder ships: article.md, meta-tags.html, head.html, schema.json, images/.
Plus a changed-articles manifest CSV + delivery note.
"""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
OUT = BLOG / "changed-articles-pack"
ARTS = OUT / "articles"

# Articles whose Target keyword was realigned to the plan in this batch.
CHANGED_IDS = [
    "010", "015", "016", "017", "018", "021", "025", "026", "030", "031",
    "051", "052", "060", "070", "071", "073", "082", "084", "089", "090", "095",
]
FILES = ("article.md", "meta-tags.html", "head.html", "schema.json")
IMG_GLOBS = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif", "*.svg")


def find_art(aid: str) -> Path | None:
    return next(iter(BLOG.glob(f"pillar*/{aid}-*/")), None)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    ARTS.mkdir(parents=True)

    # catalog lookup for metadata
    cat = {}
    cpath = BLOG / "frontend-package" / "blog-content-catalog.csv"
    if cpath.is_file():
        for r in csv.DictReader(cpath.open(encoding="utf-8-sig")):
            cat[r["文章编号"]] = r

    rows = []
    for aid in CHANGED_IDS:
        art = find_art(aid)
        if not art:
            continue
        dest = ARTS / art.name
        dest.mkdir(parents=True)
        for name in FILES:
            src = art / name
            if src.is_file():
                shutil.copy2(src, dest / name)
        imgdir = art / "images"
        if imgdir.is_dir():
            (dest / "images").mkdir()
            for pat in IMG_GLOBS:
                for img in imgdir.glob(pat):
                    shutil.copy2(img, dest / "images" / img.name)
        c = cat.get(aid, {})
        rows.append({
            "文章编号": aid,
            "slug": c.get("slug", art.name.split("-", 1)[-1]),
            "完整URL": (c.get("页面URL") or "").replace("/blog/", "https://infinisynapse.com/en/blog/") if c.get("页面URL", "").startswith("/blog/") else c.get("页面URL", ""),
            "英文标题": c.get("英文标题", ""),
            "新目标关键词": c.get("目标关键词", ""),
            "内容目录": f"articles/{art.name}",
            "部署文件": "article.md; meta-tags.html; head.html; schema.json; images/",
        })

    with (OUT / "changed-articles.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    note = f"""# 关键词对齐 · 变更文章交付包（{len(rows)} 篇）

> 本包仅含**本次修改关键词**的文章，不是全部 100 篇。

## 这次改了什么

按 SEO 规划文档把以下 {len(rows)} 篇的**主关键词替换为词库内有搜索量的关键词**，并同步更新了
正文 / 标题 / meta description / og / twitter / schema。**文章结构未变，仅替换关键词。**

## 怎么部署（覆盖更新这些页面即可）

对每篇（见 `changed-articles.csv`）：

1. `article.md`    → 重新渲染正文（已无 H1；页面 H1 用标题渲染）
2. `head.html`     → 替换该页 `<head>`（含新 canonical / 新 title(40-60) / 新 description(150-160) / og / twitter / JSON-LD）
3. `meta-tags.html`→ 同 head 内容的原始版（如不用 head.html 可用这个）
4. `schema.json`   → 更新 JSON-LD
5. `images/`       → 如有新图则上传

URL 不变（`https://infinisynapse.com/en/blog/{{slug}}`），只是页面内容与元数据更新。

## 清单

见 `changed-articles.csv`（文章编号 / slug / 完整URL / 新目标关键词 / 文件路径）。

## 部署后

这些页已在 sitemap 中，无需改 sitemap；可在 GSC 对这几条 URL「请求重新编入索引」加速更新。
"""
    (OUT / "README.md").write_text(note, encoding="utf-8")
    print(f"Built {OUT} with {len(rows)} articles")
    for r in rows:
        print(f"  {r['文章编号']} {r['新目标关键词']}")


if __name__ == "__main__":
    main()
