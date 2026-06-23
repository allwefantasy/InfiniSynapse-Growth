#!/usr/bin/env python3
"""Build a lightweight, directly-sendable SEO-fix pack for the programmer.

Contains only what's needed to fix the live On-Page SEO red flags (canonical /
description / og / twitter / title) — docs + metadata + per-slug head snippets.
No images (already hosted), no full article bodies → a few MB, easy to send.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
OUT = BLOG / "seo-fix-pack"
HEAD_DIR = OUT / "head"
# Deploy/rule guides now live in the skill library (single source of truth)
SKILL_REF = BLOG.parent.parent / "Skills" / "seo-geo-claude-skills-main" / "build" / "seo-blog-content" / "references"

DOCS = ["PROGRAMMER-SEO-DEPLOY.md", "QUICKCREATOR-SEO-FIX.md"]
DATA = [
    "部署清单-完整URL.csv",
    "seo-meta.json",
    "quickcreator-seo-fields.csv",
    "blog-index-import-master.json",
    "blog-cms-import-100.csv",
]


def pillar_dirs() -> list[Path]:
    return sorted(p for p in BLOG.glob("pillar[1-8]-*") if p.is_dir() and " copy" not in p.name)


def slug_of(art_dir: Path) -> str:
    head = (art_dir / "head.html")
    if head.is_file():
        m = re.search(r"/en/blog/([^\"'<>]+)", head.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return art_dir.name.split("-", 1)[-1]


START = """# 先看这里 · SEO 修复包（直接发程序员）

线上博客页 On-Page SEO 报红：**Canonical / Meta Description / Social Media / Meta Title**。
实测原因：部署只注入了 `<title>` + `ld+json`，**没注入** canonical / description / og / twitter，
页面用了站点默认 `<head>`。内容本身没问题，是 `<head>` 注入不全。

## 三步修复

1. **读** `PROGRAMMER-SEO-DEPLOY.md`（完整说明 + 实测诊断表）。
2. **注入**：对每篇 `/en/blog/{slug}`，把 `head/{slug}.html` 整段插入页面 `<head>`。
   - 它已含 canonical + meta description(150–160) + og:* + twitter:* + JSON-LD，且 `<title>` 已是 40–60 字符。
   - 程序化做法：读 `seo-meta.json`（按 slug 取 `canonical / meta_description / og.* / twitter.* / title`）。
3. **验证**：`curl -s https://infinisynapse.com/en/blog/{slug} | grep -i canonical`，应能看到 canonical；
   再用 QuickCreator On-Page 复查，四项转绿。

## 文件清单

| 文件 | 用途 |
|---|---|
| `部署清单-完整URL.csv` | **按优先级排序的 100 篇部署清单**（完整 URL + 周次 + 状态 + head 片段） |
| `PROGRAMMER-SEO-DEPLOY.md` | 主文档（实测诊断 + 注入方案 + Next.js 示例） |
| `QUICKCREATOR-SEO-FIX.md` | 若用 QuickCreator 后台手填，逐字段对照 |
| `seo-meta.json` | 100 篇 SEO 元数据（按 slug，程序化注入用） |
| `quickcreator-seo-fields.csv` | 同上，CSV 逐字段（人工填用） |
| `blog-index-import-master.json` | 列表页数据（标题/摘要/分类/URL=/en/blog/slug） |
| `blog-cms-import-100.csv` | 列表数据 CSV 版 |
| `head/{slug}.html` | **每篇的 `<head>` 片段**（直接注入） |

## 注意

- URL 规范：`https://infinisynapse.com/en/blog/{slug}`（英文，无尾斜杠）。
- 页面 `<h1>` 用标题渲染，正文不要再放 `# H1`（避免双 H1）。
- 不要改 `head.html` 里的 URL / FAQ / canonical。
- 图片未包含在本包（已在线上 CDN）；如需原图见完整包 `frontend-package.zip`。
"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    HEAD_DIR.mkdir()

    for name in DOCS:
        src = SKILL_REF / name
        if src.is_file():
            shutil.copy2(src, OUT / name)
    for name in DATA:
        src = BLOG / name
        if src.is_file():
            shutil.copy2(src, OUT / name)

    n = 0
    for pillar in pillar_dirs():
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            head = art / "head.html"
            if not head.is_file():
                continue
            slug = slug_of(art)
            shutil.copy2(head, HEAD_DIR / f"{slug}.html")
            n += 1

    (OUT / "00-START-HERE.md").write_text(START, encoding="utf-8")
    print(f"Built {OUT}")
    print(f"  head snippets: {n}")
    print(f"  docs: {len([d for d in DOCS if (SKILL_REF/d).is_file()])}  data: {len([d for d in DATA if (BLOG/d).is_file()])}")


if __name__ == "__main__":
    main()
