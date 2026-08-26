#!/usr/bin/env python3
"""Package new + changed blog articles for programmer handoff (git-aware).

Includes:
  - Pillar 9–15: all articles (new batch, entire pillars untracked)
  - Pillar 1–8: only folders with new article.md OR modified article.md vs HEAD

Skips unchanged Pillar 1–8 articles.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
OUT = BLOG / "programmer-handoff-pack"
ARTS = OUT / "articles"

FILES = ("article.md", "meta-tags.html", "head.html", "schema.json", "preview.html")
IMG_GLOBS = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif", "*.svg")
DATA_FILES = (
    "blog-index-import-master.json",
    "blog-cms-import-100.csv",
    "blog-cms-import-202.csv",
)


def pillar_dirs() -> list[Path]:
    return sorted(
        p for p in BLOG.glob("pillar*") if p.is_dir() and " copy" not in p.name
    )


def is_pillar_1_8(pillar: Path) -> bool:
    return bool(re.match(r"pillar[1-8]-", pillar.name))


def article_folders(pillar: Path) -> list[Path]:
    return sorted(p for p in pillar.glob("[0-9][0-9][0-9]-*") if (p / "article.md").is_file())


def git_new_folders() -> set[str]:
    out: set[str] = set()
    r = subprocess.run(
        ["git", "status", "--porcelain", "--", "SEO/Blog/pillar*"],
        cwd=BLOG.parents[1],
        capture_output=True,
        text=True,
    )
    for line in r.stdout.splitlines():
        if not line.startswith("??"):
            continue
        path = line[3:].strip().rstrip("/")
        m = re.search(r"SEO/Blog/(pillar[^/]+/(\d{3}-[^/]+))", path)
        if m and (BLOG / m.group(1) / "article.md").is_file():
            out.add(m.group(1))
    return out


def git_modified_article_md() -> set[str]:
    r = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", "SEO/Blog/pillar*/*/article.md"],
        cwd=BLOG.parents[1],
        capture_output=True,
        text=True,
    )
    out: set[str] = set()
    for line in r.stdout.splitlines():
        m = re.search(r"SEO/Blog/(pillar[^/]+/\d{3}-[^/]+)/article\.md", line)
        if m:
            out.add(m.group(1))
    return out


def select_folders() -> list[tuple[Path, str]]:
    """Return (absolute art_dir, reason) sorted by id."""
    git_new = git_new_folders()
    git_mod = git_modified_article_md()
    selected: dict[str, tuple[Path, str]] = {}

    for pillar in pillar_dirs():
        for art in article_folders(pillar):
            rel = f"{pillar.name}/{art.name}"
            if is_pillar_1_8(pillar):
                if rel in git_new:
                    selected[rel] = (art, "new")
                elif rel in git_mod:
                    selected[rel] = (art, "modified")
            else:
                # Pillar 9–15: entire batch is new content
                selected[rel] = (art, "new")

    return sorted(selected.values(), key=lambda x: x[0].name)


def load_catalog() -> dict[str, dict]:
    cat: dict[str, dict] = {}
    for path in (BLOG / "blog-content-catalog.csv", BLOG / "frontend-package" / "blog-content-catalog.csv"):
        if not path.is_file():
            continue
        for row in csv.DictReader(path.open(encoding="utf-8-sig")):
            cat[row.get("文章编号", "")] = row
    # CMS import fallback
    cms = BLOG / "blog-cms-import-202.csv"
    if cms.is_file():
        for row in csv.DictReader(cms.open(encoding="utf-8")):
            aid = row.get("id", "")
            if aid and aid not in cat:
                cat[aid] = {
                    "slug": row.get("slug", ""),
                    "英文标题": row.get("title", ""),
                    "页面URL": row.get("url", ""),
                    "目标关键词": row.get("target_keyword", ""),
                }
    return cat


def strip_body_h1(md: str) -> str:
    """Remove leading H1 — page H1 comes from CMS title field."""
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


def copy_article(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        f = src / name
        if not f.is_file():
            continue
        if name == "article.md":
            (dest / name).write_text(
                strip_body_h1(f.read_text(encoding="utf-8")), encoding="utf-8"
            )
        else:
            shutil.copy2(f, dest / name)
    imgdir = src / "images"
    if imgdir.is_dir():
        (dest / "images").mkdir(exist_ok=True)
        for pat in IMG_GLOBS:
            for img in imgdir.glob(pat):
                shutil.copy2(img, dest / "images" / img.name)


def slug_from_art(art: Path, cat: dict) -> str:
    aid = art.name.split("-")[0]
    if aid in cat and cat[aid].get("slug"):
        return cat[aid]["slug"]
    head = art / "head.html"
    if head.is_file():
        m = re.search(r"/en/blog/([^\"'<>]+)", head.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    md = art / "article.md"
    if md.is_file():
        m = re.search(r"\*\*Slug\*\*:\s*`/blog/([^`]+)`", md.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return art.name.split("-", 1)[-1]


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    ARTS.mkdir(parents=True)

    cat = load_catalog()
    rows: list[dict] = []
    new_n = mod_n = 0

    for art, reason in select_folders():
        rel_pillar = art.parent.name
        dest = ARTS / rel_pillar / art.name
        copy_article(art, dest)
        aid = art.name.split("-")[0]
        c = cat.get(aid, {})
        slug = slug_from_art(art, cat)
        url = c.get("页面URL", f"/en/blog/{slug}")
        if url.startswith("/blog/"):
            url = f"https://infinisynapse.com/en{url}"
        elif url.startswith("/en/"):
            url = f"https://infinisynapse.com{url}"
        elif not url.startswith("http"):
            url = f"https://infinisynapse.com/en/blog/{slug}"

        if reason == "new":
            new_n += 1
            change = "新发文章"
        else:
            mod_n += 1
            change = "正文/SEO/TL;DR 更新"

        rows.append({
            "文章编号": aid,
            "slug": slug,
            "完整URL": url,
            "英文标题": c.get("英文标题", c.get("title", "")),
            "目标关键词": c.get("目标关键词", c.get("target_keyword", "")),
            "支柱": rel_pillar,
            "变更类型": change,
            "源目录": f"{rel_pillar}/{art.name}",
            "交付目录": f"articles/{rel_pillar}/{art.name}",
            "部署文件": "article.md; head.html; meta-tags.html; schema.json; preview.html(可选); images/",
        })

    for name in DATA_FILES:
        src = BLOG / name
        if src.is_file():
            shutil.copy2(src, OUT / name)

    with (OUT / "deploy-manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    readme = f"""# 博客文章 · 程序员交付包（{len(rows)} 篇）

> 仅含**新发**或**相对 Git HEAD 有 `article.md` 改动**的文章；未改动的 Pillar 1–8 篇目不包含在内。

## 包内结构

```
programmer-handoff-pack/
├── README.md
├── deploy-manifest.csv          ← 部署清单（编号 / slug / URL / 变更类型）
├── blog-index-import-master.json
├── blog-cms-import-100.csv
├── blog-cms-import-202.csv
└── articles/
    └── pillar{{N}}-{{name}}/
        └── {{编号}}-{{slug}}/
            ├── article.md       ← 正文（无 H1；页面 H1 用 title）
            ├── head.html        ← 整段注入 <head>
            ├── meta-tags.html
            ├── schema.json
            ├── preview.html     ← 本地 QA 对照（可选）
            └── images/
```

## 统计

| 类型 | 篇数 |
|------|------|
| 新发（Pillar 9–15 全量 + Pillar 1–8 新增编号） | {new_n} |
| 更新（Pillar 1–8 相对 HEAD 改动） | {mod_n} |
| **合计** | **{len(rows)}** |

## 部署步骤

1. 打开 **`deploy-manifest.csv`**，按 `完整URL` 或 `slug` 定位线上页面。
2. 对每一行，从 **`articles/{{源目录}}`** 覆盖 CMS / 静态站点对应文件：
   - **必做**：`article.md` → 渲染正文（**已无 `# 标题`**；页面 H1 用 CMS「文章标题」= `blog-index` 的 `title` 或 `schema.headline`）
   - **推荐**：`head.html` → 注入 canonical、description(150–160)、og、twitter、JSON-LD
   - **可选**：`schema.json`、`images/`（新文章必传图）
3. **列表页**：import `blog-index-import-master.json` 的 `posts` 数组（或 CSV 导入 CMS）。
4. URL 规范：`https://infinisynapse.com/en/blog/{{slug}}`（无尾斜杠）。

## 新文章 vs 更新

- **新发**：Pillar 9–15 全部 + Pillar 1–8 中 101–119 等新编号 — 需创建路由并上传 hero 图。
- **更新**：Pillar 1–8 原 001–100 等 — 覆盖现有 URL 内容即可；sitemap 通常无需改。

## 验证

```bash
curl -s "https://infinisynapse.com/en/blog/{{slug}}" | grep -i canonical
```

部署后可在 GSC 对 manifest 中的 URL 批量「请求编入索引」。
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    zip_path = BLOG / "programmer-handoff-pack.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in OUT.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(OUT.parent))

    mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Built {OUT} — {len(rows)} articles (new {new_n}, modified {mod_n})")
    print(f"Zip: {zip_path} ({mb:.1f} MB)")


if __name__ == "__main__":
    main()
