#!/usr/bin/env bash
# Pillar 3 · Hero covers HTML→PNG
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar3-ai-analyst-tools"
CHROME=""
for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"   "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"; do
  [[ -x "$p" ]] && CHROME="$p" && break
done
[[ -n "$CHROME" ]] || { echo "❌ Chrome not found"; exit 1; }

render() {
  local label="$1" html="$2" png="$3" w="${4:-1200}" h="${5:-630}"
  [[ -f "$html" ]] || { echo "SKIP $label"; return; }
  mkdir -p "$(dirname "$png")"
  echo "▶ $label (${w}×${h})"
  "$CHROME" --headless=new --hide-scrollbars --disable-gpu \
    --force-device-scale-factor=2 --window-size="${w},${h}" \
    --screenshot="$png" --default-background-color=ffffffff \
    "file://$html" >/dev/null 2>&1
  if [[ -f "$png" ]]; then
    echo "  ✅ $(basename "$png")"
    cp -f "$png" "$(dirname "$png")/og-cover.png"
  fi
}

while IFS='|' read -r slug html png w h; do
  [[ "$slug" == \#* || -z "$slug" ]] && continue
  render "$slug" "$PILLAR/$html" "$PILLAR/$png" "${w:-1200}" "${h:-630}"
done <<'JOBS'
# Heroes — 1200×630
024-hero|024-best-ai-tools-for-data-analysis/visuals/hero.html|024-best-ai-tools-for-data-analysis/images/hero-best-ai-tools-for-data-analysis.png|1200|630
025-hero|025-ai-data-analysis-tools/visuals/hero.html|025-ai-data-analysis-tools/images/hero-ai-data-analysis-tools.png|1200|630
026-hero|026-sql-data-analysis-tools/visuals/hero.html|026-sql-data-analysis-tools/images/hero-sql-data-analysis-tools.png|1200|630
027-hero|027-ai-excel-data-analysis-tools/visuals/hero.html|027-ai-excel-data-analysis-tools/images/hero-ai-excel-data-analysis-tools.png|1200|630
028-hero|028-ai-data-visualization-tools/visuals/hero.html|028-ai-data-visualization-tools/images/hero-ai-data-visualization-tools.png|1200|630
029-hero|029-self-hosted-ai-data-analyst/visuals/hero.html|029-self-hosted-ai-data-analyst/images/hero-self-hosted-ai-data-analyst.png|1200|630
030-hero|030-chatgpt-data-analysis-alternatives/visuals/hero.html|030-chatgpt-data-analysis-alternatives/images/hero-chatgpt-data-analysis-alternatives.png|1200|630
031-hero|031-julius-ai-alternatives/visuals/hero.html|031-julius-ai-alternatives/images/hero-julius-ai-alternatives.png|1200|630
032-hero|032-thoughtspot-alternatives/visuals/hero.html|032-thoughtspot-alternatives/images/hero-thoughtspot-alternatives.png|1200|630
033-hero|033-databricks-genie-alternatives/visuals/hero.html|033-databricks-genie-alternatives/images/hero-databricks-genie-alternatives.png|1200|630
034-hero|034-tableau-pulse-alternatives/visuals/hero.html|034-tableau-pulse-alternatives/images/hero-tableau-pulse-alternatives.png|1200|630
035-hero|035-perplexity-data-analysis-alternatives/visuals/hero.html|035-perplexity-data-analysis-alternatives/images/hero-perplexity-data-analysis-alternatives.png|1200|630
036-hero|036-code-interpreter-alternatives/visuals/hero.html|036-code-interpreter-alternatives/images/hero-code-interpreter-alternatives.png|1200|630
037-hero|037-infinisynapse-vs-julius-ai/visuals/hero.html|037-infinisynapse-vs-julius-ai/images/hero-infinisynapse-vs-julius-ai.png|1200|630
038-hero|038-infinisynapse-vs-chatgpt/visuals/hero.html|038-infinisynapse-vs-chatgpt/images/hero-infinisynapse-vs-chatgpt.png|1200|630
039-hero|039-infinisynapse-vs-databricks-genie/visuals/hero.html|039-infinisynapse-vs-databricks-genie/images/hero-infinisynapse-vs-databricks-genie.png|1200|630
040-hero|040-julius-ai-vs-chatgpt/visuals/hero.html|040-julius-ai-vs-chatgpt/images/hero-julius-ai-vs-chatgpt.png|1200|630
041-hero|041-thoughtspot-vs-databricks-genie/visuals/hero.html|041-thoughtspot-vs-databricks-genie/images/hero-thoughtspot-vs-databricks-genie.png|1200|630
042-hero|042-infinisynapse-vs-tableau/visuals/hero.html|042-infinisynapse-vs-tableau/images/hero-infinisynapse-vs-tableau.png|1200|630
043-hero|043-infinisynapse-review/visuals/hero.html|043-infinisynapse-review/images/hero-infinisynapse-review.png|1200|630
# Body infographics — comparison / review articles
039-body|039-infinisynapse-vs-databricks-genie/visuals/lakehouse-decision.html|039-infinisynapse-vs-databricks-genie/images/lakehouse-decision-infinisynapse-vs-genie.png|1200|680
040-body|040-julius-ai-vs-chatgpt/visuals/decision-flow.html|040-julius-ai-vs-chatgpt/images/decision-flow-julius-vs-chatgpt.png|1200|720
041-body|041-thoughtspot-vs-databricks-genie/visuals/decision-chart.html|041-thoughtspot-vs-databricks-genie/images/decision-chart-thoughtspot-vs-genie.png|1200|680
042-body|042-infinisynapse-vs-tableau/visuals/matrix.html|042-infinisynapse-vs-tableau/images/matrix-infinisynapse-vs-tableau.png|1200|680
043-body|043-infinisynapse-review/visuals/five-pillars-radar.html|043-infinisynapse-review/images/five-pillars-radar-infinisynapse.png|1200|720
JOBS
echo "✅ Pillar 3 heroes + body infographics rendered."
