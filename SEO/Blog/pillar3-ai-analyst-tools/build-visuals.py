#!/usr/bin/env python3
"""Generate Pillar 3 hero covers (title + abstract geometry) and body infographics."""
import re
from html import escape
from pathlib import Path

PILLAR = Path(__file__).parent

# Hero titles must match article.md H1 exactly.
HEROES = [
    ("024-best-ai-tools-for-data-analysis", "Best AI Tools for Data Analysis in 2026", "Tools · 2026", 0),
    ("025-ai-data-analysis-tools", "AI Data Analysis Tools: 10 Best Options for Analysts in 2026", "Tools · 2026", 1),
    ("026-sql-data-analysis-tools", "SQL Data Analysis Tools: Best AI Options for 2026 Teams", "SQL Tools", 2),
    ("027-ai-excel-data-analysis-tools", "Best AI Tools for Excel Data Analysis in 2026", "Excel · AI", 3),
    ("028-ai-data-visualization-tools", "Best AI Data Visualization Tools in 2026", "Viz Tools", 4),
    ("029-self-hosted-ai-data-analyst", "Hosted vs Self-Hosted Data Agents: Agentic Data Plane Deployment Guide (2026)", "Deployment", 5),
    ("030-chatgpt-data-analysis-alternatives", "7 Alternatives to ChatGPT for Data Analysis (2026)", "Alternatives", 6),
    ("031-julius-ai-alternatives", "Best Julius AI Alternatives for Spreadsheet Analysis (2026)", "Alternatives", 7),
    ("032-thoughtspot-alternatives", "ThoughtSpot Alternatives: Best AI Data Visualization Tools in 2026", "Alternatives", 8),
    ("033-databricks-genie-alternatives", "Databricks Assistant vs Genie: 6 Alternatives for Lakehouse Teams (2026)", "Alternatives", 9),
    ("034-tableau-pulse-alternatives", "Tableau Pulse Alternatives in 2026: 7 Options for AI Analytics Teams", "Alternatives", 10),
    ("035-perplexity-data-analysis-alternatives", "Perplexity Data Analysis Alternatives in 2026: Research AI vs Dedicated Analytics Tools", "Alternatives", 11),
    ("036-code-interpreter-alternatives", "Enterprise Alternatives to ChatGPT Code Interpreter for Data Analysis (2026)", "Enterprise", 12),
    ("037-infinisynapse-vs-julius-ai", "InfiniSynapse vs Julius AI for Data Analysis (2026): Head-to-Head Across Five Pillars", "Comparison", 13),
    ("038-infinisynapse-vs-chatgpt", "InfiniSynapse vs ChatGPT for Data Analysis in 2026: Which Workflow Wins?", "Comparison", 14),
    ("039-infinisynapse-vs-databricks-genie", "InfiniSynapse vs Databricks Genie: Lakehouse AI Comparison for 2026", "Comparison", 15),
    ("040-julius-ai-vs-chatgpt", "Julius AI vs ChatGPT for Data and File Analysis: 2026 Practical Guide", "Comparison", 16),
    ("041-thoughtspot-vs-databricks-genie", "ThoughtSpot vs Databricks Genie: Neutral AI Analytics Comparison (2026)", "Comparison", 17),
    ("042-infinisynapse-vs-tableau", "InfiniSynapse vs Tableau AI/Pulse: Which Is Better for Analysis Execution?", "Comparison", 18),
    ("043-infinisynapse-review", "InfiniSynapse Review (2026): Honest Scorecard, Pros, Cons, and Buyer Fit", "Review · 2026", 19),
]

SVG_VARIANTS = [
    # 0 nodes — deep blue/violet glow
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1d4ed8"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient><filter id="gl"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><circle cx="280" cy="180" r="48" fill="url(#g)" opacity=".95" filter="url(#gl)"/><circle cx="380" cy="280" r="32" fill="#2563eb" opacity=".85"/><circle cx="220" cy="320" r="24" fill="#7c3aed" opacity=".8"/><circle cx="340" cy="380" r="56" fill="url(#g)" opacity=".75" filter="url(#gl)"/><path d="M280 180 Q340 220 380 280 Q300 300 220 320 Q260 360 340 380" fill="none" stroke="#38bdf8" stroke-width="3" opacity=".85"/></svg>',
    # 1 arrow
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#1e40af"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient></defs><polygon points="260,420 180,300 220,300 220,120 300,120 300,300 340,300" fill="url(#g)" opacity=".88"/><circle cx="260" cy="100" r="18" fill="#a78bfa" opacity=".95"/><circle cx="200" cy="200" r="8" fill="#38bdf8" opacity=".9"/><circle cx="320" cy="240" r="10" fill="#6366f1" opacity=".85"/></svg>',
    # 2 pipeline
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#1d4ed8"/><stop offset="100%" stop-color="#5b21b6"/></linearGradient></defs><rect x="80" y="220" width="90" height="56" rx="14" fill="url(#g)" opacity=".9"/><rect x="190" y="200" width="90" height="56" rx="14" fill="url(#g)" opacity=".8"/><rect x="300" y="180" width="90" height="56" rx="14" fill="url(#g)" opacity=".72"/><rect x="410" y="160" width="90" height="56" rx="14" fill="url(#g)" opacity=".65"/><line x1="170" y1="248" x2="190" y2="228" stroke="#38bdf8" stroke-width="2.5" opacity=".9"/><line x1="280" y1="228" x2="300" y2="208" stroke="#818cf8" stroke-width="2.5" opacity=".9"/><line x1="390" y1="208" x2="410" y2="188" stroke="#38bdf8" stroke-width="2.5" opacity=".9"/></svg>',
    # 3 pillars
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#1e3a8a"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient></defs><rect x="100" y="280" width="44" height="140" rx="6" fill="url(#g)" opacity=".55"/><rect x="170" y="240" width="44" height="180" rx="6" fill="url(#g)" opacity=".65"/><rect x="240" y="200" width="44" height="220" rx="6" fill="url(#g)" opacity=".75"/><rect x="310" y="160" width="44" height="260" rx="6" fill="url(#g)" opacity=".85"/><rect x="380" y="120" width="44" height="300" rx="6" fill="url(#g)" opacity=".95"/><ellipse cx="260" cy="400" rx="200" ry="24" fill="#334155" opacity=".5"/></svg>',
    # 4 prisms
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#2563eb"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient></defs><rect x="120" y="300" width="36" height="120" rx="4" fill="#475569" opacity=".65"/><rect x="170" y="260" width="36" height="160" rx="4" fill="#475569" opacity=".7"/><rect x="220" y="220" width="36" height="200" rx="4" fill="url(#g)" opacity=".85"/><rect x="300" y="280" width="36" height="140" rx="4" fill="#475569" opacity=".6"/><rect x="350" y="200" width="36" height="220" rx="4" fill="url(#g)" opacity=".9"/><rect x="400" y="160" width="36" height="260" rx="4" fill="url(#g)" opacity=".95"/></svg>',
    # 5 ring
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#2563eb"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient></defs><circle cx="280" cy="260" r="140" fill="none" stroke="url(#g)" stroke-width="28" opacity=".55"/><circle cx="280" cy="260" r="90" fill="none" stroke="#818cf8" stroke-width="4" opacity=".75"/><circle cx="280" cy="260" r="36" fill="url(#g)" opacity=".95"/><path d="M420 260 A140 140 0 0 1 280 120" fill="none" stroke="#38bdf8" stroke-width="6" opacity=".9"/></svg>',
    # 6 split
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1d4ed8"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient></defs><line x1="200" y1="80" x2="200" y2="440" stroke="#475569" stroke-width="2" opacity=".8"/><circle cx="320" cy="200" r="40" fill="url(#g)" opacity=".88"/><circle cx="380" cy="300" r="28" fill="#7c3aed" opacity=".85"/><circle cx="300" cy="360" r="52" fill="url(#g)" opacity=".75"/><path d="M320 200 Q360 250 380 300 Q340 330 300 360" fill="none" stroke="#38bdf8" stroke-width="2.5" opacity=".85"/></svg>',
    # 7 lattice
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1e40af"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient></defs><polygon points="280,140 340,200 280,260 220,200" fill="url(#g)" opacity=".9"/><polygon points="360,220 420,280 360,340 300,280" fill="url(#g)" opacity=".78"/><polygon points="200,280 260,340 200,400 140,340" fill="url(#g)" opacity=".65"/><circle cx="280" cy="200" r="60" fill="none" stroke="#38bdf8" stroke-width="2" opacity=".8"/></svg>',
    # 8 layers
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1d4ed8"/><stop offset="100%" stop-color="#5b21b6"/></linearGradient></defs><rect x="120" y="300" width="120" height="80" rx="12" fill="#334155" opacity=".55"/><rect x="140" y="260" width="120" height="80" rx="12" fill="#334155" opacity=".65"/><rect x="160" y="220" width="120" height="80" rx="12" fill="#475569" opacity=".75"/><rect x="300" y="200" width="160" height="200" rx="16" fill="url(#g)" opacity=".85"/><rect x="320" y="230" width="120" height="36" rx="6" fill="#38bdf8" opacity=".35"/><rect x="320" y="280" width="120" height="36" rx="6" fill="#818cf8" opacity=".3"/><rect x="320" y="330" width="120" height="36" rx="6" fill="#a78bfa" opacity=".25"/></svg>',
    # 9 stacks
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#475569"/></linearGradient><linearGradient id="g2" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#1e40af"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient></defs><rect x="160" y="320" width="100" height="24" rx="4" fill="url(#g)" opacity=".75"/><rect x="160" y="280" width="100" height="24" rx="4" fill="url(#g)" opacity=".65"/><rect x="160" y="240" width="100" height="24" rx="4" fill="url(#g)" opacity=".55"/><rect x="300" y="360" width="120" height="24" rx="4" fill="url(#g2)" opacity=".8"/><rect x="300" y="310" width="120" height="24" rx="4" fill="url(#g2)" opacity=".88"/><rect x="300" y="260" width="120" height="24" rx="4" fill="url(#g2)" opacity=".92"/><rect x="300" y="210" width="120" height="24" rx="4" fill="url(#g2)" opacity=".96"/><rect x="300" y="160" width="120" height="24" rx="4" fill="url(#g2)" opacity="1"/></svg>',
    # 10 venn
    '<svg viewBox="0 0 520 520" width="520" height="520"><circle cx="300" cy="260" r="130" fill="#1d4ed8" opacity=".45"/><circle cx="360" cy="300" r="90" fill="#6d28d9" opacity=".55"/><circle cx="320" cy="340" r="14" fill="#38bdf8" opacity=".95"/><circle cx="340" cy="320" r="10" fill="#818cf8" opacity=".9"/><circle cx="360" cy="340" r="8" fill="#a78bfa" opacity=".85"/></svg>',
    # 11 hex chain
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#1d4ed8"/><stop offset="100%" stop-color="#5b21b6"/></linearGradient></defs><polygon points="100,260 130,208 190,208 220,260 190,312 130,312" fill="#334155" opacity=".7"/><polygon points="180,260 210,208 270,208 300,260 270,312 210,312" fill="url(#g)" opacity=".75"/><polygon points="260,260 290,208 350,208 380,260 350,312 290,312" fill="url(#g)" opacity=".85"/><polygon points="340,260 370,208 430,208 460,260 430,312 370,312" fill="url(#g)" opacity=".95"/></svg>',
    # 12 hub
    '<svg viewBox="0 0 520 520" width="520" height="520"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#2563eb"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient></defs><circle cx="300" cy="260" r="36" fill="url(#g)" opacity=".98"/><circle cx="300" cy="140" r="16" fill="#38bdf8" opacity=".9"/><circle cx="420" cy="200" r="14" fill="#818cf8" opacity=".88"/><circle cx="400" cy="340" r="18" fill="#38bdf8" opacity=".9"/><circle cx="220" cy="360" r="12" fill="#a78bfa" opacity=".85"/><circle cx="180" cy="220" r="14" fill="#38bdf8" opacity=".88"/><line x1="300" y1="224" x2="300" y2="156" stroke="#38bdf8" stroke-width="2" opacity=".75"/><line x1="332" y1="248" x2="406" y2="206" stroke="#818cf8" stroke-width="2" opacity=".75"/><line x1="328" y1="284" x2="386" y2="326" stroke="#38bdf8" stroke-width="2" opacity=".75"/><line x1="272" y1="288" x2="228" y2="348" stroke="#a78bfa" stroke-width="2" opacity=".75"/><line x1="268" y1="240" x2="192" y2="222" stroke="#38bdf8" stroke-width="2" opacity=".75"/></svg>',
]

COVER_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:630px;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.cover{display:grid;grid-template-columns:54% 46%;height:100%;background:linear-gradient(145deg,#070b14 0%,#0f172a 38%,#151030 72%,#0c1222 100%)}
.left{padding:52px 40px 52px 64px;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2}
.kicker{display:inline-flex;align-items:center;gap:10px;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#38bdf8;margin-bottom:18px}
.kicker::before{content:"";width:28px;height:2px;background:linear-gradient(90deg,#2563eb,#7c3aed)}
h1{font-size:FSpx;line-height:1.12;font-weight:800;color:#f1f5f9;letter-spacing:-.02em;max-width:580px;text-shadow:0 2px 24px rgba(15,23,42,.6)}
.accent{background:linear-gradient(90deg,#60a5fa,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.brand{margin-top:28px;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#475569}
.right{position:relative;overflow:hidden;display:flex;align-items:center;justify-content:flex-end;padding-right:24px}
.right::before{content:"";position:absolute;inset:0;background:linear-gradient(rgba(37,99,235,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(37,99,235,.08) 1px,transparent 1px);background-size:28px 28px;mask-image:linear-gradient(90deg,transparent,black 30%);-webkit-mask-image:linear-gradient(90deg,transparent,black 30%)}
.right svg{position:relative;z-index:1;filter:drop-shadow(0 0 48px rgba(37,99,235,.55)) drop-shadow(0 0 24px rgba(109,40,217,.4))}
.glow{position:absolute;right:-60px;top:50%;transform:translateY(-50%);width:480px;height:480px;border-radius:50%;background:radial-gradient(circle,rgba(37,99,235,.28) 0%,rgba(109,40,217,.14) 45%,transparent 72%);pointer-events:none}
"""

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:Wpx;height:Hpx;background:linear-gradient(180deg,#f8fafc 0%,#eef2ff 100%);color:#0f172a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;overflow:hidden;padding:36px 44px}
.badge{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#e0f2fe;background:linear-gradient(135deg,#1e3a8a,#312e81);border:1px solid #3730a3;padding:4px 10px;border-radius:4px;margin-bottom:10px}
h1{font-size:FSpx;line-height:1.15;font-weight:700;margin-bottom:6px;color:#0c1222}
.sub{font-size:14px;color:#475569;margin-bottom:18px}
table{width:100%;border-collapse:collapse;font-size:12px}
th,td{border:1px solid #cbd5e1;padding:8px 10px;text-align:left;vertical-align:top}
th{background:linear-gradient(180deg,#1e3a8a,#1e40af);color:#e0f2fe;font-weight:600}
td{color:#1e293b;background:#f8fafc}
.yes{color:#047857;font-weight:700}.no{color:#64748b}.partial{color:#b45309}
.best{background:#dbeafe;color:#1e3a8a;font-weight:700}
.flow{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:12px}
.node{padding:10px 14px;background:linear-gradient(135deg,#dbeafe,#e0e7ff);border:1px solid #3b82f6;border-radius:8px;font-size:12px;font-weight:600;color:#1e40af}
.arr{color:#4338ca;font-size:18px;font-weight:700}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.card{border:1px solid #94a3b8;border-radius:10px;padding:16px;background:#f1f5f9}
.card h3{font-size:14px;color:#1e40af;margin-bottom:8px}
.card p,.card li{font-size:12px;color:#334155;line-height:1.45}
.cols3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.col h4{font-size:13px;color:#1e3a8a;margin-bottom:8px;border-bottom:2px solid #6366f1;padding-bottom:4px}
.ul{margin:0;padding-left:16px}
.stack{display:flex;flex-direction:column;gap:8px;margin-top:10px}
.layer{padding:12px 16px;border-radius:8px;border:1px solid #6366f1;font-size:12px;font-weight:600}
.l1{background:linear-gradient(90deg,#dbeafe,#c7d2fe);color:#1e3a8a}.l2{background:linear-gradient(90deg,#ccfbf1,#a7f3d0);color:#065f46}.l3{background:#e2e8f0;color:#1e293b}
"""


def page(w, h, fs, body, title=""):
    css = CSS.replace("W", str(w)).replace("H", str(h)).replace("FS", str(fs))
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'


def write(rel, content):
    p = PILLAR / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  {rel}")


def title_font_size(title: str) -> int:
    n = len(title)
    if n <= 42:
        return 42
    if n <= 58:
        return 36
    if n <= 72:
        return 32
    return 28


def hero_cover(title: str, kicker: str, variant: int) -> str:
    fs = title_font_size(title)
    css = COVER_CSS.replace("FS", str(fs))
    svg = SVG_VARIANTS[variant % len(SVG_VARIANTS)]
    return (
        f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        f'<style>{css}</style></head><body>'
        f'<div class="cover"><div class="left">'
        f'<div class="kicker">{escape(kicker)}</div>'
        f'<h1>{escape(title)}</h1>'
        f'<div class="brand">InfiniSynapse</div>'
        f'</div><div class="right"><div class="glow"></div>{svg}</div></div>'
        f'</body></html>'
    )


for folder, title, kicker, variant in HEROES:
    write(f"{folder}/visuals/hero.html", hero_cover(title, kicker, variant))

def refresh_existing_body_styles() -> None:
    """Re-apply CSS to body HTML files not rebuilt above."""
    style_re = re.compile(r"<style>.*?</style>", re.DOTALL)
    for path in sorted(PILLAR.glob("**/visuals/*.html")):
        if path.name == "hero.html":
            continue
        text = path.read_text(encoding="utf-8")
        dims = re.search(r"width:(\d+)px;height:(\d+)px", text)
        fs_m = re.search(r"h1\{font-size:(\d+)px", text)
        if not dims:
            continue
        w, h, fs = dims.group(1), dims.group(2), (fs_m.group(1) if fs_m else "26")
        new_style = f"<style>{CSS.replace('W', w).replace('H', h).replace('FS', fs)}</style>"
        path.write_text(style_re.sub(new_style, text, count=1), encoding="utf-8")
        print(f"  refreshed {path.relative_to(PILLAR)}")


BODY_VISUALS = [
    (
        "039-infinisynapse-vs-databricks-genie/visuals/lakehouse-decision.html",
        1200,
        680,
        26,
        '<span class="badge">Decision View</span>'
        "<h1>Lakehouse Path — Databricks-native vs Cross-source Agent</h1>"
        '<p class="sub">Choose by data topology and who needs answers outside the workspace.</p>'
        '<div class="grid2">'
        '<div class="card"><h3>Path A · Databricks-native</h3>'
        "<ul class='ul'><li>Delta + Unity Catalog is system of record</li>"
        "<li>Analysts work inside Databricks UI</li>"
        "<li>NL exploration over governed assets</li></ul>"
        '<p><strong>Best fit:</strong> Databricks Genie</p></div>'
        '<div class="card"><h3>Path B · Cross-source execution</h3>'
        "<ul class='ul'><li>KPIs span lakehouse + ops DB + files</li>"
        "<li>Business users need web/chat/API parity</li>"
        "<li>Recurring workflows need memory cards</li></ul>"
        '<p><strong>Best fit:</strong> InfiniSynapse Data Agent</p></div>'
        "</div>"
        '<div class="flow" style="margin-top:20px">'
        '<span class="node">Business question</span><span class="arr">→</span>'
        '<span class="node">Single lakehouse?</span><span class="arr">→</span>'
        '<span class="node">Genie</span>'
        '<span class="arr" style="margin-left:24px">↘</span>'
        '<span class="node">Multi-source + recurring?</span><span class="arr">→</span>'
        '<span class="node">Data Agent</span>'
        "</div>",
    ),
    (
        "040-julius-ai-vs-chatgpt/visuals/decision-flow.html",
        1200,
        720,
        26,
        '<span class="badge">Decision Flow</span>'
        "<h1>Julius AI vs ChatGPT — Pick by Workflow Type</h1>"
        '<p class="sub">File-first speed vs cross-functional breadth.</p>'
        '<div class="flow" style="margin-bottom:16px">'
        '<span class="node">Analyst task</span><span class="arr">→</span>'
        '<span class="node">Primary input?</span>'
        "</div>"
        "<table>"
        "<tr><th>Workflow signal</th><th>Julius AI</th><th>ChatGPT</th></tr>"
        "<tr><td>Tabular file upload → first chart</td><td class='best'>Faster onboarding</td><td>Flexible, more prompt variance</td></tr>"
        "<tr><td>Executive memo + SQL draft same thread</td><td class='partial'>Analysis-centric</td><td class='best'>Cross-functional utility</td></tr>"
        "<tr><td>Recurring monthly KPI on same file</td><td class='partial'>Manual re-upload</td><td class='partial'>Re-prompt / custom GPT</td></tr>"
        "<tr><td>Multi-role org (PM + analyst + eng)</td><td>Analyst pod</td><td class='best'>Broader adoption</td></tr>"
        "</table>"
        '<p class="sub" style="margin-top:14px">Weight <strong>memory</strong> and <strong>repeatability</strong> heavily for production habits.</p>',
    ),
    (
        "041-thoughtspot-vs-databricks-genie/visuals/decision-chart.html",
        1200,
        680,
        26,
        '<span class="badge">Decision Chart</span>'
        "<h1>ThoughtSpot vs Databricks Genie — Stack &amp; User Fit</h1>"
        '<p class="sub">Match product to where data contracts already live.</p>'
        "<table>"
        "<tr><th>If your reality is…</th><th>ThoughtSpot</th><th>Databricks Genie</th></tr>"
        "<tr><td>BI consumers need search UX at scale</td><td class='best'>Primary surface</td><td>Workspace-native</td></tr>"
        "<tr><td>Unity Catalog is governance standard</td><td>Connected sources + semantic layer</td><td class='best'>Native UC lineage</td></tr>"
        "<tr><td>Embedded analytics in customer apps</td><td class='best'>Mature embed patterns</td><td class='partial'>Evolving</td></tr>"
        "<tr><td>Analyst-engineer handoff in one workspace</td><td class='partial'>BI + engineering split</td><td class='best'>Single lakehouse workspace</td></tr>"
        "<tr><td>Cross-system orchestration outside estate</td><td class='partial'>Model boundaries</td><td class='no'>Databricks-first</td></tr>"
        "</table>",
    ),
    (
        "042-infinisynapse-vs-tableau/visuals/matrix.html",
        1200,
        680,
        26,
        '<span class="badge">Execution Matrix</span>'
        "<h1>Dashboard-AI Path vs Execution-Agent Path</h1>"
        '<p class="sub">Consumption layer vs multi-step analysis execution.</p>'
        '<div class="cols3">'
        '<div class="col"><h4>Tableau AI / Pulse</h4><ul class="ul">'
        "<li>Monitor modeled metrics</li><li>Pulse summaries &amp; anomalies</li>"
        "<li>Fast insight inside dashboards</li><li>BI-consumer UX</li></ul></div>"
        '<div class="col"><h4>Shared overlap</h4><ul class="ul">'
        "<li>Natural-language questions</li><li>Governed semantic context</li>"
        "<li>Executive-friendly delivery</li></ul></div>"
        '<div class="col"><h4>InfiniSynapse</h4><ul class="ul">'
        "<li>Goal-led multi-step runs</li><li>Cross-source orchestration</li>"
        "<li>SQL + source trace timeline</li><li>Memory cards across cycles</li></ul></div>"
        "</div>"
        "<table style='margin-top:16px'>"
        "<tr><th>Bottleneck</th><th>Choose</th></tr>"
        "<tr><td>KPI monitoring inside Tableau estate</td><td class='best'>Tableau Pulse</td></tr>"
        "<tr><td>Recurring cross-source execution workflows</td><td class='best'>InfiniSynapse</td></tr>"
        "</table>",
    ),
    (
        "043-infinisynapse-review/visuals/five-pillars-radar.html",
        1200,
        720,
        26,
        '<span class="badge">Scorecard</span>'
        "<h1>InfiniSynapse Review — Five-Pillar Radar</h1>"
        '<p class="sub">Directional scores for recurring operational analytics (10-point scale).</p>'
        "<table>"
        "<tr><th>Pillar</th><th>Score</th><th>Weight</th><th>Weighted</th><th>Signal</th></tr>"
        "<tr><td>Autonomy</td><td class='best'>9.0</td><td>25%</td><td>2.25</td><td>Multi-step from one goal</td></tr>"
        "<tr><td>Transparency</td><td class='best'>9.2</td><td>20%</td><td>1.84</td><td>Task timeline + SQL trace</td></tr>"
        "<tr><td>Memory</td><td class='best'>9.1</td><td>25%</td><td>2.28</td><td>Distilled cards across runs</td></tr>"
        "<tr><td>Multi-entry</td><td class='best'>9.0</td><td>15%</td><td>1.35</td><td>Web + chat + API parity</td></tr>"
        "<tr><td>Self-correction</td><td class='partial'>8.6</td><td>15%</td><td>1.29</td><td>Reroute on schema drift</td></tr>"
        "</table>"
        '<p class="sub" style="margin-top:12px"><strong>Composite: 9.0/10</strong> · Overall product rating <strong>4.5/5</strong> — run your own pilot before procurement.</p>',
    ),
]

for rel, w, h, fs, body in BODY_VISUALS:
    write(rel, page(w, h, fs, body))

refresh_existing_body_styles()
print(f"Built 20 hero covers + {len(BODY_VISUALS)} body infographics.")
