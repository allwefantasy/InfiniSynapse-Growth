#!/usr/bin/env bash
# Pillar 6 · Hero HTML→PNG
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar6-ai-excel-csv-spreadsheet"
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

render "069-hero" "$PILLAR/069-clean-excel-data-with-ai/visuals/hero.html" "$PILLAR/069-clean-excel-data-with-ai/images/hero-clean-excel-data-with-ai.png" 1200 630
render "070-hero" "$PILLAR/070-ai-alternative-to-pivot-table/visuals/hero.html" "$PILLAR/070-ai-alternative-to-pivot-table/images/hero-ai-alternative-to-pivot-table.png" 1200 630
render "071-hero" "$PILLAR/071-ai-vlookup-replacement/visuals/hero.html" "$PILLAR/071-ai-vlookup-replacement/images/hero-ai-vlookup-replacement.png" 1200 630
render "072-hero" "$PILLAR/072-ai-excel-formula-generator/visuals/hero.html" "$PILLAR/072-ai-excel-formula-generator/images/hero-ai-excel-formula-generator.png" 1200 630
render "073-hero" "$PILLAR/073-analyze-csv-with-ai/visuals/hero.html" "$PILLAR/073-analyze-csv-with-ai/images/hero-analyze-csv-with-ai.png" 1200 630
render "074-hero" "$PILLAR/074-merge-multiple-csv-with-ai/visuals/hero.html" "$PILLAR/074-merge-multiple-csv-with-ai/images/hero-merge-multiple-csv-with-ai.png" 1200 630
render "075-hero" "$PILLAR/075-deduplicate-data-with-ai/visuals/hero.html" "$PILLAR/075-deduplicate-data-with-ai/images/hero-deduplicate-data-with-ai.png" 1200 630
render "076-hero" "$PILLAR/076-ai-data-cleaning-techniques/visuals/hero.html" "$PILLAR/076-ai-data-cleaning-techniques/images/hero-ai-data-cleaning-techniques.png" 1200 630
render "077-hero" "$PILLAR/077-ai-excel-chart-generator/visuals/hero.html" "$PILLAR/077-ai-excel-chart-generator/images/hero-ai-excel-chart-generator.png" 1200 630
render "078-hero" "$PILLAR/078-ai-financial-modeling-excel/visuals/hero.html" "$PILLAR/078-ai-financial-modeling-excel/images/hero-ai-financial-modeling-excel.png" 1200 630
render "079-hero" "$PILLAR/079-excel-monthly-report-automation-ai/visuals/hero.html" "$PILLAR/079-excel-monthly-report-automation-ai/images/hero-excel-monthly-report-automation-ai.png" 1200 630
render "080-hero" "$PILLAR/080-ai-data-wrangling-tools/visuals/hero.html" "$PILLAR/080-ai-data-wrangling-tools/images/hero-ai-data-wrangling-tools.png" 1200 630
echo "✅ Pillar 6 heroes rendered."
