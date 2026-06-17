#!/usr/bin/env bash
# Pillar 4 · Hero HTML→PNG
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar4-data-source-connectors"
CHROME=""
for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"; do
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
    cp -f "$png" "$(dirname "$png")/hero.png"
    cp -f "$png" "$(dirname "$png")/og-cover.png"
  fi
}

render "044-hero" "$PILLAR/044-connect-supabase-to-ai-data-analyst/visuals/hero.html" "$PILLAR/044-connect-supabase-to-ai-data-analyst/images/hero-connect-supabase-to-ai-data-analyst.png" 1200 630
render "045-hero" "$PILLAR/045-connect-postgres-to-ai-data-analyst/visuals/hero.html" "$PILLAR/045-connect-postgres-to-ai-data-analyst/images/hero-connect-postgres-to-ai-data-analyst.png" 1200 630
render "046-hero" "$PILLAR/046-connect-mysql-to-ai-data-analyst/visuals/hero.html" "$PILLAR/046-connect-mysql-to-ai-data-analyst/images/hero-connect-mysql-to-ai-data-analyst.png" 1200 630
render "047-hero" "$PILLAR/047-connect-snowflake-to-ai-analyst/visuals/hero.html" "$PILLAR/047-connect-snowflake-to-ai-analyst/images/hero-connect-snowflake-to-ai-analyst.png" 1200 630
render "048-hero" "$PILLAR/048-connect-bigquery-to-ai-data-analyst/visuals/hero.html" "$PILLAR/048-connect-bigquery-to-ai-data-analyst/images/hero-connect-bigquery-to-ai-data-analyst.png" 1200 630
render "049-hero" "$PILLAR/049-connect-databricks-to-ai-analyst/visuals/hero.html" "$PILLAR/049-connect-databricks-to-ai-analyst/images/hero-connect-databricks-to-ai-analyst.png" 1200 630
render "050-hero" "$PILLAR/050-connect-mongodb-to-ai-data-analyst/visuals/hero.html" "$PILLAR/050-connect-mongodb-to-ai-data-analyst/images/hero-connect-mongodb-to-ai-data-analyst.png" 1200 630
render "051-hero" "$PILLAR/051-ai-data-analysis-google-sheets/visuals/hero.html" "$PILLAR/051-ai-data-analysis-google-sheets/images/hero-ai-data-analysis-google-sheets.png" 1200 630
render "052-hero" "$PILLAR/052-ai-data-analysis-csv-files/visuals/hero.html" "$PILLAR/052-ai-data-analysis-csv-files/images/hero-ai-data-analysis-csv-files.png" 1200 630
render "053-hero" "$PILLAR/053-ai-data-analysis-airtable/visuals/hero.html" "$PILLAR/053-ai-data-analysis-airtable/images/hero-ai-data-analysis-airtable.png" 1200 630
render "054-hero" "$PILLAR/054-ai-analysis-notion-database/visuals/hero.html" "$PILLAR/054-ai-analysis-notion-database/images/hero-ai-analysis-notion-database.png" 1200 630
render "055-hero" "$PILLAR/055-connect-clickhouse-to-ai-analyst/visuals/hero.html" "$PILLAR/055-connect-clickhouse-to-ai-analyst/images/hero-connect-clickhouse-to-ai-analyst.png" 1200 630
render "056-hero" "$PILLAR/056-connect-redshift-to-ai-data-analyst/visuals/hero.html" "$PILLAR/056-connect-redshift-to-ai-data-analyst/images/hero-connect-redshift-to-ai-data-analyst.png" 1200 630
render "057-hero" "$PILLAR/057-analyze-stripe-data-with-ai/visuals/hero.html" "$PILLAR/057-analyze-stripe-data-with-ai/images/hero-analyze-stripe-data-with-ai.png" 1200 630
render "058-hero" "$PILLAR/058-analyze-shopify-data-with-ai/visuals/hero.html" "$PILLAR/058-analyze-shopify-data-with-ai/images/hero-analyze-shopify-data-with-ai.png" 1200 630
echo "✅ Pillar 4 heroes rendered."
