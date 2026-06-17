#!/usr/bin/env bash
# Pillar 5 · Hero HTML→PNG
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar5-nl2sql-text-to-sql"
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

render "059-hero" "$PILLAR/059-natural-language-to-sql/visuals/hero.html" "$PILLAR/059-natural-language-to-sql/images/hero-natural-language-to-sql.png" 1200 630
render "060-hero" "$PILLAR/060-text-to-sql-llm/visuals/hero.html" "$PILLAR/060-text-to-sql-llm/images/hero-text-to-sql-llm.png" 1200 630
render "061-hero" "$PILLAR/061-nl2sql-benchmark-spider-bird/visuals/hero.html" "$PILLAR/061-nl2sql-benchmark-spider-bird/images/hero-nl2sql-benchmark-spider-bird.png" 1200 630
render "062-hero" "$PILLAR/062-ai-sql-generator/visuals/hero.html" "$PILLAR/062-ai-sql-generator/images/hero-ai-sql-generator.png" 1200 630
render "063-hero" "$PILLAR/063-llm-sql-generation-architecture/visuals/hero.html" "$PILLAR/063-llm-sql-generation-architecture/images/hero-llm-sql-generation-architecture.png" 1200 630
render "064-hero" "$PILLAR/064-sql-rag-vs-semantic-layer/visuals/hero.html" "$PILLAR/064-sql-rag-vs-semantic-layer/images/hero-sql-rag-vs-semantic-layer.png" 1200 630
render "065-hero" "$PILLAR/065-text-to-sql-fine-tuning/visuals/hero.html" "$PILLAR/065-text-to-sql-fine-tuning/images/hero-text-to-sql-fine-tuning.png" 1200 630
render "066-hero" "$PILLAR/066-sql-agent-vs-text-to-sql/visuals/hero.html" "$PILLAR/066-sql-agent-vs-text-to-sql/images/hero-sql-agent-vs-text-to-sql.png" 1200 630
render "067-hero" "$PILLAR/067-nl2sql-production-failure-modes/visuals/hero.html" "$PILLAR/067-nl2sql-production-failure-modes/images/hero-nl2sql-production-failure-modes.png" 1200 630
render "068-hero" "$PILLAR/068-dialect-aware-sql-generation/visuals/hero.html" "$PILLAR/068-dialect-aware-sql-generation/images/hero-dialect-aware-sql-generation.png" 1200 630
echo "✅ Pillar 5 heroes rendered."
