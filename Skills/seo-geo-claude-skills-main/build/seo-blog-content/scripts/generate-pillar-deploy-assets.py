#!/usr/bin/env python3
"""Generate DEPLOY.md, render-all-images.sh, manifest.json per pillar from registry."""
import json
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
REG_FILES = [
    BLOG / "pillar-manifests" / "pillar2-articles.json",
    BLOG / "pillar-manifests" / "pillar4-8-articles.json",
]
ROOT = "/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"


def deploy_md(pillar: dict) -> str:
    n = pillar["pillar_num"]
    folder = pillar["folder"]
    articles = pillar["articles"]
    first, last = articles[0]["id"], articles[-1]["id"]
    rows = "\n".join(
        f"| `{a['slug']}` | `{a['folder']}/` | `https://infinisynapse.com/en/blog/{a['slug']}` |"
        for a in articles
    )
    return f"""# 前端部署手册 · Pillar {n}（{len(articles)} 篇）

> **内容集群**：{pillar['name']}（规划文档 {first}–{last}）

## 1. 路由映射

| slug | 源目录 | 发布 URL |
|---|---|---|
{rows}

机器可读清单：[manifest.json](./manifest.json)

## 2. 集成要点

- 正文：`article.md` → HTML，H2/H3 需与 TOC 锚点一致
- `<head>`：`meta-tags.html` + `schema.json` JSON-LD
- 图片 CDN：`/blog/assets/{folder}/<slug>/hero.png`
- 内链：保持 `/blog/<slug>` 相对路径

## 3. 质量门禁

```bash
python3 SEO/Blog/audit-wordcount.py SEO/Blog/{folder}
python3 SEO/Blog/audit-eeat.py SEO/Blog/{folder}
python3 SEO/Blog/audit-external-links.py SEO/Blog/{folder}
python3 SEO/Blog/sync-audit-gates.py
```

| 指标 | 要求 |
|---|---|
| 正文字数 | 2000–2500（从 `## TL;DR` 起） |
| 关键词密度 | 1.2%–1.7% |
| EEAT 快速扫描 | 12/12 |
| 高 DR 外链 | ≥5 条（DR≥70，叙事嵌入）· `audit-high-dr-links.py` |

## 4. 预览

```bash
python3 SEO/Blog/{folder}/build-preview.py
open SEO/Blog/{folder}/INDEX-preview.html
```

## 5. Hero 图

```bash
python3 SEO/Blog/build-pillar-heroes.py {folder}
bash SEO/Blog/{folder}/render-all-images.sh
```
"""


def manifest(pillar: dict) -> dict:
    return {
        "pillar": pillar["folder"],
        "pillar_name": pillar["name"],
        "article_count": len(pillar["articles"]),
        "source_plan": f"100页主题集群规划-v1-替换后主关键词版.md · Pillar {pillar['pillar_num']}",
        "articles": [
            {
                "id": a["id"],
                "folder": a["folder"],
                "slug": a["slug"],
                "keyword": a["keyword"],
                "type": a["type"],
                "url": f"https://infinisynapse.com/en/blog/{a['slug']}",
            }
            for a in pillar["articles"]
        ],
    }


def render_sh(pillar: dict) -> str:
    folder = pillar["folder"]
    lines = [
        "#!/usr/bin/env bash",
        f"# Pillar {pillar['pillar_num']} · Hero HTML→PNG",
        "set -euo pipefail",
        f'ROOT="{ROOT}"',
        f'PILLAR="$ROOT/SEO/Blog/{folder}"',
        'CHROME=""',
        'for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"; do',
        '  [[ -x "$p" ]] && CHROME="$p" && break',
        "done",
        '[[ -n "$CHROME" ]] || { echo "❌ Chrome not found"; exit 1; }',
        "",
        "render() {",
        '  local label="$1" html="$2" png="$3" w="${4:-1200}" h="${5:-630}"',
        '  [[ -f "$html" ]] || { echo "SKIP $label"; return; }',
        '  mkdir -p "$(dirname "$png")"',
        '  echo "▶ $label (${w}×${h})"',
        '  "$CHROME" --headless=new --hide-scrollbars --disable-gpu \\',
        '    --force-device-scale-factor=2 --window-size="${w},${h}" \\',
        '    --screenshot="$png" --default-background-color=ffffffff \\',
        '    "file://$html" >/dev/null 2>&1',
        '  if [[ -f "$png" ]]; then',
        '    echo "  ✅ $(basename "$png")"',
        '    cp -f "$png" "$(dirname "$png")/hero.png"',
        '    cp -f "$png" "$(dirname "$png")/og-cover.png"',
        "  fi",
        "}",
        "",
    ]
    for a in pillar["articles"]:
        slug = a["slug"]
        lines.append(
            f'render "{a["id"]}-hero" "$PILLAR/{a["folder"]}/visuals/hero.html" '
            f'"$PILLAR/{a["folder"]}/images/hero-{slug}.png" 1200 630'
        )
    lines.append(f'echo "✅ Pillar {pillar["pillar_num"]} heroes rendered."')
    return "\n".join(lines) + "\n"


def main() -> int:
    pillars = []
    for reg_path in REG_FILES:
        if reg_path.exists():
            data = json.loads(reg_path.read_text(encoding="utf-8"))
            pillars.extend(data["pillars"])
    for pillar in pillars:
        root = BLOG / pillar["folder"]
        (root / "DEPLOY.md").write_text(deploy_md(pillar), encoding="utf-8")
        (root / "manifest.json").write_text(
            json.dumps(manifest(pillar), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        sh = root / "render-all-images.sh"
        sh.write_text(render_sh(pillar), encoding="utf-8")
        sh.chmod(0o755)
        print(f"  {pillar['folder']}: DEPLOY + manifest + render script")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
