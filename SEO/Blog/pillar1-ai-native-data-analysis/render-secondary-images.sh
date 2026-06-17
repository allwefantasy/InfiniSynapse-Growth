#!/usr/bin/env bash
# 渲染 Pillar 1 正文内信息图（HTML → PNG）
set -euo pipefail

ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar1-ai-native-data-analysis"

CHROME=""
for path in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"; do
  [[ -x "$path" ]] && CHROME="$path" && break
done
[[ -n "$CHROME" ]] || { echo "❌ Chrome not found"; exit 1; }

render() {
  local label="$1" html="$2" png="$3" w="${4:-1200}" h="${5:-680}"
  [[ -f "$html" ]] || { echo "SKIP $label — no html"; return; }
  mkdir -p "$(dirname "$png")"
  echo "▶ $label ($w×$h)"
  "$CHROME" --headless=new --hide-scrollbars --disable-gpu \
    --force-device-scale-factor=2 --window-size="${w},${h}" \
    --screenshot="$png" --default-background-color=00000000 \
    "file://$html" >/dev/null 2>&1
  [[ -f "$png" ]] && echo "  ✅ $png" || echo "  ❌ failed"
}

declare -a JOBS=(
  "005 decision-matrix|$PILLAR/005-best-agentic-analytics/visuals/decision-matrix.html|$PILLAR/005-best-agentic-analytics/images/decision-matrix-agentic-analytics.png"
  "006 self-correction|$PILLAR/006-autonomous-data-agent/visuals/self-correction-tree.html|$PILLAR/006-autonomous-data-agent/images/self-correction-decision-tree.png"
  "007 division-matrix|$PILLAR/007-ai-data-analyst/visuals/division-matrix.html|$PILLAR/007-ai-data-analyst/images/human-ai-division-matrix.png"
  "008 skills-matrix|$PILLAR/008-ai-data-analyst-job-description/visuals/skills-matrix.html|$PILLAR/008-ai-data-analyst-job-description/images/skills-matrix-ai-data-analyst.png"
  "009 memory-card|$PILLAR/009-data-agent-memory/visuals/memory-card.html|$PILLAR/009-data-agent-memory/images/memory-card-anatomy.png"
  "010 fabric-matrix|$PILLAR/010-fabric-data-agent-vs-copilot/visuals/decision-matrix.html|$PILLAR/010-fabric-data-agent-vs-copilot/images/decision-matrix-fabric.png"
  "011 five-pillars|$PILLAR/011-ai-native-vs-augmented-analytics/visuals/five-pillars.html|$PILLAR/011-ai-native-vs-augmented-analytics/images/five-pillars-vs-augmented.png"
  "012 seven-stage|$PILLAR/012-ai-data-analysis/visuals/seven-stage-workflow.html|$PILLAR/012-ai-data-analysis/images/seven-stage-workflow.png"
  "013 term-map|$PILLAR/013-data-agent-glossary/visuals/term-map.html|$PILLAR/013-data-agent-glossary/images/term-relationship-map.png"
)

for job in "${JOBS[@]}"; do
  IFS='|' read -r label html png <<<"$job"
  render "$label" "$html" "$png"
done
echo "Done."
