#!/usr/bin/env python3
"""Generate Pillar 2 hero cover HTML (1200×630) for Chrome headless render."""
import json
import re
from html import escape
from pathlib import Path

PILLAR = Path(__file__).parent
REG = json.loads((PILLAR / "articles_registry.json").read_text(encoding="utf-8"))

SVG_VARIANTS = [
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1d4ed8"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient></defs><circle cx="280" cy="180" r="48" fill="url(#g)" opacity=".95"/><circle cx="380" cy="280" r="32" fill="#2563eb" opacity=".85"/><circle cx="220" cy="320" r="24" fill="#7c3aed" opacity=".8"/><path d="M280 180 Q340 220 380 280 Q300 300 220 320 Q260 360 340 380" fill="none" stroke="#38bdf8" stroke-width="3" opacity=".85"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#1e40af"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient></defs><polygon points="260,420 180,300 220,300 220,120 300,120 300,300 340,300" fill="url(#g)" opacity=".88"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#1d4ed8"/><stop offset="100%" stop-color="#5b21b6"/></linearGradient></defs><rect x="80" y="220" width="90" height="56" rx="14" fill="url(#g)" opacity=".9"/><rect x="190" y="200" width="90" height="56" rx="14" fill="url(#g)" opacity=".8"/><rect x="300" y="180" width="90" height="56" rx="14" fill="url(#g)" opacity=".72"/><rect x="410" y="160" width="90" height="56" rx="14" fill="url(#g)" opacity=".65"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#1e3a8a"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient></defs><rect x="100" y="280" width="44" height="140" rx="6" fill="url(#g)" opacity=".55"/><rect x="170" y="240" width="44" height="180" rx="6" fill="url(#g)" opacity=".65"/><rect x="240" y="200" width="44" height="220" rx="6" fill="url(#g)" opacity=".75"/><rect x="310" y="160" width="44" height="260" rx="6" fill="url(#g)" opacity=".85"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><circle cx="300" cy="260" r="130" fill="#1d4ed8" opacity=".45"/><circle cx="360" cy="300" r="90" fill="#6d28d9" opacity=".55"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#2563eb"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient></defs><circle cx="300" cy="260" r="36" fill="url(#g)" opacity=".98"/><circle cx="300" cy="140" r="16" fill="#38bdf8" opacity=".9"/><circle cx="420" cy="200" r="14" fill="#818cf8" opacity=".88"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><line x1="200" y1="80" x2="200" y2="440" stroke="#475569" stroke-width="2" opacity=".8"/><circle cx="320" cy="200" r="40" fill="#1d4ed8" opacity=".88"/><circle cx="380" cy="300" r="28" fill="#7c3aed" opacity=".85"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><rect x="120" y="300" width="120" height="80" rx="12" fill="#334155" opacity=".55"/><rect x="300" y="200" width="160" height="200" rx="16" fill="#1d4ed8" opacity=".85"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><polygon points="100,260 130,208 190,208 220,260 190,312 130,312" fill="#334155" opacity=".7"/><polygon points="260,260 290,208 350,208 380,260 350,312 290,312" fill="#2563eb" opacity=".95"/></svg>',
    '<svg viewBox="0 0 520 520" width="520" height="520"><circle cx="280" cy="260" r="140" fill="none" stroke="#2563eb" stroke-width="28" opacity=".55"/><circle cx="280" cy="260" r="36" fill="#7c3aed" opacity=".95"/></svg>',
]

COVER_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:630px;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.cover{display:grid;grid-template-columns:54% 46%;height:100%;background:linear-gradient(145deg,#070b14 0%,#0f172a 38%,#151030 72%,#0c1222 100%)}
.left{padding:52px 40px 52px 64px;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2}
.kicker{display:inline-flex;align-items:center;gap:10px;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#38bdf8;margin-bottom:18px}
.kicker::before{content:"";width:28px;height:2px;background:linear-gradient(90deg,#2563eb,#7c3aed)}
h1{font-size:FSpx;line-height:1.12;font-weight:800;color:#f1f5f9;letter-spacing:-.02em;max-width:580px}
.brand{margin-top:28px;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#475569}
.right{position:relative;overflow:hidden;display:flex;align-items:center;justify-content:flex-end;padding-right:24px}
.right svg{position:relative;z-index:1;filter:drop-shadow(0 0 48px rgba(37,99,235,.55))}
.glow{position:absolute;right:-60px;top:50%;transform:translateY(-50%);width:480px;height:480px;border-radius:50%;background:radial-gradient(circle,rgba(37,99,235,.28) 0%,transparent 72%)}
"""


def title_from_article(folder: str) -> str:
    md = PILLAR / folder / "article.md"
    for line in md.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return folder.replace("-", " ").title()


def hero_html(title: str, kicker: str, variant: int) -> str:
    fs = "38" if len(title) < 55 else ("32" if len(title) < 75 else "28")
    css = COVER_CSS.replace("FS", fs)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="cover"><div class="left"><div class="kicker">{escape(kicker)}</div>
<h1>{escape(title)}</h1><div class="brand">InfiniSynapse · Pillar 2</div></div>
<div class="right"><div class="glow"></div>{SVG_VARIANTS[variant % len(SVG_VARIANTS)]}</div></div></body></html>"""


def main() -> None:
    for i, art in enumerate(REG["articles"]):
        folder = art["folder"]
        title = title_from_article(folder)
        kicker = art.get("kicker", "Comparison · 2026")
        out = PILLAR / folder / "visuals" / "hero.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(hero_html(title, kicker, i), encoding="utf-8")
        print(f"  {folder}/visuals/hero.html")
    print(f"Built {len(REG['articles'])} hero HTML files.")


if __name__ == "__main__":
    main()
