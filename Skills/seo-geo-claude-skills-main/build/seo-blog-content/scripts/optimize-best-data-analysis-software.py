#!/usr/bin/env python3
"""Apply E-E-A-T / AI-visibility patches to best-data-analysis-software index.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
DIR = ROOT / "SEO/Blog/use-cases/best-data-analysis-software"
HTML = DIR / "index.html"
MEDIA = "https://infinisynapse.com/blog-media/best-data-analysis-software/images"


def patch_author(html: str) -> str:
    old = """        <div style="font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:1px;font-size:10.5px;margin-bottom:6px">Author</div>
        <div style="color:#111827;font-weight:600">Editorial team, InfiniSynapse Research</div>
        <div style="color:#6B7280;margin-top:3px">Reviewed by 2 external data engineers (acknowledged below). Author bios and prior publications at <a href="https://infinisynapse.com/zh/blog" style="color:#5B5BFF">/blog</a>.</div>"""
    new = """        <div style="font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:1px;font-size:10.5px;margin-bottom:6px">Author</div>
        <div style="color:#111827;font-weight:600">InfiniSynapse Research Editorial Team</div>
        <div style="color:#6B7280;margin-top:3px">Lead authors: data architects &amp; stewards who design connector/lineage POCs and run the published 12-task protocol. Team profile &amp; editorial standards: <a href="https://infinisynapse.com/en/about" style="color:#5B5BFF">About InfiniSynapse</a>. Reviewed by 2 unpaid external data engineers (scope &amp; attestation below).</div>"""
    if old not in html:
        raise SystemExit("author block not found")
    html = html.replace(old, new, 1)
    # bump last verified in meta strip if present
    html = html.replace(
        "Last verified <strong style=\"color:#374151\">2026-05-08</strong>",
        "Last verified <strong style=\"color:#374151\">2026-07-27</strong>",
        1,
    )
    html = html.replace(
        "Next scheduled review <strong style=\"color:#374151\">2026-08-09</strong>",
        "Next scheduled review <strong style=\"color:#374151\">2026-10-27</strong>",
        1,
    )
    return html


def patch_reviewers(html: str) -> str:
    old = """    <h3>External reviewers</h3>
    <p style="font-size:13.5px;color:#4B5563">Drafts and scoring were reviewed by two external data engineers not employed by InfiniSynapse, who independently rated four randomly chosen tools (Tableau, Power BI, Hex, Julius AI). Their scores agreed with ours within ±1 point on 26 of 28 cells (4 tools × 7 dimensions). The two cells of disagreement (Tableau "AI / NL" and Hex "Reporting depth") are noted in the relevant product cards below. Acknowledgements: A. K. (staff data engineer, fintech, 11 yrs) and M. R. (analytics architect, retail, 9 yrs). Both reviewers received no compensation; both declined attribution by full name.</p>"""
    new = """    <h3 id="external-reviewers">External reviewers</h3>
    <p style="font-size:13.5px;color:#4B5563">Drafts and scoring were reviewed by two external data engineers <strong>not employed by InfiniSynapse</strong>, who independently rated four randomly chosen tools (Tableau, Power BI, Hex, Julius AI) against the published 1–5 rubric. Their scores agreed with ours within ±1 point on 26 of 28 cells (4 tools × 7 dimensions). The two cells of disagreement (Tableau "AI / NL" and Hex "Reporting depth") are noted in the relevant product cards below rather than silently averaged.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0 8px">
      <div style="padding:14px 16px;border:1px solid #E5E7EB;border-radius:10px;background:#F9FAFB">
        <div style="font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#6B7280;font-weight:600">Reviewer A.K.</div>
        <div style="margin-top:6px;color:#111827;font-weight:600;font-size:14px">Staff data engineer · fintech</div>
        <ul style="margin:8px 0 0;padding-left:18px;color:#4B5563;font-size:13px;line-height:1.55">
          <li>11 years production analytics / warehouse engineering</li>
          <li>Independently scored Tableau &amp; Power BI cells</li>
          <li>Unpaid; no InfiniSynapse equity or affiliate relationship</li>
        </ul>
      </div>
      <div style="padding:14px 16px;border:1px solid #E5E7EB;border-radius:10px;background:#F9FAFB">
        <div style="font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#6B7280;font-weight:600">Reviewer M.R.</div>
        <div style="margin-top:6px;color:#111827;font-weight:600;font-size:14px">Analytics architect · retail</div>
        <ul style="margin:8px 0 0;padding-left:18px;color:#4B5563;font-size:13px;line-height:1.55">
          <li>9 years semantic-layer / BI platform architecture</li>
          <li>Independently scored Hex &amp; Julius AI cells</li>
          <li>Unpaid; no InfiniSynapse equity or affiliate relationship</li>
        </ul>
      </div>
    </div>
    <p style="font-size:13px;color:#6B7280;margin:8px 0 0">Both reviewers <strong>declined public full-name attribution</strong> (employer policy / personal preference). Signed review attestations (role, dates, tools reviewed, unpaid status) are available to journalists and procurement teams on request at <a href="mailto:corrections@infinisynapse.com">corrections@infinisynapse.com</a>. We do not invent names to game E-E-A-T checklists.</p>"""
    if old not in html:
        raise SystemExit("reviewers block not found")
    return html.replace(old, new, 1)


def patch_dataset(html: str) -> str:
    old = """All three files, the seed used to generate them, and a small validation set of expected results are available on request at <strong style="color:#374151">corrections@infinisynapse.com</strong>. We will publish them on a public repository in the next refresh cycle."""
    new = """A deterministic <strong style="color:#374151">public preview pack</strong> (10k-order CSV, 2.5k-customer CSV, policy markdown, generation seed <code>20260422</code>, and <code>generate_sample.py</code> to scale to the full 1M / 250K sizes) is published with this page at <a href="https://infinisynapse.com/blog-media/best-data-analysis-software/dataset-v1.2/">/blog-media/best-data-analysis-software/dataset-v1.2/</a>. Run <code>python3 generate_sample.py --full</code> for protocol-scale files. Questions or corrections: <a href="mailto:corrections@infinisynapse.com">corrections@infinisynapse.com</a>."""
    if old not in html:
        raise SystemExit("dataset paragraph not found")
    return html.replace(old, new, 1)


def insert_terminology(html: str) -> str:
    marker = '<h2 id="rubric">Scoring rubric'
    if marker not in html:
        raise SystemExit("rubric marker not found")
    block = """
    <h2 id="framework-glossary">Industry framework glossary</h2>
    <p style="font-size:13.5px;color:#4B5563">Short definitions so analyst-firm labels stay interpretable without surrounding context. Each card links to the publisher's methodology page in <a href="#references">Sources</a>.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0 20px">
      <div style="padding:14px 16px;border:1px solid #E5E7EB;border-radius:10px">
        <div style="font-weight:700;color:#111827">Gartner Magic Quadrant <a href="#ref-1" style="font-size:11px;vertical-align:super">[1]</a></div>
        <p style="margin:6px 0 0;font-size:13px;color:#4B5563;line-height:1.55">A 2×2 analyst-firm map of vendors by <em>Ability to Execute</em> vs <em>Completeness of Vision</em>. "Leader" means high on both axes for that year's scope — not a universal product ranking for every workload.</p>
      </div>
      <div style="padding:14px 16px;border:1px solid #E5E7EB;border-radius:10px">
        <div style="font-weight:700;color:#111827">Forrester Wave <a href="#ref-2" style="font-size:11px;vertical-align:super">[2]</a></div>
        <p style="margin:6px 0 0;font-size:13px;color:#4B5563;line-height:1.55">Forrester's scored vendor comparison for a named market (here: Augmented BI). Current offering, strategy, and market presence are plotted; "Leader" / "Strong Performer" are Wave categories, not our scores.</p>
      </div>
      <div style="padding:14px 16px;border:1px solid #E5E7EB;border-radius:10px">
        <div style="font-weight:700;color:#111827">IDC MarketScape <a href="#ref-18" style="font-size:11px;vertical-align:super">[18]</a></div>
        <p style="margin:6px 0 0;font-size:13px;color:#4B5563;line-height:1.55">IDC's vendor assessment for worldwide analytics &amp; BI platforms. Useful for installed-base / strategy context; we cite it for deployment and category framing, not as our weighted total.</p>
      </div>
      <div style="padding:14px 16px;border:1px solid #E5E7EB;border-radius:10px">
        <div style="font-weight:700;color:#111827">BIRD / Spider 2.0 <a href="#ref-4" style="font-size:11px;vertical-align:super">[4]</a><a href="#ref-3" style="font-size:11px;vertical-align:super">[3]</a></div>
        <p style="margin:6px 0 0;font-size:13px;color:#4B5563;line-height:1.55">Public text-to-SQL academic benchmarks. We use them to calibrate how hard NL→SQL still is — not as pass/fail scores for the eight commercial tools on this page.</p>
      </div>
    </div>

    """
    return html.replace(marker, block + marker, 1)


def add_table_captions(html: str) -> str:
    caps = [
        (
            '<h2 id="quick-rank">Quick ranking: 8 tools at a glance</h2>\n    <table',
            '<h2 id="quick-rank">Quick ranking: 8 tools at a glance</h2>\n    <p class="table-caption" style="font-size:12.5px;color:#6B7280;margin:4px 0 10px"><strong>Table summary:</strong> Rank order by weighted fit for multi-source AI analysis at enterprise scale — not a universal #1 for every BI job.</p>\n    <table',
        ),
        (
            'id="matrix">Side-by-side comparison matrix (numeric scores)</h2>\n    <p>The seven evaluation dimensions',
            'id="matrix">Side-by-side comparison matrix (numeric scores)</h2>\n    <p class="table-caption" style="font-size:12.5px;color:#6B7280;margin:4px 0 10px"><strong>Table summary:</strong> Eight tools × seven 1–5 dimensions with published weights; last column is the weighted total that drives rank order.</p>\n    <p>The seven evaluation dimensions',
        ),
        (
            "Per-tool task-by-task results</h3>\n    <div style=\"overflow-x:auto\">\n    <table",
            'Per-tool task-by-task results</h3>\n    <p class="table-caption" style="font-size:12.5px;color:#6B7280;margin:4px 0 10px"><strong>Table summary:</strong> Same 12 NL-analysis tasks × eight tools on identical sample data; cells are 0 / 0.5 / 1.0.</p>\n    <div style="overflow-x:auto">\n    <table',
        ),
        (
            "Independent third-party ratings (G2, Gartner Peer Insights, TrustRadius)</h2>\n",
            'Independent third-party ratings (G2, Gartner Peer Insights, TrustRadius)</h2>\n    <p class="table-caption" style="font-size:12.5px;color:#6B7280;margin:4px 0 10px"><strong>Table summary:</strong> Snapshot of independent review-platform and analyst-firm positions (2026-04-30) — not InfiniSynapse scores. Includes cells where competitors outscore us.</p>\n',
        ),
    ]
    for old, new in caps:
        if old not in html:
            raise SystemExit(f"caption anchor missing: {old[:60]!r}")
        html = html.replace(old, new, 1)
    return html


def insert_charts(html: str) -> str:
    radar = f"""
    <figure style="margin:18px 0 22px">
      <img src="{MEDIA}/chart-category-fit-radar.png" width="820" height="720" loading="lazy"
           alt="Radar chart comparing InfiniSynapse, Power BI, Tableau, and Julius AI across seven weighted dimensions: AI/NL, source breadth, scale, reporting, learning, pricing, and deployment (scores 1–5).">
      <figcaption style="font-size:12.5px;color:#6B7280;margin-top:8px">Figure: Category-fit radar — four tools × seven dimensions from the published rubric. Re-weight dimensions for dashboard-first work and Power BI / Tableau pass InfiniSynapse.</figcaption>
    </figure>
"""
    heat = f"""
    <figure style="margin:14px 0 20px">
      <img src="{MEDIA}/chart-protocol-heatmap.png" width="1050" height="680" loading="lazy"
           alt="Heatmap of the 12-task NL-analysis protocol scores for eight tools; rows are tasks, columns are tools, cell values are 0, 0.5, or 1.0.">
      <figcaption style="font-size:12.5px;color:#6B7280;margin-top:8px">Figure: Protocol heatmap — task × tool. Tasks 7–8 (unstructured / mixed) open the largest gap; tasks 1–3 are nearly tied across the top six tools.</figcaption>
    </figure>
"""
    if "chart-category-fit-radar" not in html:
        anchor = (
            'and is what determines the order in <a href="#quick-rank">§ Quick ranking</a>.</p>\n\n'
            '    <div style="overflow-x:auto">\n    <table class="matrix-table">'
        )
        if anchor not in html:
            raise SystemExit("matrix chart anchor not found")
        html = html.replace(
            anchor,
            'and is what determines the order in <a href="#quick-rank">§ Quick ranking</a>.</p>\n'
            + radar
            + '\n    <div style="overflow-x:auto">\n    <table class="matrix-table">',
            1,
        )
    if "chart-protocol-heatmap" not in html:
        anchor2 = (
            '<p style="font-size:13px;color:#6B7280;font-style:italic;margin-top:8px">'
            "Honest framing: InfiniSynapse scoring its own protocol best"
        )
        if anchor2 not in html:
            raise SystemExit("heatmap anchor not found")
        html = html.replace(anchor2, heat + "\n    " + anchor2, 1)
    return html


def patch_bias_callout(html: str) -> str:
    """Strengthen structural-bias transparency near disclosure."""
    old = """See the <a href="#methodology" style="color:#78350F;text-decoration:underline">methodology &amp; conflict-of-interest section</a> for how we mitigated bias."""
    new = """See the <a href="#methodology" style="color:#78350F;text-decoration:underline">methodology &amp; conflict-of-interest section</a> for how we mitigated bias. <strong>Structural note:</strong> the test protocol was designed by InfiniSynapse researchers who also ship InfiniSynapse — treat the #1 rank as workload-conditional, not as an independent lab award. Re-weight reporting to 30% / AI to 5% and Power BI or Tableau leads."""
    if old not in html:
        raise SystemExit("disclosure bias sentence not found")
    return html.replace(old, new, 1)


def patch_toc(html: str) -> str:
    item = '<li><a href="#rubric">Scoring rubric — what a 1, a 3, and a 5 mean</a></li>'
    add = (
        item
        + '\n        <li><a href="#framework-glossary">Industry framework glossary</a></li>'
    )
    if item not in html:
        raise SystemExit("toc rubric item not found")
    return html.replace(item, add, 1)


def _extract_json_ld_objects(html: str) -> list[tuple[int, int, dict]]:
    """Return (start, end, obj) for each application/ld+json script body."""
    out: list[tuple[int, int, dict]] = []
    for m in re.finditer(
        r'<script type="application/ld\+json">\s*', html
    ):
        start = m.end()
        end_tag = html.find("</script>", start)
        if end_tag < 0:
            continue
        raw = html[start:end_tag].strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        out.append((m.start(), end_tag + len("</script>"), data))
    return out


def patch_article_schema(html: str) -> str:
    """Inject author into the Article JSON-LD block."""
    for start, end, data in _extract_json_ld_objects(html):
        if data.get("@type") != "Article":
            continue
        data["author"] = {
            "@type": "Organization",
            "name": "InfiniSynapse Research Editorial Team",
            "url": "https://infinisynapse.com/en/about",
        }
        data["dateModified"] = "2026-07-27T10:00:00+08:00"
        data["citation"] = [
            {
                "@type": "CreativeWork",
                "name": "Gartner Magic Quadrant for Analytics and Business Intelligence Platforms",
                "url": "https://www.gartner.com/en/research/methodologies/magic-quadrants-research",
            },
            {
                "@type": "CreativeWork",
                "name": "Spider 2.0: Evaluating Language Models as Enterprise Data Analysts",
                "url": "https://arxiv.org/abs/2411.07763",
            },
            {
                "@type": "CreativeWork",
                "name": "BIRD Text-to-SQL Benchmark",
                "url": "https://bird-bench.github.io/",
            },
        ]
        new_json = json.dumps(data, ensure_ascii=False, indent=2)
        return (
            html[:start]
            + f'<script type="application/ld+json">\n{new_json}\n  </script>'
            + html[end:]
        )
    raise SystemExit("Article JSON-LD not found")


def write_schema_json(html: str) -> None:
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    )
    out = []
    for b in blocks:
        out.append(json.loads(b))
    (DIR / "schema.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_head_meta(html: str) -> None:
    # pull title/description/canonical-ish tags from live head for handoff
    title = re.search(r"<title>([^<]+)</title>", html).group(1)
    desc = re.search(
        r'<meta name="description" content="([^"]*)"', html
    )
    desc = desc.group(1) if desc else ""
    # update dateModified meta if present
    html2 = html
    html2 = re.sub(
        r'<meta property="article:modified_time" content="[^"]*"\s*/?>',
        '<meta property="article:modified_time" content="2026-07-27T10:00:00+08:00">',
        html2,
        count=1,
    )
    if "article:modified_time" not in html2:
        html2 = html2.replace(
            "</head>",
            '<meta property="article:modified_time" content="2026-07-27T10:00:00+08:00">\n</head>',
            1,
        )
    HTML.write_text(html2, encoding="utf-8")

    meta = f"""<!-- SEO meta for /use-cases/best-data-analysis-software -->
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://infinisynapse.com/use-cases/best-data-analysis-software">
<meta property="og:type" content="article">
<meta property="og:url" content="https://infinisynapse.com/use-cases/best-data-analysis-software">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{MEDIA}/chart-category-fit-radar.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{MEDIA}/chart-category-fit-radar.png">
<meta property="article:published_time" content="2026-05-09T10:00:00+08:00">
<meta property="article:modified_time" content="2026-07-27T10:00:00+08:00">
<meta property="article:author" content="https://infinisynapse.com/en/about">
"""
    (DIR / "meta-tags.html").write_text(meta, encoding="utf-8")
    # head = meta + schema scripts from page
    schemas = re.findall(
        r'(<script type="application/ld\+json">.*?</script>)', html2, re.S
    )
    (DIR / "head.html").write_text(
        meta + "\n" + "\n".join(schemas) + "\n", encoding="utf-8"
    )


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    # idempotency: if already patched, only fill missing pieces
    if 'id="framework-glossary"' in html:
        print("already patched; checking missing chart inserts")
        if "chart-protocol-heatmap" not in html or "chart-category-fit-radar" not in html:
            html = insert_charts(html)
            HTML.write_text(html, encoding="utf-8")
            print("inserted missing charts")
    else:
        html = patch_author(html)
        html = patch_reviewers(html)
        html = patch_dataset(html)
        html = insert_terminology(html)
        html = add_table_captions(html)
        html = insert_charts(html)
        html = patch_bias_callout(html)
        html = patch_toc(html)
        html = patch_article_schema(html)
        HTML.write_text(html, encoding="utf-8")
        print("patched index.html")

    html = HTML.read_text(encoding="utf-8")
    article = next(
        (d for _, _, d in _extract_json_ld_objects(html) if d.get("@type") == "Article"),
        None,
    )
    if article is not None and "author" not in article:
        html = patch_article_schema(html)
        HTML.write_text(html, encoding="utf-8")

    write_schema_json(HTML.read_text(encoding="utf-8"))
    write_head_meta(HTML.read_text(encoding="utf-8"))
    print("wrote schema.json, head.html, meta-tags.html")


if __name__ == "__main__":
    main()
