#!/usr/bin/env bash
# Regenerate hero images flagged by scan-hero-text-p21-25.py
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../../../../.." && pwd)"
BLOG="$ROOT/SEO/Blog"
FLAGS="$BLOG/hero-text-flags.txt"
MODEL="${MODEL:-openoctopus/imagen-4-fast}"
MAX="${MAX:-0}"  # 0 = all flagged

read_prompt() {
  awk '
    BEGIN { header = 1 }
    header && /^#($| )/ { next }
    header && /^[[:space:]]*$/ { next }
    { header = 0; print }
  ' "$1"
}

if [[ ! -f "$FLAGS" ]]; then
  echo "Run: python3 "$SCRIPT_DIR/scan-hero-text-p21-25.py""
  exit 1
fi

ok=0
fail=0
n=0

while IFS=$'\t' read -r name _rest; do
  [[ -n "$name" ]] || continue
  n=$((n+1))
  if [[ "$MAX" -gt 0 && "$n" -gt "$MAX" ]]; then
    break
  fi

  art="$(find "$BLOG"/pillar2[1-5]-* -maxdepth 1 -type d -name "$name" | head -1)"
  if [[ -z "$art" ]]; then
    echo "SKIP $name (dir not found)"
    fail=$((fail+1))
    continue
  fi

  img_name="$(grep -oE 'images/hero-[^)]+\.png' "$art/article.md" | head -1 | sed 's|images/||')"
  prompt_file="$art/prompts/cover.prompt"
  out="$art/images/$img_name"

  if [[ ! -f "$prompt_file" ]]; then
    echo "SKIP $name (no prompt)"
    fail=$((fail+1))
    continue
  fi

  mkdir -p "$art/images"
  prompt_text="$(read_prompt "$prompt_file")"
  # Extra anti-text suffix for regen pass.
  prompt_text="$prompt_text

CRITICAL: This is a wordless abstract illustration. No typography, no fake UI, no dashboard labels, no step names, no year numbers, no title banners."

  echo "▶ [$n] $name"
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
done < <(cut -f1 "$FLAGS")

echo "Done: ok=$ok fail=$fail"
