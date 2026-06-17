#!/usr/bin/env bash
# Pillar 2 · Hero HTML→PNG
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar2-data-agent-vs-alternatives"
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

render "014-hero" "$PILLAR/014-code-agent-vs-data-agent/visuals/hero.html" "$PILLAR/014-code-agent-vs-data-agent/images/hero-code-agent-vs-data-agent.png" 1200 630
render "015-hero" "$PILLAR/015-data-agent-architecture/visuals/hero.html" "$PILLAR/015-data-agent-architecture/images/hero-data-agent-architecture.png" 1200 630
render "016-hero" "$PILLAR/016-ai-data-analyst-vs-bi-tools/visuals/hero.html" "$PILLAR/016-ai-data-analyst-vs-bi-tools/images/hero-ai-data-analyst-vs-bi-tools.png" 1200 630
render "017-hero" "$PILLAR/017-data-agent-vs-llm-chatbot/visuals/hero.html" "$PILLAR/017-data-agent-vs-llm-chatbot/images/hero-data-agent-vs-llm-chatbot.png" 1200 630
render "018-hero" "$PILLAR/018-chatgpt-data-analysis-limitations/visuals/hero.html" "$PILLAR/018-chatgpt-data-analysis-limitations/images/hero-chatgpt-data-analysis-limitations.png" 1200 630
render "019-hero" "$PILLAR/019-code-interpreter-vs-data-agent/visuals/hero.html" "$PILLAR/019-code-interpreter-vs-data-agent/images/hero-code-interpreter-vs-data-agent.png" 1200 630
render "020-hero" "$PILLAR/020-databricks-genie-vs-data-agent/visuals/hero.html" "$PILLAR/020-databricks-genie-vs-data-agent/images/hero-databricks-genie-vs-data-agent.png" 1200 630
render "021-hero" "$PILLAR/021-ai-data-analyst-vs-human-analyst/visuals/hero.html" "$PILLAR/021-ai-data-analyst-vs-human-analyst/images/hero-ai-data-analyst-vs-human-analyst.png" 1200 630
render "022-hero" "$PILLAR/022-governance-for-ai-data-analysis/visuals/hero.html" "$PILLAR/022-governance-for-ai-data-analysis/images/hero-governance-for-ai-data-analysis.png" 1200 630
render "023-hero" "$PILLAR/023-ai-data-analyst-vs-traditional-bi-analyst/visuals/hero.html" "$PILLAR/023-ai-data-analyst-vs-traditional-bi-analyst/images/hero-ai-data-analyst-vs-traditional-bi-analyst.png" 1200 630
echo "✅ Pillar 2 heroes rendered."
