#!/usr/bin/env bash
# Pillar 1 · 批量生成 hero 插图（ooct imagen-4-fast）
set -euo pipefail

ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
PILLAR="$ROOT/SEO/Blog/pillar1-ai-native-data-analysis"
MODEL="openoctopus/imagen-4-fast"
ASPECT="16:9"
RESOLUTION="2k"
NEG_PROMPT="$(tr '\n' ' ' < "$PILLAR/_negative-prompt.txt" | sed 's/  */ /g')"

declare -a JOBS=(
  "001-ai-for-data-analysis|hero-ai-for-data-analysis.png|prompts/cover.prompt"
  "002-data-agent-manifesto|hero-data-agent-manifesto.png|prompts/cover.prompt"
  "003-what-is-a-data-agent|hero-what-is-a-data-agent.png|prompts/cover.prompt"
  "004-ai-native-data-platform|hero-ai-native-data-platform.png|prompts/cover.prompt"
  "005-best-agentic-analytics|hero-agentic-analytics-comparison.png|prompts/cover.prompt"
  "006-autonomous-data-agent|hero-autonomous-data-agent-lifecycle.png|prompts/cover.prompt"
  "007-ai-data-analyst|hero-ai-data-analyst-workflow.png|prompts/cover.prompt"
  "008-ai-data-analyst-job-description|hero-ai-data-analyst-jd-template.png|prompts/cover.prompt"
  "009-data-agent-memory|hero-distillation-vs-chat-history.png|prompts/cover.prompt"
  "010-fabric-data-agent-vs-copilot|hero-fabric-data-agent-vs-copilot.png|prompts/cover.prompt"
  "011-ai-native-vs-augmented-analytics|hero-ai-native-vs-augmented.png|prompts/cover.prompt"
  "012-ai-data-analysis|hero-ai-data-analysis-workflow.png|prompts/cover.prompt"
  "013-data-agent-glossary|hero-data-agent-glossary.png|prompts/cover.prompt"
)

read_prompt() {
  awk 'BEGIN{h=1} h&&/^#($| )/{next} h&&/^[[:space:]]*$/{next} {h=0;print}' "$1"
}

echo "Generating ${#JOBS[@]} hero images with $MODEL …"
for job in "${JOBS[@]}"; do
  IFS='|' read -r folder outname promptfile <<<"$job"
  dir="$PILLAR/$folder"
  prompt_path="$dir/$promptfile"
  out_png="$dir/images/$outname"
  if [[ ! -f "$prompt_path" ]]; then
    echo "SKIP $folder — missing $promptfile"
    continue
  fi
  mkdir -p "$dir/images"
  prompt_text="$(read_prompt "$prompt_path")"
  echo "▶ $folder → images/$outname"
  ooct run "$MODEL" \
    --prompt "$prompt_text" \
    --negative-prompt "$NEG_PROMPT" \
    --aspect-ratio "$ASPECT" \
    --resolution "$RESOLUTION" \
    --output "$out_png"
  if [[ -f "$out_png" ]]; then
    cp -f "$out_png" "$dir/images/og-cover.png"
    echo "  ✅ $out_png (+ og-cover.png)"
  else
    echo "  ❌ failed"
  fi
done
echo "Done."
