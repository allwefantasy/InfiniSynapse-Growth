#!/usr/bin/env python3
"""Generate preview.html for each Pillar 1 article (local browser review)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension

PILLAR = Path(__file__).resolve().parent

PREVIEW_CSS = """
:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --text: #0f172a;
  --muted: #64748b;
  --accent: #0d9488;
  --accent-soft: #f0fdfa;
  --border: #e2e8f0;
  --code-bg: #f1f5f9;
  --banner: #1e40af;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 17px;
  line-height: 1.7;
}
.preview-banner {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--banner);
  color: #fff;
  padding: 10px 20px;
  font-size: 13px;
  text-align: center;
  letter-spacing: 0.02em;
}
.preview-banner strong { font-weight: 700; }
.site-header {
  max-width: 860px;
  margin: 0 auto;
  padding: 28px 24px 0;
}
.site-header a {
  color: var(--accent);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
}
article {
  max-width: 860px;
  margin: 0 auto 64px;
  padding: 32px 24px 48px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(15, 23, 42, 0.06);
}
article > h1:first-child {
  font-size: 2.1rem;
  line-height: 1.2;
  margin: 0 0 0.75rem;
  letter-spacing: -0.02em;
}
article > blockquote:first-of-type {
  margin: 0 0 1.5rem;
  padding: 0;
  border: none;
  color: var(--muted);
  font-size: 0.95rem;
}
article img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1.5rem 0;
  border: 1px solid var(--border);
}
h2 {
  font-size: 1.45rem;
  margin: 2.5rem 0 1rem;
  padding-bottom: 0.35rem;
  border-bottom: 2px solid var(--accent-soft);
  color: #0f766e;
}
h3 { font-size: 1.15rem; margin: 1.75rem 0 0.75rem; }
p { margin: 0 0 1.1rem; }
ul, ol { margin: 0 0 1.1rem; padding-left: 1.4rem; }
li { margin-bottom: 0.35rem; }
a { color: #2563eb; }
a:hover { text-decoration: underline; }
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
  margin: 1.25rem 0 1.5rem;
}
th, td {
  border: 1px solid var(--border);
  padding: 10px 12px;
  text-align: left;
  vertical-align: top;
}
th { background: var(--accent-soft); color: #0f766e; font-weight: 600; }
tr:nth-child(even) td { background: #fafafa; }
blockquote {
  margin: 1.25rem 0;
  padding: 14px 18px;
  background: var(--accent-soft);
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  color: #134e4a;
}
blockquote p:last-child { margin-bottom: 0; }
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.88em;
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
}
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}
footer.preview-meta {
  max-width: 860px;
  margin: 0 auto 48px;
  padding: 0 24px;
  font-size: 13px;
  color: var(--muted);
}
footer.preview-meta code {
  font-size: 12px;
}
"""

BANNER = (
    '<div class="preview-banner">'
    "<strong>LOCAL PREVIEW</strong> · Not for production · "
    "Images &amp; links use relative paths · "
    "Open via <code>file://</code> or local static server"
    "</div>"
)


def slugify(value: str, separator: str = "-") -> str:
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s_-]+", separator, value)


def strip_cms_metadata(text: str) -> str:
    """Remove SEO metadata lines; keep title, byline, hero, body."""
    skip_prefixes = (
        "**Meta Description**:",
        "**Slug**:",
        "**Target keyword**:",
        "**Secondary**:",
    )
    lines = []
    for line in text.splitlines():
        if any(line.strip().startswith(p) for p in skip_prefixes):
            continue
        lines.append(line)
    return "\n".join(lines)


def extract_meta_tags(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    # Drop HTML comment blocks
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    return raw.strip()


def md_to_html(text: str) -> str:
    converter = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "nl2br",
            TocExtension(slugify=slugify, permalink=False),
        ]
    )
    return converter.convert(text)


def build_preview(article_dir: Path) -> None:
    article_md = article_dir / "article.md"
    meta_path = article_dir / "meta-tags.html"
    schema_path = article_dir / "schema.json"
    out_path = article_dir / "preview.html"

    if not article_md.exists():
        print(f"SKIP {article_dir.name} — no article.md")
        return

    md_text = strip_cms_metadata(article_md.read_text(encoding="utf-8"))
    body_html = md_to_html(md_text)

    meta_html = extract_meta_tags(meta_path) if meta_path.exists() else ""
    schema_block = ""
    if schema_path.exists():
        schema_json = schema_path.read_text(encoding="utf-8").strip()
        schema_block = (
            f'<script type="application/ld+json">\n{schema_json}\n</script>'
        )

    folder_name = article_dir.name
    index_link = f"../INDEX-preview.html"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
{meta_html}
  <style>{PREVIEW_CSS}</style>
{schema_block}
</head>
<body>
{BANNER}
<header class="site-header">
  <a href="{index_link}">← All Pillar 1 previews</a>
</header>
<article class="blog-post">
{body_html}
</article>
<footer class="preview-meta">
  Source: <code>{folder_name}/article.md</code> ·
  Generated by <code>build-preview.py</code>
</footer>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ {folder_name}/preview.html")


def build_index(article_dirs: list[Path]) -> None:
    items = []
    for d in sorted(article_dirs):
        md = d / "article.md"
        if not md.exists():
            continue
        first = md.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        items.append((d.name, first))

    lis = "\n".join(
        f'    <li><a href="{slug}/preview.html"><code>{slug}</code> — {title}</a></li>'
        for slug, title in items
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Pillar 1 · Article Previews</title>
  <style>
    body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 24px; color: #0f172a; }}
    h1 {{ font-size: 1.75rem; }}
    ul {{ line-height: 2; padding-left: 1.2rem; }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{ font-size: 0.85em; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; }}
    .note {{ color: #64748b; font-size: 14px; margin-bottom: 24px; }}
  </style>
</head>
<body>
  <h1>Pillar 3 · Article Previews (20)</h1>
  <p class="note">Local preview pages for editorial / frontend review. Not deployed to production.</p>
  <ul>
{lis}
  </ul>
</body>
</html>
"""
    (PILLAR / "INDEX-preview.html").write_text(html, encoding="utf-8")
    print("  ✅ INDEX-preview.html")


def main() -> None:
    dirs = sorted(p for p in PILLAR.glob("[0-9][0-9][0-9]-*") if p.is_dir())
    print(f"Building {len(dirs)} preview.html files …")
    for d in dirs:
        build_preview(d)
    build_index(dirs)
    print("Done.")


if __name__ == "__main__":
    main()
