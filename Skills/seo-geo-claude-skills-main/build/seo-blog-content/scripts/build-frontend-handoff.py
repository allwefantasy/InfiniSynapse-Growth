#!/usr/bin/env python3
"""Build SEO/Blog/frontend-handoff/ — self-contained pack for frontend team."""
from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
OUT = BLOG / "frontend-handoff"
CONTENT = OUT / "content"
# Deploy/rule guides now live in the skill library (single source of truth)
SKILL_REF = BLOG.parent.parent / "Skills" / "seo-geo-claude-skills-main" / "build" / "seo-blog-content" / "references"

DEPLOY_FILES = ("article.md", "meta-tags.html", "schema.json", "head.html")
PREVIEW_FILE = "preview.html"
IMAGE_GLOBS = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif", "*.svg")

UI_MODULES = {
    "long-form-guide": {"count_hint": 26, "label": "标准长文", "reference_slug": "ai-for-data-analysis"},
    "how-to-steps": {"count_hint": 21, "label": "步骤教程", "reference_slug": "connect-supabase-to-ai-data-analyst"},
    "versus-scorecard": {"count_hint": 16, "label": "对比打分表", "reference_slug": "code-agent-vs-data-agent"},
    "use-case-persona": {"count_hint": 13, "label": "场景/角色", "reference_slug": "ai-data-analysis-finance-teams"},
    "tool-listicle": {"count_hint": 8, "label": "工具排行榜", "reference_slug": "best-ai-tools-for-data-analysis"},
    "alternatives-matrix": {"count_hint": 7, "label": "替代方案矩阵", "reference_slug": "chatgpt-data-analysis-alternatives"},
    "definition-box": {"count_hint": 2, "label": "定义强调框", "reference_slug": "what-is-a-data-agent"},
    "glossary-terms": {"count_hint": 2, "label": "术语表", "reference_slug": "data-agent-glossary"},
    "prompt-resource": {"count_hint": 2, "label": "Prompt 资源", "reference_slug": "ai-data-analysis-prompts"},
    "copy-block": {"count_hint": 1, "label": "可复制模板", "reference_slug": "ai-data-analyst-job-description"},
    "product-review": {"count_hint": 1, "label": "产品评测", "reference_slug": "infinisynapse-review"},
    "faq-hub": {"count_hint": 1, "label": "FAQ 主导", "reference_slug": "ai-analytics-glossary"},
}


def pillar_dirs() -> list[Path]:
    return sorted(
        p for p in BLOG.glob("pillar[1-8]-*")
        if p.is_dir() and " copy" not in p.name
    )


def strip_body_h1(md: str) -> str:
    """Remove the first leading H1 so the deploy body has no H1 (page H1 = title)."""
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
            return md  # first heading already H2+ (no body H1)
        if re.match(r"^#\s+\S", line):
            del lines[i]
            if i < len(lines) and lines[i].strip() == "":
                del lines[i]
            return "".join(lines)
    return md


def copy_article(art_dir: Path, dest: Path) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for name in DEPLOY_FILES:
        src = art_dir / name
        if not src.is_file():
            continue
        if name == "article.md":
            # deploy copy is body-only; page <h1> is rendered from the title
            (dest / name).write_text(
                strip_body_h1(src.read_text(encoding="utf-8")), encoding="utf-8"
            )
        else:
            shutil.copy2(src, dest / name)
        copied.append(name)
    preview_src = art_dir / PREVIEW_FILE
    has_preview = preview_src.is_file()
    if has_preview:
        shutil.copy2(preview_src, dest / PREVIEW_FILE)
        copied.append(PREVIEW_FILE)
    img_dest = dest / "images"
    img_dir = art_dir / "images"
    n_images = 0
    if img_dir.is_dir():
        img_dest.mkdir(exist_ok=True)
        for pattern in IMAGE_GLOBS:
            for img in img_dir.glob(pattern):
                shutil.copy2(img, img_dest / img.name)
                n_images += 1
    return {"files": copied, "images": n_images, "has_preview": has_preview}


def build_preview_index(article_manifest: list[dict]) -> str:
    rows: list[str] = []
    for art in sorted(article_manifest, key=lambda x: x["id"]):
        if not art.get("has_preview"):
            continue
        rel = f"{art['dest']}/preview.html"
        title = art.get("title") or art["folder"]
        rows.append(
            f'    <li><a href="{rel}"><code>{art["folder"]}</code> — {title}</a></li>'
        )
    n = len(rows)
    items = "\n".join(rows)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>InfiniSynapse Blog · 100 Article Previews</title>
  <style>
    body {{ font-family: -apple-system, sans-serif; max-width: 960px; margin: 40px auto; padding: 0 24px; color: #0f172a; }}
    h1 {{ font-size: 1.75rem; }}
    ul {{ line-height: 2; padding-left: 1.2rem; }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{ font-size: 0.85em; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; }}
    .note {{ color: #64748b; font-size: 14px; margin-bottom: 24px; line-height: 1.6; }}
    .warn {{ background: #fef3c7; border: 1px solid #fcd34d; padding: 12px 16px; border-radius: 8px; margin-bottom: 24px; font-size: 14px; }}
  </style>
</head>
<body>
  <h1>InfiniSynapse Blog · Article Previews ({n})</h1>
  <div class="warn">
    <strong>如何预览：</strong>用桌面 Chrome / Safari 打开本页，点击链接查看完整文章。<br>
    <strong>注意：</strong><code>meta-tags.html</code> 不是网页（只有 &lt;head&gt; 片段），打开会空白 — 请点 <code>preview.html</code>。
  </div>
  <p class="note">本地预览，勿部署到生产环境。集成上线请用 article.md + meta-tags.html + schema.json。</p>
  <ul>
{items}
  </ul>
</body>
</html>
"""


def rewrite_source_paths(posts: list[dict]) -> list[dict]:
    out = []
    for p in posts:
        q = dict(p)
        q["source_path"] = f"content/{p['pillar_cluster']}/{p['source_folder']}"
        out.append(q)
    return out


def build_readme(article_count: int, image_count: int, preview_count: int) -> str:
    return f"""# InfiniSynapse Blog · 前端交付包（100 篇）

> 内容团队交付 · 可直接 zip 打包集成  
> 生成目录：`SEO/Blog/frontend-handoff/`

## 先看什么（15 分钟）

1. **[FRONTEND-DEPLOY-GUIDE.md](./FRONTEND-DEPLOY-GUIDE.md)** — 部署总手册（零 SEO 背景）
2. **[blog-index-import-master.json](./blog-index-import-master.json)** — 列表页 100 条卡片数据
3. **[PREVIEW-INDEX.html](./PREVIEW-INDEX.html)** — **浏览器打开，点链接预览全部 {preview_count} 篇文章**

## 如何预览文章（重要）

| 文件 | 双击打开 | 说明 |
|---|---|---|
| **`preview.html`** | ✅ 完整网页 | 本地 UI 参考，**用这个看效果** |
| `meta-tags.html` | ❌ 空白页 | 只是 `<head>` 片段，给前端粘贴用 |
| `article.md` | ✅ 编辑器 | Markdown 源文件 |

桌面浏览器打开 **[PREVIEW-INDEX.html](./PREVIEW-INDEX.html)**，或进入任意文章文件夹打开 `preview.html`。

## 目录结构

```
frontend-handoff/
├── README.md                          ← 本文件
├── PREVIEW-INDEX.html                 ← 100 篇预览入口（浏览器打开）
├── FRONTEND-DEPLOY-GUIDE.md           ← 集成手册
├── blog-index-import-master.json      ← 列表页 import（推荐）
├── blog-cms-import-100.csv            ← 同上，CSV 版
├── ui-modules-reference.json          ← 12 种 UI 变体说明
├── MANIFEST.json                      ← 文件清单统计
└── content/                           ← 100 篇文章发布包
    └── pillar{{N}}-.../
        └── {{id}}-{{slug}}/
            ├── article.md             ← Markdown 正文（上线用）
            ├── meta-tags.html         ← <head> 片段（上线用，勿直接打开）
            ├── schema.json            ← JSON-LD（上线用）
            ├── preview.html           ← 完整预览页（本地看，勿部署）
            └── images/                ← hero + 插图（{image_count} 张）
```

## 快速集成

```ts
import blogIndex from './blog-index-import-master.json';

// 列表页
const posts = blogIndex.posts.sort((a, b) => b.sort_priority - a.sort_priority);

// 详情页：slug → source_path
const post = blogIndex.posts.find(p => p.slug === slug);
// 读 content/{{pillar}}/{{folder}}/article.md + meta-tags.html + schema.json
```

## 统计

- 文章数：**{article_count}**
- 可预览：**{preview_count}**（均有 preview.html）
- 图片数：**{image_count}**
- 路由格式：`/blog/{{slug}}`（无日期前缀、无尾斜杠）

## 不要部署到线上的文件

| 文件 | 说明 |
|---|---|
| `PREVIEW-INDEX.html` | 本地预览索引 |
| `content/**/preview.html` | 本地 UI 参考 |
| `MANIFEST.json` | 交付清单 |

## 有问题找谁

- 正文 / FAQ / 链接错误 → 内容团队
- 路由 / slug → 查 `blog-index-import-master.json`
- 样式 / 组件 → 按 `ui_module` 字段选变体（见 `ui-modules-reference.json`）
"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    CONTENT.mkdir()

    # Docs & index data — deploy/rule guides sourced from the skill library
    shutil.copy2(SKILL_REF / "FRONTEND-DEPLOY-GUIDE.md", OUT / "FRONTEND-DEPLOY-GUIDE.md")
    shutil.copy2(BLOG / "blog-cms-import-100.csv", OUT / "blog-cms-import-100.csv")
    for extra in ("PROGRAMMER-SEO-DEPLOY.md", "QUICKCREATOR-SEO-FIX.md"):
        src = SKILL_REF / extra
        if src.is_file():
            shutil.copy2(src, OUT / extra)
    for extra in ("seo-meta.json", "quickcreator-seo-fields.csv"):
        src = BLOG / extra
        if src.is_file():
            shutil.copy2(src, OUT / extra)

    # Load master index and rewrite paths
    master_src = json.loads((BLOG / "blog-index-import-master.json").read_text(encoding="utf-8"))
    posts = rewrite_source_paths(master_src["posts"])
    master_src["posts"] = posts
    master_src["_handoff_note"] = (
        "source_path 已改为相对本包 content/ 目录；"
        "与仓库 SEO/Blog/ 内路径不同，集成时以本文件为准。"
    )
    (OUT / "blog-index-import-master.json").write_text(
        json.dumps(master_src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # UI modules reference
    slug_to_path = {p["slug"]: p["source_path"] for p in posts}
    ui_ref = {
        "_comment": "详情页 ui_module 字段 → 组件变体对照",
        "modules": {
            k: {**v, "example_source_path": slug_to_path.get(v["reference_slug"], "")}
            for k, v in UI_MODULES.items()
        },
    }
    (OUT / "ui-modules-reference.json").write_text(
        json.dumps(ui_ref, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Copy content
    article_manifest: list[dict] = []
    total_images = 0
    preview_count = 0
    slug_by_folder = {p["source_folder"]: p for p in posts}
    for pillar_dir in pillar_dirs():
        pillar_name = pillar_dir.name
        for art_dir in sorted(pillar_dir.glob("[0-9][0-9][0-9]-*/")):
            if not (art_dir / "article.md").is_file():
                continue
            dest = CONTENT / pillar_name / art_dir.name
            info = copy_article(art_dir, dest)
            total_images += info["images"]
            if info["has_preview"]:
                preview_count += 1
            post = slug_by_folder.get(art_dir.name, {})
            article_manifest.append({
                "id": art_dir.name[:3],
                "folder": art_dir.name,
                "slug": post.get("slug", ""),
                "title": post.get("title", ""),
                "pillar": pillar_name,
                "dest": f"content/{pillar_name}/{art_dir.name}",
                "files": info["files"],
                "images": info["images"],
                "has_preview": info["has_preview"],
            })

    # Master preview index
    (OUT / "PREVIEW-INDEX.html").write_text(
        build_preview_index(article_manifest), encoding="utf-8"
    )

    ui_counts = Counter(p.get("ui_module", "") for p in posts)
    manifest = {
        "generated_by": "SEO/Blog/build-frontend-handoff.py",
        "article_count": len(article_manifest),
        "preview_count": preview_count,
        "image_count": total_images,
        "pillars": len(pillar_dirs()),
        "ui_module_counts": dict(ui_counts),
        "filter_category_counts": dict(Counter(p["filter_category"] for p in posts)),
        "articles": sorted(article_manifest, key=lambda x: x["id"]),
    }
    (OUT / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (OUT / "README.md").write_text(
        build_readme(len(article_manifest), total_images, preview_count), encoding="utf-8"
    )

    # Patch guide paths for handoff context
    guide = (OUT / "FRONTEND-DEPLOY-GUIDE.md").read_text(encoding="utf-8")
    guide = guide.replace(
        "SEO/Blog/pillar2-data-agent-vs-alternatives/014-code-agent-vs-data-agent/",
        "content/pillar2-data-agent-vs-alternatives/014-code-agent-vs-data-agent/",
    )
    guide = guide.replace(
        "SEO/Blog/pillar2-data-agent-vs-alternatives/014-code-agent-vs-data-agent/article.md",
        "content/pillar2-data-agent-vs-alternatives/014-code-agent-vs-data-agent/article.md",
    )
    guide = guide.replace(
        "**`samples/preview-014-versus.html`**（Versus 类参考；其余文章结构相同）",
        "**`PREVIEW-INDEX.html`**（100 篇预览入口）或任意文章文件夹内的 **`preview.html`**",
    )
    guide = guide.replace(
        "任意文章文件夹里的 **`preview.html`**",
        "**`PREVIEW-INDEX.html`** 或任意文章文件夹内的 **`preview.html`**",
    )
    if "meta-tags.html` 不是网页" not in guide:
        guide = guide.replace(
            "本地视觉参考：",
            "**注意：`meta-tags.html` 不是网页（打开会空白），请用 `preview.html` 预览。**\n\n本地视觉参考：",
        )
    (OUT / "FRONTEND-DEPLOY-GUIDE.md").write_text(guide, encoding="utf-8")

    print(f"Built → {OUT}")
    print(f"  articles: {len(article_manifest)}")
    print(f"  previews: {preview_count}")
    print(f"  images:   {total_images}")
    print(f"\nZip command:")
    print(f"  cd {BLOG.parent.parent} && zip -r frontend-handoff.zip SEO/Blog/frontend-handoff")


if __name__ == "__main__":
    main()
