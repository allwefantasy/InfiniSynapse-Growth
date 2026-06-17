#!/usr/bin/env bash
# Pillar 1 · Hero 封面 + 正文信息图 HTML→PNG
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar1-ai-native-data-analysis"
CHROME=""
for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"; do
  [[ -x "$p" ]] && CHROME="$p" && break
done
[[ -n "$CHROME" ]] || { echo "❌ Chrome not found"; exit 1; }

render() {
  local label="$1" html="$2" png="$3" w="${4:-1200}" h="${5:-720}"
  [[ -f "$html" ]] || { echo "SKIP $label — no html"; return; }
  mkdir -p "$(dirname "$png")"
  echo "▶ $label (${w}×${h})"
  "$CHROME" --headless=new --hide-scrollbars --disable-gpu \
    --force-device-scale-factor=2 --window-size="${w},${h}" \
    --screenshot="$png" --default-background-color=ffffffff \
    "file://$html" >/dev/null 2>&1
  if [[ -f "$png" ]]; then
    echo "  ✅ $(basename "$png")"
    if [[ "$label" == *-hero ]]; then
      cp -f "$png" "$(dirname "$png")/og-cover.png"
    fi
  else
    echo "  ❌ failed"
  fi
}

while IFS='|' read -r slug html png w h; do
  [[ "$slug" == \#* || -z "$slug" ]] && continue
  render "$slug" "$PILLAR/$html" "$PILLAR/$png" "${w:-1200}" "${h:-720}"
done <<'JOBS'
# Heroes — article title + abstract geometry (1200×630)
001-hero|001-ai-for-data-analysis/visuals/hero.html|001-ai-for-data-analysis/images/hero-ai-for-data-analysis.png|1200|630
002-hero|002-data-agent-manifesto/visuals/hero.html|002-data-agent-manifesto/images/hero-data-agent-manifesto.png|1200|630
003-hero|003-what-is-a-data-agent/visuals/hero.html|003-what-is-a-data-agent/images/hero-what-is-a-data-agent.png|1200|630
004-hero|004-ai-native-data-platform/visuals/hero.html|004-ai-native-data-platform/images/hero-ai-native-data-platform.png|1200|630
005-hero|005-best-agentic-analytics/visuals/hero.html|005-best-agentic-analytics/images/hero-agentic-analytics-comparison.png|1200|630
006-hero|006-autonomous-data-agent/visuals/hero.html|006-autonomous-data-agent/images/hero-autonomous-data-agent-lifecycle.png|1200|630
007-hero|007-ai-data-analyst/visuals/hero.html|007-ai-data-analyst/images/hero-ai-data-analyst-workflow.png|1200|630
008-hero|008-ai-data-analyst-job-description/visuals/hero.html|008-ai-data-analyst-job-description/images/hero-ai-data-analyst-jd-template.png|1200|630
009-hero|009-data-agent-memory/visuals/hero.html|009-data-agent-memory/images/hero-distillation-vs-chat-history.png|1200|630
010-hero|010-fabric-data-agent-vs-copilot/visuals/hero.html|010-fabric-data-agent-vs-copilot/images/hero-fabric-data-agent-vs-copilot.png|1200|630
011-hero|011-ai-native-vs-augmented-analytics/visuals/hero.html|011-ai-native-vs-augmented-analytics/images/hero-ai-native-vs-augmented.png|1200|630
012-hero|012-ai-data-analysis/visuals/hero.html|012-ai-data-analysis/images/hero-ai-data-analysis-workflow.png|1200|630
013-hero|013-data-agent-glossary/visuals/hero.html|013-data-agent-glossary/images/hero-data-agent-glossary.png|1200|630
# Body diagrams
001-body|001-ai-for-data-analysis/visuals/five-methods.html|001-ai-for-data-analysis/images/five-analysis-methods.png
002-body|002-data-agent-manifesto/visuals/objective-split.html|002-data-agent-manifesto/images/code-vs-data-agent-objectives.png
003-body|003-what-is-a-data-agent/visuals/architecture.html|003-what-is-a-data-agent/images/data-agent-architecture-layers.png
004-body|004-ai-native-data-platform/visuals/platform-layers.html|004-ai-native-data-platform/images/platform-five-layers.png
005-timeline|005-best-agentic-analytics/visuals/task-timeline.html|005-best-agentic-analytics/images/infinisynapse-task-timeline.png
005-matrix|005-best-agentic-analytics/visuals/decision-matrix.html|005-best-agentic-analytics/images/decision-matrix-agentic-analytics.png
006-tree|006-autonomous-data-agent/visuals/self-correction-tree.html|006-autonomous-data-agent/images/self-correction-decision-tree.png
007-matrix|007-ai-data-analyst/visuals/division-matrix.html|007-ai-data-analyst/images/human-ai-division-matrix.png
008-matrix|008-ai-data-analyst-job-description/visuals/skills-matrix.html|008-ai-data-analyst-job-description/images/skills-matrix-ai-data-analyst.png
009-card|009-data-agent-memory/visuals/memory-card.html|009-data-agent-memory/images/memory-card-anatomy.png
010-matrix|010-fabric-data-agent-vs-copilot/visuals/decision-matrix.html|010-fabric-data-agent-vs-copilot/images/decision-matrix-fabric.png
010-compare|010-fabric-data-agent-vs-copilot/visuals/compare-table.html|010-fabric-data-agent-vs-copilot/images/fabric-vs-copilot-table.png
011-pillars|011-ai-native-vs-augmented-analytics/visuals/five-pillars.html|011-ai-native-vs-augmented-analytics/images/five-pillars-vs-augmented.png
012-flow|012-ai-data-analysis/visuals/seven-stage-workflow.html|012-ai-data-analysis/images/seven-stage-workflow.png
013-map|013-data-agent-glossary/visuals/term-map.html|013-data-agent-glossary/images/term-relationship-map.png
JOBS

echo "✅ All hero covers + body diagrams rendered."
