#!/usr/bin/env bash
# Generate AI heroes only for articles still using small programmatic PNGs (<100KB).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../../../../.." && pwd)"
BLOG="$ROOT/SEO/Blog"
MODEL="${MODEL:-openoctopus/imagen-4-fast}"
MIN_AI_BYTES=100000

read_prompt() {
  awk '
    BEGIN { header = 1 }
    header && /^#($| )/ { next }
    header && /^[[:space:]]*$/ { next }
    { header = 0; print }
  ' "$1"
}

ok=0
fail=0
skip=0

for art in "$BLOG"/pillar2[1-5]-*/[0-9][0-9][0-9]-*/article.md; do
  [[ -f "$art" ]] || continue
  dir="$(dirname "$art")"
  name="$(basename "$dir")"
  img_name="$(grep -oE 'images/hero-[^)]+\.png' "$art" | head -1 | sed 's|images/||')"
  [[ -n "$img_name" ]] || continue
  out="$dir/images/$img_name"
  if [[ -f "$out" ]] && [[ $(stat -f%z "$out" 2>/dev/null || stat -c%s "$out") -ge $MIN_AI_BYTES ]]; then
    skip=$((skip+1))
    continue
  fi
  prompt_file="$dir/prompts/cover.prompt"
  if [[ ! -f "$prompt_file" ]]; then
    echo "SKIP $name (no prompt)"
    fail=$((fail+1))
    continue
  fi
  mkdir -p "$dir/images"
  prompt_text="$(read_prompt "$prompt_file")"
  echo "▶ $name"
  if ooct run "$MODEL" \
      --prompt "$prompt_text" \
      --aspect-ratio 16:9 \
      --resolution 2k \
      --output "$out"; then
    if [[ -f "$out" ]]; then
      sz=$(sips -g pixelWidth -g pixelHeight "$out" 2>/dev/null | awk '/pixel/ {print $2}' | xargs | tr ' ' 'x' || echo "?")
      echo "  OK $out ($sz)"
      ok=$((ok+1))
    else
      echo "  FAIL $name"
      fail=$((fail+1))
    fi
  else
    echo "  FAIL $name"
    fail=$((fail+1))
  fi
done

echo "Done: ok=$ok skip=$skip fail=$fail"
