#!/usr/bin/env python3
"""Build programmer handoff pack: each pillar's Hub article IS the landing page.

Do NOT deploy /en/blog/pillar/{slug} routes. Use existing /en/blog/{hub-slug} URLs.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BLOG = ROOT / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
OUT = BLOG / "hub-landing-handoff-pack"
ARTS = OUT / "articles"
SITE = "https://infinisynapse.com"

_spec = importlib.util.spec_from_file_location("reg", SCRIPTS / "cluster-link-registry.py")
reg = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(reg)

FILES = ("article.md", "meta-tags.html", "head.html", "schema.json", "preview.html")
IMG_GLOBS = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif", "*.svg")

# Deprecated /en/blog/pillar/* routes → correct hub URL (301 if already deployed)
DEPRECATED_PILLAR_LANDING_SLUGS: dict[str, str] = {
    "ai-native-data-analysis": "ai-for-data-analysis",
    "data-agent-vs-alternatives": "code-agent-vs-data-agent",
    "ai-analyst-tools": "best-ai-tools-for-data-analysis",
    "data-source-connectors": "connect-supabase-to-ai-data-analyst",
    "nl2sql-text-to-sql": "natural-language-to-sql",
    "ai-excel-csv-spreadsheet": "clean-excel-data-with-ai",
    "use-cases-by-role": "ai-tools-for-data-analysts",
    "skills-templates-glossary": "data-agent-faq",
    "semantic-layer": "semantic-layer",
    "mcp-data-access": "mcp-for-data-analysis",
    "agentic-analytics": "agentic-analytics",
    "data-trends": "what-are-data-trends",
    "data-privacy-security": "data-security-compliance",
    "enterprise-data": "enterprise-data-security-solutions",
    "data-search": "public-data",
}


def meta_field(pat: str, text: str) -> str:
    m = re.search(pat, text)
    return (m.group(1) if m else "").replace("&quot;", '"').strip()


def slug_from_meta(meta: str) -> str:
    s = meta_field(r'<link rel="canonical" href="https://infinisynapse\.com/en/blog/([^"]+)"', meta)
    if s:
        return s
    return meta_field(r'<link rel="canonical" href="https://infinisynapse\.cn/blog/([^"]+)"', meta)


def copy_article(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        f = src / name
        if not f.is_file():
            continue
        if name == "article.md":
            text = f.read_text(encoding="utf-8")
            # Deploy body: no H1 (page H1 = CMS title)
            lines = text.splitlines(keepends=True)
            for i, raw in enumerate(lines):
                line = raw.rstrip("\n")
                if re.match(r"^#\s+\S", line) and not re.match(r"^#{2,}\s", line):
                    del lines[i]
                    if i < len(lines) and lines[i].strip() == "":
                        del lines[i]
                    text = "".join(lines)
                    break
            (dest / name).write_text(text, encoding="utf-8")
        else:
            shutil.copy2(f, dest / name)
    imgdir = src / "images"
    if imgdir.is_dir():
        (dest / "images").mkdir(exist_ok=True)
        for pat in IMG_GLOBS:
            for img in imgdir.glob(pat):
                shutil.copy2(img, dest / "images" / img.name)


def hub_records() -> list[dict]:
    blog = json.loads((BLOG / "blog-index-import-master.json").read_text(encoding="utf-8"))
    by_slug = {p["slug"]: p for p in blog["posts"]}
    rows: list[dict] = []
    for pillar_dir in reg.PILLAR_DIRS:
        hub_folder = reg.PRIMARY_HUB[pillar_dir.name]
        hub_slug = reg.slug_from_folder(hub_folder)
        art_dir = pillar_dir / hub_folder
        if not (art_dir / "article.md").is_file():
            raise SystemExit(f"Missing hub article: {art_dir}")
        post = by_slug.get(hub_slug, {})
        cluster_posts = [p for p in blog["posts"] if p.get("pillar_cluster") == pillar_dir.name]
        meta_path = art_dir / "meta-tags.html"
        meta = meta_path.read_text(encoding="utf-8") if meta_path.is_file() else ""
        canonical = meta_field(r'<link rel="canonical" href="([^"]+)"', meta) or f"{SITE}/en/blog/{hub_slug}"
        rows.append(
            {
                "pillar_num": int(re.search(r"pillar(\d+)", pillar_dir.name).group(1)),  # type: ignore[union-attr]
                "pillar_dir": pillar_dir.name,
                "hub_folder": hub_folder,
                "hub_slug": hub_slug,
                "hub_title": post.get("title") or reg.slug_titles_from_index().get(hub_slug, hub_slug),
                "landing_url": canonical,
                "url_path": f"/en/blog/{hub_slug}",
                "article_count": len(cluster_posts),
                "cluster_count_excluding_hub": max(0, len(cluster_posts) - 1),
                "meta_title": meta_field(r"<title>([^<]+)</title>", meta),
                "meta_description": meta_field(r'<meta name="description" content="([^"]+)"', meta),
                "source_path": f"SEO/Blog/{pillar_dir.name}/{hub_folder}",
                "delivery_path": f"articles/{pillar_dir.name}/{hub_folder}",
            }
        )
    return sorted(rows, key=lambda r: r["pillar_num"])


def cluster_json(pillar_dir: str, hub_slug: str, posts: list[dict]) -> list[dict]:
    cluster = [p for p in posts if p.get("pillar_cluster") == pillar_dir]
    cluster.sort(key=lambda p: (-p.get("sort_priority", 0), p.get("slug", "")))
    return [
        {
            "slug": p["slug"],
            "title": p["title"],
            "excerpt": p.get("excerpt", ""),
            "url": p.get("url", f"/blog/{p['slug']}"),
            "card_tag": p.get("card_tag", ""),
            "display_date": p.get("display_date", ""),
            "hero_image": p.get("hero_image", ""),
            "is_hub": p["slug"] == hub_slug,
        }
        for p in cluster
    ]


def qc_row(rec: dict, meta: str) -> dict:
    slug = rec["hub_slug"]
    url = rec["landing_url"]
    return {
        "hub_slug": slug,
        "page_url": url,
        "meta_title": rec["meta_title"],
        "meta_description": rec["meta_description"],
        "canonical_url": url,
        "og_title": meta_field(r'<meta property="og:title" content="([^"]+)"', meta),
        "og_description": meta_field(r'<meta property="og:description" content="([^"]+)"', meta),
        "og_image": meta_field(r'<meta property="og:image" content="([^"]+)"', meta),
        "twitter_title": meta_field(r'<meta name="twitter:title" content="([^"]+)"', meta),
        "twitter_description": meta_field(r'<meta name="twitter:description" content="([^"]+)"', meta),
        "twitter_image": meta_field(r'<meta name="twitter:image" content="([^"]+)"', meta),
        "badge_label": f"{rec['article_count']} GUIDES",
        "qc_notes": "Hub article = pillar landing page. Render FULL article.md body (2000+ word Ultimate Guide). Inject head.html. Card grid is optional supplement only.",
    }


def annotate_blog_index(hub_slugs: set[str]) -> dict:
    data = json.loads((BLOG / "blog-index-import-master.json").read_text(encoding="utf-8"))
    for post in data["posts"]:
        slug = post.get("slug", "")
        if slug in hub_slugs:
            post["is_pillar_hub_landing"] = True
            post["pillar_landing_url"] = post.get("url", f"/blog/{slug}")
        else:
            post["is_pillar_hub_landing"] = False
    data["_hub_landing_note"] = (
        "Each pillar's landing page is its Hub article (is_pillar_hub_landing=true). "
        "Do NOT use /en/blog/pillar/* routes."
    )
    return data


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    ARTS.mkdir(parents=True)

    records = hub_records()
    hub_slugs = {r["hub_slug"] for r in records}
    blog_posts = json.loads((BLOG / "blog-index-import-master.json").read_text(encoding="utf-8"))["posts"]
    qc_rows: list[dict] = []

    for rec in records:
        src = BLOG / rec["pillar_dir"] / rec["hub_folder"]
        dest = ARTS / rec["pillar_dir"] / rec["hub_folder"]
        copy_article(src, dest)
        cluster = cluster_json(rec["pillar_dir"], rec["hub_slug"], blog_posts)
        (dest / "cluster-articles.json").write_text(
            json.dumps(cluster, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        meta = (src / "meta-tags.html").read_text(encoding="utf-8")
        qc_rows.append(qc_row(rec, meta))

    # Manifest
    manifest_fields = [
        "pillar_num", "pillar_dir", "hub_slug", "hub_title", "landing_url",
        "article_count", "source_path", "delivery_path",
    ]
    with (OUT / "hub-landing-manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=manifest_fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(records)

    # 301 redirect table for wrongly deployed /pillar/* routes
    redirect_rows = [
        {
            "deprecated_url": f"{SITE}/en/blog/pillar/{old}",
            "redirect_to": f"{SITE}/en/blog/{hub}",
            "status": "301",
        }
        for old, hub in DEPRECATED_PILLAR_LANDING_SLUGS.items()
    ]
    with (OUT / "redirect-deprecated-pillar-routes.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["deprecated_url", "redirect_to", "status"])
        w.writeheader()
        w.writerows(redirect_rows)

    master = {
        "_comment": "Pillar landing page = Hub article at /en/blog/{hub_slug}. No /en/blog/pillar/* routes.",
        "_generated_by": "build-hub-landing-handoff-pack.py",
        "_generated_at": datetime.now().isoformat(timespec="seconds"),
        "hub_count": len(records),
        "hubs": records,
    }
    (OUT / "hub-landing-pages-master.json").write_text(
        json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    qc_fields = list(qc_rows[0].keys())
    with (OUT / "quickcreator-hub-landing-seo-fields.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=qc_fields)
        w.writeheader()
        w.writerows(qc_rows)

    blog_index = annotate_blog_index(hub_slugs)
    (OUT / "blog-index-import-master.json").write_text(
        json.dumps(blog_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Regenerate sitemap (227 URLs, no /pillar/*)
    subprocess.run([sys.executable, str(SCRIPTS / "build-sitemap.py")], check=True, cwd=ROOT)
    shutil.copy2(BLOG / "sitemap.xml", OUT / "sitemap.xml")

    readme = f"""# Pillar 落地页 · Hub 即落地页（15 篇 Hub 长文）

> **核心规则**：每个 Pillar 的**落地页 = 该集群的 Hub 长文**，URL 为 `/en/blog/{{hub_slug}}`。  
> **禁止**新建或保留 `/en/blog/pillar/{{slug}}` 路由。

## 为什么不用 /blog/pillar/*？

Hub 长文本身已是 Pillar Page：含完整正文、`## Cluster guides in this pillar` 表格、FAQ、内链全集群。  
单独做 `/blog/pillar/*` 会与 Hub URL **重复主题、分散权重**，且造成 QuickCreator SEO 字段重复维护。

## 15 个 Hub 落地页

| Pillar | Hub slug | 落地 URL |
|--------|----------|----------|
"""
    for r in records:
        readme += f"| P{r['pillar_num']} | `{r['hub_slug']}` | {r['landing_url']} |\n"

    readme += """
## 包内结构

```
hub-landing-handoff-pack/
├── README.md
├── DEPLOY-RULES.md
├── hub-landing-manifest.csv           ← 15 Hub 对照表
├── hub-landing-pages-master.json      ← 前端 import（博客分类 → Hub URL）
├── redirect-deprecated-pillar-routes.csv  ← 若已上线 /pillar/*，301 到 Hub
├── quickcreator-hub-landing-seo-fields.csv
├── blog-index-import-master.json      ← posts 含 is_pillar_hub_landing 标记
├── sitemap.xml                        ← 227 URL（无 /pillar/*）
└── articles/{pillar}/{hub-folder}/    ← Hub 文章交付包
```

## 程序员必做

1. **删除或 301** 所有 `/en/blog/pillar/*` 路由 → 见 `redirect-deprecated-pillar-routes.csv`
2. **博客列表 / 分类入口** 链到 `hub-landing-pages-master.json` 中的 `landing_url`（不是 /pillar/*）
3. **Hub 页面** 按普通博客详情页部署：**完整** `article.md` 正文（2000+ 词终极指南）+ `head.html`；`cluster-articles.json` 仅作可选卡片补充（**禁止**用卡片替代正文）
4. **徽章文案** 用 `{N} GUIDES`，不要显示 Pillar 编号（06、14 等）
5. **Sitemap** 用包内 `sitemap.xml` 整体替换线上（**不含** /pillar/* URL）
6. **QuickCreator SEO** 对 15 个 Hub 填 `quickcreator-hub-landing-seo-fields.csv`

## 与 Cluster 文章关系

- **Hub** = 落地页 + 深度总览（本包 15 篇）
- **Cluster** = 同文件夹下其余文章，正文须链回 Hub
- Hub 文末 **Cluster guides** 表格已索引全部 Cluster（无部署序号）

## 验收

```bash
# 不应存在 200
curl -sI "https://infinisynapse.com/en/blog/pillar/enterprise-data" | head -1

# Hub 落地页应 200 + canonical
curl -s "https://infinisynapse.com/en/blog/enterprise-data-security-solutions" | grep canonical
```

- [ ] 15 个 Hub URL 均可访问
- [ ] 无 `/en/blog/pillar/*` 索引 URL（或已 301）
- [ ] sitemap 中 Hub slug priority=0.9
- [ ] 列表页分类指向 Hub URL
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    rules = """# 部署规则 · Hub 即 Pillar 落地页

## URL 模型

| 类型 | URL 模式 | 示例 |
|------|----------|------|
| 博客列表 | `/en/blog` | 全站博客入口 |
| **Pillar 落地页（Hub）** | `/en/blog/{hub-slug}` | `/en/blog/enterprise-data-security-solutions` |
| Cluster 文章 | `/en/blog/{slug}` | `/en/blog/enterprise-data-governance` |
| ~~错误~~ | ~~`/en/blog/pillar/{slug}`~~ | **不要部署** |

## 正文 = 终极指南（硬规则）

Hub 页面**不是**文章列表页。每篇 Hub 是一篇**完整、自成体系、高信息密度**的长文（类比《项目管理终极指南（2026版）》），读者打开即可读完整个主题，无需先点卡片。

| 模块 | 要求 |
|------|------|
| **体量** | 正文 **2000–2800 词**（目标 2300+）；20–30 个 H2/H3/H4 |
| **定义** | TL;DR + Key Definition + 2026 语境 |
| **核心框架** | 4–6 个支柱/阶段/方法 + **≥1 表格或架构图** |
| **方法论对比** | 对比表 + 叙事句内链到 Cluster（如 Code Agent vs Data Agent） |
| **工具 landscape** | 分 tier 叙述 + 内链到测评/选型 Cluster 文 |
| **实施路径** | 分阶段 roadmap 或 numbered workflow |
| **案例/证据** | 生产模式、可 replay 指标 |
| **索引** | `## Cluster guides in this pillar` 表格（标题无 001/002 前缀） |
| **FAQ** | ≥4 问，与 schema.json 一致 |

**禁止**：仅用 `cluster-articles.json` 卡片网格替代 `article.md` 正文；禁止薄索引页 UI。

内容框架详见仓库内 `pillar-hub-ultimate-guide-framework.md`；发布前跑 `generate-pillar-hub-checklist.py` 对照 `pillar-hub-section-checklist.csv`。

## 前端：分类 / 专题入口

从 `hub-landing-pages-master.json` 读取：

```ts
import hubs from './hub-landing-pages-master.json';
// hubs.hubs[].landing_url  →  pillar 分类「查看全部」链接
// hubs.hubs[].hub_title    →  落地页标题（与 Hub H1 一致）
```

或从 `blog-index-import-master.json`：

```ts
posts.filter(p => p.is_pillar_hub_landing)
```

## Hub 页面 UI（渲染顺序）

1. **H1** = Hub 文章标题（来自 meta / CMS 标题）
2. **Hero 图** + **完整正文** = 渲染 `article.md` 全部 Markdown（TL;DR → 框架 → 对比 → 工具 → 案例 → Scorecard → 失败模式 → Cluster 表格 → FAQ → Conclusion）
3. **可选补充**：`cluster-articles.json` 卡片网格放在正文**之后**（与表格互补，**非替代**）
4. **徽章**：`{article_count} GUIDES`，无 Pillar 内部编号（06、14 等）

## SEO

- 使用 Hub 文章已有 `head.html`（canonical、description、og、JSON-LD BlogPosting）
- QuickCreator：按 `quickcreator-hub-landing-seo-fields.csv` 填 15 个 Hub 页
- Sitemap：Hub URL 已含在 `sitemap.xml`，priority **0.9**

## 若已错误上线 /en/blog/pillar/*

按 `redirect-deprecated-pillar-routes.csv` 配置 **301** 到对应 Hub URL，并从 sitemap 移除 /pillar/*。

## 验收（内容 + 技术）

- [ ] 页面首屏可见 TL;DR 与正文段落（非仅卡片）
- [ ] 正文词数 ≥2000（可用 checklist CSV 核对）
- [ ] 含方法论对比段 + Cluster guides 表格
- [ ] canonical / og / twitter 来自 head.html
"""
    (OUT / "DEPLOY-RULES.md").write_text(rules, encoding="utf-8")

    # Deprecate old pack
    old_pack = BLOG / "pillar-landing-handoff-pack"
    if old_pack.is_dir():
        (old_pack / "DEPRECATED.md").write_text(
            "# DEPRECATED\n\n"
            "Pillar 落地页应使用 **Hub 长文**（`/en/blog/{hub-slug}`），不是 `/en/blog/pillar/*`。\n\n"
            "请改用：`SEO/Blog/hub-landing-handoff-pack.zip`\n\n"
            "生成：`python3 Skills/.../build-hub-landing-handoff-pack.py`\n",
            encoding="utf-8",
        )

    zip_path = OUT.with_suffix(".zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in OUT.rglob("*"):
            if path.is_file() and path.suffix != ".zip":
                zf.write(path, path.relative_to(OUT.parent))

    print(f"Wrote {len(records)} hub landing pages -> {OUT}")
    print(f"Zip -> {zip_path}")
    locs = sum(1 for _ in open(BLOG / "sitemap.xml"))
    print(f"Sitemap URLs (approx lines): {locs // 6}")


if __name__ == "__main__":
    main()
