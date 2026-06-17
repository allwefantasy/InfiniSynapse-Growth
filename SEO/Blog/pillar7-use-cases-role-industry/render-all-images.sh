#!/usr/bin/env bash
# Pillar 7 · Hero HTML→PNG
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar7-use-cases-role-industry"
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

render "081-hero" "$PILLAR/081-ai-tools-for-data-analysts/visuals/hero.html" "$PILLAR/081-ai-tools-for-data-analysts/images/hero-ai-tools-for-data-analysts.png" 1200 630
render "082-hero" "$PILLAR/082-ai-data-analysis-product-managers/visuals/hero.html" "$PILLAR/082-ai-data-analysis-product-managers/images/hero-ai-data-analysis-product-managers.png" 1200 630
render "083-hero" "$PILLAR/083-ai-data-analysis-finance-teams/visuals/hero.html" "$PILLAR/083-ai-data-analysis-finance-teams/images/hero-ai-data-analysis-finance-teams.png" 1200 630
render "084-hero" "$PILLAR/084-ai-data-analysis-marketing/visuals/hero.html" "$PILLAR/084-ai-data-analysis-marketing/images/hero-ai-data-analysis-marketing.png" 1200 630
render "085-hero" "$PILLAR/085-ai-data-analysis-operations/visuals/hero.html" "$PILLAR/085-ai-data-analysis-operations/images/hero-ai-data-analysis-operations.png" 1200 630
render "086-hero" "$PILLAR/086-ai-for-data-engineers/visuals/hero.html" "$PILLAR/086-ai-for-data-engineers/images/hero-ai-for-data-engineers.png" 1200 630
render "087-hero" "$PILLAR/087-ai-data-strategy-cto/visuals/hero.html" "$PILLAR/087-ai-data-strategy-cto/images/hero-ai-data-strategy-cto.png" 1200 630
render "088-hero" "$PILLAR/088-ai-data-analysis-founders/visuals/hero.html" "$PILLAR/088-ai-data-analysis-founders/images/hero-ai-data-analysis-founders.png" 1200 630
render "089-hero" "$PILLAR/089-ai-data-analysis-ecommerce/visuals/hero.html" "$PILLAR/089-ai-data-analysis-ecommerce/images/hero-ai-data-analysis-ecommerce.png" 1200 630
render "090-hero" "$PILLAR/090-ai-data-analysis-saas/visuals/hero.html" "$PILLAR/090-ai-data-analysis-saas/images/hero-ai-data-analysis-saas.png" 1200 630
render "091-hero" "$PILLAR/091-ai-data-analysis-financial-services/visuals/hero.html" "$PILLAR/091-ai-data-analysis-financial-services/images/hero-ai-data-analysis-financial-services.png" 1200 630
render "092-hero" "$PILLAR/092-ai-data-analysis-supply-chain/visuals/hero.html" "$PILLAR/092-ai-data-analysis-supply-chain/images/hero-ai-data-analysis-supply-chain.png" 1200 630
render "093-hero" "$PILLAR/093-ai-data-analysis-healthcare/visuals/hero.html" "$PILLAR/093-ai-data-analysis-healthcare/images/hero-ai-data-analysis-healthcare.png" 1200 630
render "094-hero" "$PILLAR/094-ai-data-analysis-logistics/visuals/hero.html" "$PILLAR/094-ai-data-analysis-logistics/images/hero-ai-data-analysis-logistics.png" 1200 630
echo "✅ Pillar 7 heroes rendered."
