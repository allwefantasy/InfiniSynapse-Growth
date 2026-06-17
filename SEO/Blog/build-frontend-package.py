#!/usr/bin/env python3
"""Build SEO/Blog/frontend-package/ — clean handoff for frontend (no SEO-only files)."""
from __future__ import annotations

import csv
import json
import re
import shutil
from pathlib import Path

BLOG = Path(__file__).parent
OUT = BLOG / "frontend-package"
ARTICLES = OUT / "articles"

DEPLOY_FILES = ("article.md", "meta-tags.html", "schema.json")
IMAGE_GLOBS = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif", "*.svg")

PILLAR_ZH = {
    1: "AI原生数据分析",
    2: "数据智能体对比",
    3: "AI分析师工具",
    4: "数据源连接教程",
    5: "自然语言转SQL",
    6: "Excel与CSV",
    7: "角色与行业场景",
    8: "模板与评测",
}

UI_MODULE_ZH = {
    "long-form-guide": "长文指南",
    "how-to-steps": "分步教程",
    "versus-scorecard": "对比打分表",
    "use-case-persona": "场景/角色页",
    "tool-listicle": "工具排行榜",
    "alternatives-matrix": "替代品对比表",
    "definition-box": "定义科普框",
    "glossary-terms": "术语表",
    "prompt-resource": "Prompt模板",
    "copy-block": "可复制文本块",
    "product-review": "产品评测",
    "faq-hub": "FAQ专题",
}

FILTER_ZH = {
    "knowledge": "知识科普",
    "comparisons": "对比与替代",
    "tools_reviews": "工具与评测",
    "deep_dive": "技术深度",
    "tutorials": "教程实操",
    "connectors": "数据连接与集成",
    "use_cases": "角色与行业场景",
    "excel_csv": "Excel与表格AI",
    "nl2sql": "自然语言转SQL",
}


def pillar_dirs() -> list[Path]:
    return sorted(p for p in BLOG.glob("pillar[1-8]-*") if p.is_dir() and " copy" not in p.name)


def load_master_posts() -> list[dict]:
    data = json.loads((BLOG / "blog-index-import-master.json").read_text(encoding="utf-8"))
    return data["posts"]


def load_deploy_meta() -> dict[str, dict]:
    """slug -> deploy row from pillar-sorted handoff CSV."""
    path = BLOG / "blog-deploy-order-90d-zh.csv"
    if not path.is_file():
        return {}
    out = {}
    for row in csv.DictReader(path.open(encoding="utf-8-sig")):
        slug = row.get("slug", "").strip()
        if slug and slug != "TBD-case-study":
            out[slug] = row
    return out


def find_hero_image(art_dir: Path) -> str:
    img_dir = art_dir / "images"
    if not img_dir.is_dir():
        return ""
    for pattern in ("hero*.png", "hero*.jpg", "og-cover.png", "*.png"):
        hits = sorted(img_dir.glob(pattern))
        if hits:
            return hits[0].name
    return ""


def copy_article(art_dir: Path, dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    for name in DEPLOY_FILES:
        src = art_dir / name
        if src.is_file():
            shutil.copy2(src, dest / name)
    img_dest = dest / "images"
    n = 0
    img_dir = art_dir / "images"
    if img_dir.is_dir():
        img_dest.mkdir(exist_ok=True)
        for pattern in IMAGE_GLOBS:
            for img in img_dir.glob(pattern):
                shutil.copy2(img, img_dest / img.name)
                n += 1
    return n


def build_catalog_row(
    deploy_order: int,
    post: dict,
    folder: str,
    rel_path: str,
    hero_file: str,
    image_count: int,
    deploy: dict,
) -> dict:
    pnum = int(post.get("pillar_num") or 0)
    slug = post["slug"]
    return {
        "部署序号": deploy_order,
        "文章编号": folder[:3],
        "slug": slug,
        "页面URL": post["url"],
        "英文标题": post["title"],
        "列表摘要": post.get("excerpt", ""),
        "目标关键词": post.get("target_keyword", ""),
        "支柱编号": pnum,
        "支柱名称": PILLAR_ZH.get(pnum, ""),
        "内容类型": post.get("content_type", ""),
        "详情页组件": post.get("ui_module", ""),
        "详情页组件说明": UI_MODULE_ZH.get(post.get("ui_module", ""), ""),
        "列表分类": post.get("filter_category", ""),
        "列表分类说明": FILTER_ZH.get(post.get("filter_category", ""), ""),
        "列表标签": post.get("card_tag", ""),
        "列表排序权重": post.get("sort_priority", ""),
        "计划周次": deploy.get("周次", ""),
        "部署动作": deploy.get("部署动作", "待发文章"),
        "内容目录": rel_path,
        "正文文件": f"{rel_path}/article.md",
        "页面头信息": f"{rel_path}/meta-tags.html",
        "结构化数据": f"{rel_path}/schema.json",
        "图片目录": f"{rel_path}/images/",
        "封面图文件": f"{rel_path}/images/{hero_file}" if hero_file else "",
        "图片数量": image_count,
        "备注": deploy.get("备注", ""),
    }


def build_list_row(post: dict, folder: str, rel_path: str, hero_file: str) -> dict:
    pnum = int(post.get("pillar_num") or 0)
    return {
        "slug": post["slug"],
        "url": post["url"],
        "title": post["title"],
        "excerpt": post.get("excerpt", ""),
        "card_tag": post.get("card_tag", ""),
        "filter_category": post.get("filter_category", ""),
        "ui_module": post.get("ui_module", ""),
        "sort_priority": post.get("sort_priority", ""),
        "pillar_num": pnum,
        "content_path": rel_path,
        "hero_filename": hero_file,
    }


def write_readme(article_count: int, image_count: int) -> str:
    return f"""# InfiniSynapse 博客 · 前端集成包

> 共 **{article_count}** 篇文章 · **{image_count}** 张图片 · 可直接 zip 发给前端  
> 生成目录：`SEO/Blog/frontend-package/`

---

## 1. 这个包里有什么

| 文件/目录 | 用途 |
|-----------|------|
| **`集成手册.md`** | 怎么接路由、怎么拼页面（先看这个） |
| **`blog-content-catalog.csv`** | **100 篇内容总目录**（路径、slug、组件类型、部署顺序） |
| **`blog-nav-tags.csv`** | **Blog 页筛选标签**（导航 pill + 篇数，见 `show_in_nav` 列） |
| **`blog-list.csv`** | 列表页 `/blog` 卡片数据（精简版） |
| **`blog-list.json`** | 同上，JSON 格式 |
| **`articles/`** | 每篇文章的发布文件 |

**本包 intentionally 不包含：** `preview.html`、`audit.md`、SEO 审计脚本、运营说明 — 那些不是上线所需。

---

## 2. 每篇文章文件夹里只有 4 样东西

```
articles/037-infinisynapse-vs-julius-ai/
├── article.md        ← Markdown 正文（渲染成 HTML body）
├── meta-tags.html    ← 复制进 <head>（不是完整网页，浏览器打开会空白）
├── schema.json       ← 粘贴进 <script type="application/ld+json">
└── images/           ← 封面 + 正文插图
```

---

## 3. 三分钟接入

### 列表页 `/blog`

```ts
import rows from './blog-list.json';

const posts = rows.sort((a, b) => b.sort_priority - a.sort_priority);
// 卡片：title, excerpt, url, card_tag, filter_category, hero_filename
```

### 详情页 `/blog/:slug`

1. 在 **`blog-content-catalog.csv`** 里用 `slug` 查到 `内容目录`
2. 读取该目录下的 `article.md` + `meta-tags.html` + `schema.json`
3. 上传 `images/` 到 CDN，替换正文与 og:image 路径

### 路由规则

- URL 格式：`/blog/{{slug}}`（无日期、无尾斜杠）
- 示例：`/blog/julius-ai-alternatives`

---

## 4. 部署顺序

按 **`blog-content-catalog.csv`** 的 **`部署序号`** 列执行（已按支柱 P1→P8、文章编号排序）。  
`部署动作` 列标明：新发 / 已发更新 / Q2 候选。

---

## 5. 验收（前端自查）

- [ ] `/blog/{{slug}}` 200，与 CSV 中 `页面URL` 一致
- [ ] `<title>` 来自 `meta-tags.html`，与 H1 一致
- [ ] FAQ 条数与 `schema.json` 里 FAQPage 一致
- [ ] 站内链接 `/blog/...` 可点击，不加 nofollow
- [ ] 图片已上传 CDN，`alt` 非空

**正文/FAQ 内容有问题 → 找内容团队，前端不要改文案。**

---

## 6. 打包命令

```bash
cd SEO/Blog && zip -r frontend-package.zip frontend-package
```
"""


def write_handbook() -> str:
    return """# 博客集成手册（前端版）

## 你要做的页面

| 页面 | 数量 | 说明 |
|------|------|------|
| `/blog` | 1 | 文章列表（卡片 + 分类筛选） |
| `/blog/:slug` | 100 | **同一套详情模板**，按 `ui_module` 切换部分区块样式 |

不需要写 100 套设计。详情页共用壳层：Hero + TOC + 正文 + FAQ 手风琴 + 相关阅读。

---

## 单篇文章装配步骤

```
article.md       →  Markdown 转 HTML（跳过顶部 **Slug** 等元数据行）
meta-tags.html   →  插入 <head>（去掉 HTML 注释块）
schema.json      →  <script type="application/ld+json"> 原样粘贴
images/          →  上传 CDN
```

### article.md 注意

- 顶部 `**Slug**`、`**Target keyword**` 等字段 **不要渲染进正文**
- 所有 `##` / `###` 标题需生成 `id`（TOC 锚点跳转）
- 内链已是 `/blog/other-slug` 相对路径

### meta-tags.html 注意

- **不要用浏览器直接打开** — 它只有 `<head>` 片段，会显示空白
- 复制注释以外的 `<title>`、`<meta>`、`<link>` 行
- **不要改** `canonical` 和 `og:url`

### schema.json 注意

- 是一个 JSON **数组**，原样注入
- FAQ 文字必须与页面上 FAQ 区块一致（内容团队已对齐）

---

## ui_module → 详情页组件变体

查 `blog-content-catalog.csv` 的 **详情页组件** 列：

| ui_module | 额外 UI |
|-----------|---------|
| `long-form-guide` | 标准长文 + TL;DR 高亮框 |
| `how-to-steps` | 分步编号 / 连接教程卡片 |
| `versus-scorecard` | 对比维度表 |
| `tool-listicle` | 工具卡片网格 |
| `alternatives-matrix` | 替代方案对比表 |
| `use-case-persona` | 角色/行业标签 |
| `definition-box` | 首屏定义强调框 |
| `glossary-terms` | 术语表样式 |
| `prompt-resource` | 可复制 Prompt 块 |
| `copy-block` | 一键复制模板 |
| `product-review` | 评分 Pros/Cons |
| `faq-hub` | FAQ 为主布局 |

MVP 可先统一用一种长文样式上线 100 篇，再按模块渐进增强。

---

## Next.js 示例

```ts
// app/blog/[slug]/page.tsx
import catalog from '@/content/blog-content-catalog.csv'; // 或 build 时转 JSON

export async function generateStaticParams() {
  return catalog.map(row => ({ slug: row.slug }));
}

async function loadPost(slug: string) {
  const row = catalog.find(r => r.slug === slug);
  const base = path.join(process.cwd(), 'content', row['内容目录']);
  return {
    markdown: fs.readFileSync(`${base}/article.md`, 'utf8'),
    metaHtml: fs.readFileSync(`${base}/meta-tags.html`, 'utf8'),
    schema: JSON.parse(fs.readFileSync(`${base}/schema.json`, 'utf8')),
  };
}
```

---

## 禁止事项

| 不要做 | 原因 |
|--------|------|
| 改 `canonical` / `og:url` | 重复 URL |
| 给站内 `/blog/` 链接加 nofollow | 破坏内链 |
| 删改 FAQ 文案 | 与 schema 不一致 |
| 用 JS 延迟渲染正文 | 影响收录（优先 SSG/SSR） |
| 改 article.md 英文正文 | 找内容团队 |

---

## 有问题找谁

- 路由 / slug / 路径 → `blog-content-catalog.csv`
- 列表卡片字段 → `blog-list.csv`
- 正文 / FAQ 错误 → 内容团队
"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    ARTICLES.mkdir()

    posts_by_folder = {p["source_folder"]: p for p in load_master_posts()}
    deploy_by_slug = load_deploy_meta()

    catalog_rows: list[dict] = []
    list_rows: list[dict] = []
    total_images = 0

    # Collect all articles first, sort by pillar + article id
    entries: list[tuple[str, Path, dict]] = []
    for pillar_dir in pillar_dirs():
        for art_dir in sorted(pillar_dir.glob("[0-9][0-9][0-9]-*/")):
            if not (art_dir / "article.md").is_file():
                continue
            folder = art_dir.name
            post = posts_by_folder.get(folder, {})
            entries.append((folder, art_dir, post))

    entries.sort(key=lambda x: (int(x[0][:3]), x[0]))

    for i, (folder, art_dir, post) in enumerate(entries, 1):
        rel_path = f"articles/{folder}"
        dest = OUT / rel_path
        n_img = copy_article(art_dir, dest)
        total_images += n_img
        hero = find_hero_image(art_dir)
        slug = post.get("slug") or folder.split("-", 1)[-1]
        deploy = deploy_by_slug.get(slug, {})
        catalog_rows.append(
            build_catalog_row(i, post, folder, rel_path, hero, n_img, deploy)
        )
        list_rows.append(build_list_row(post, folder, rel_path, hero))

    catalog_fields = list(catalog_rows[0].keys()) if catalog_rows else []
    list_fields = list(list_rows[0].keys()) if list_rows else []

    for path in (OUT / "blog-content-catalog.csv",):
        with path.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=catalog_fields)
            w.writeheader()
            w.writerows(catalog_rows)

    with (OUT / "blog-list.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list_fields)
        w.writeheader()
        w.writerows(list_rows)

    (OUT / "blog-list.json").write_text(
        json.dumps(list_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (OUT / "README.md").write_text(write_readme(len(catalog_rows), total_images), encoding="utf-8")
    (OUT / "集成手册.md").write_text(write_handbook(), encoding="utf-8")

    # Copy nav tags if present
    nav_src = BLOG / "blog-nav-tags.csv"
    if nav_src.is_file():
        shutil.copy2(nav_src, OUT / "blog-nav-tags.csv")

    print(f"Built → {OUT}")
    print(f"  articles: {len(catalog_rows)}")
    print(f"  images:   {total_images}")
    print(f"  catalog:  blog-content-catalog.csv")
    print(f"\nZip:")
    print(f"  cd SEO/Blog && zip -r frontend-package.zip frontend-package")


if __name__ == "__main__":
    main()
