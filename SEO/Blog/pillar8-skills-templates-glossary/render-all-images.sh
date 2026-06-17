#!/usr/bin/env bash
# Pillar 8 · Hero HTML→PNG
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar8-skills-templates-glossary"
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

render "095-hero" "$PILLAR/095-ai-data-analysis-prompts/visuals/hero.html" "$PILLAR/095-ai-data-analysis-prompts/images/hero-ai-data-analysis-prompts.png" 1200 630
render "096-hero" "$PILLAR/096-data-analysis-prompt-template/visuals/hero.html" "$PILLAR/096-data-analysis-prompt-template/images/hero-data-analysis-prompt-template.png" 1200 630
render "097-hero" "$PILLAR/097-ai-data-analyst-skills/visuals/hero.html" "$PILLAR/097-ai-data-analyst-skills/images/hero-ai-data-analyst-skills.png" 1200 630
render "098-hero" "$PILLAR/098-how-to-evaluate-ai-data-analyst/visuals/hero.html" "$PILLAR/098-how-to-evaluate-ai-data-analyst/images/hero-how-to-evaluate-ai-data-analyst.png" 1200 630
render "099-hero" "$PILLAR/099-ai-analytics-glossary/visuals/hero.html" "$PILLAR/099-ai-analytics-glossary/images/hero-ai-analytics-glossary.png" 1200 630
render "100-hero" "$PILLAR/100-data-agent-faq/visuals/hero.html" "$PILLAR/100-data-agent-faq/images/hero-data-agent-faq.png" 1200 630
echo "✅ Pillar 8 heroes rendered."
