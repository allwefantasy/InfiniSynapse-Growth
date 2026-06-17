#!/usr/bin/env python3
"""把 article.html 里的图片占位符替换为已上传的 mmbiz CDN <img>，生成可直接 paste 的 HTML（无需再上传图片）。"""
import base64
import json
import re
from pathlib import Path

DIR = Path(__file__).parent
html = (DIR / "article.html").read_text(encoding="utf-8")
cdn = json.loads((DIR / "cdn-mapping.json").read_text(encoding="utf-8"))

missing = []
for key, url in cdn.items():
    pattern = rf'<p data-image-placeholder="{re.escape(key)}"[^>]*>【待上传图片：[^】]*】</p>'
    replacement = f'<p style="text-align:center;margin:1em 0;"><img src="{url}" style="max-width:100%;" alt=""/></p>'
    html, n = re.subn(pattern, replacement, html)
    if n == 0:
        missing.append(key)

leftover = re.findall(r'data-image-placeholder="([^"]+)"', html)
if missing or leftover:
    raise SystemExit(f"未替换的占位符 missing={missing} leftover={leftover}")

out = DIR / "article-with-cdn.html"
out.write_text(html, encoding="utf-8")
b64 = base64.b64encode(html.encode("utf-8")).decode("ascii")
(DIR / "article-with-cdn.html.b64").write_text(b64)
print(f"OK: wrote {out.name}, html_len={len(html)}, b64_len={len(b64)}, images={len(cdn)}")
