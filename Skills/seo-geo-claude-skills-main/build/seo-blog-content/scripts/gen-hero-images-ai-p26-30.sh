#!/usr/bin/env bash
# Batch AI hero images for Pillars 26-30 via OpenOctopus CLI (ooct).
#
# Prereq:
#   python3 "$SCRIPT_DIR/gen-hero-prompts-p26-30.py"
#   ooct auth login
#
# Usage:
#   bash "$SCRIPT_DIR/gen-hero-images-ai-p26-30.sh"              # all 100
#   bash "$SCRIPT_DIR/gen-hero-images-ai-p26-30.sh" pillar26     # one pillar
#   bash "$SCRIPT_DIR/gen-hero-images-ai-p26-30.sh" --dry-run    # plan only
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
BLOG="$ROOT/SEO/Blog"
MODEL="${MODEL:-openoctopus/imagen-4-fast}"
ASPECT="${ASPECT:-16:9}"
RESOLUTION="${RESOLUTION:-2k}"
DRY_RUN=0
PILLAR_FILTER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    pillar2[6-9]*|pillar30*) PILLAR_FILTER="$1"; shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if ! command -v ooct >/dev/null 2>&1; then
  echo "ooct CLI not found. Install: sudo npm i -g @openoctopus/cli"
  exit 1
fi
if ! ooct auth status 2>/dev/null | grep -q "Authenticated"; then
  echo "Run: ooct auth login"
  exit 1
fi

read_prompt() {
  awk '
    BEGIN { header = 1 }
    header && /^#($| )/ { next }
    header && /^[[:space:]]*$/ { next }
    { header = 0; print }
  ' "$1"
}

articles=()
for pillar in "$BLOG"/pillar2[6-9]-* "$BLOG"/pillar30-*; do
  [[ -d "$pillar" ]] || continue
  if [[ -n "$PILLAR_FILTER" && "$(basename "$pillar")" != *"$PILLAR_FILTER"* ]]; then
    continue
  fi
  for art in "$pillar"/[0-9][0-9][0-9]-*/article.md; do
    [[ -f "$art" ]] || continue
    articles+=("$art")
  done
done

echo "Model: $MODEL | aspect: $ASPECT | resolution: $RESOLUTION"
echo "Articles: ${#articles[@]}"
if [[ ${#articles[@]} -eq 0 ]]; then
  echo "No articles found under $BLOG (pillar26-30). Check paths."
  exit 1
fi
est=$(awk -v n="${#articles[@]}" 'BEGIN{printf "%.2f", n*0.038}')
echo "Estimated cost: ~\$$est USD"
echo ""

ok=0
fail=0
for art in "${articles[@]}"; do
  dir="$(dirname "$art")"
  name="$(basename "$dir")"
  prompt_file="$dir/prompts/cover.prompt"
  if [[ ! -f "$prompt_file" ]]; then
    echo "SKIP $name (no prompts/cover.prompt)"
    fail=$((fail+1))
    continue
  fi
  img_name="$(grep -oE 'images/hero-[^)]+\.png' "$art" | head -1 | sed 's|images/||')"
  if [[ -z "$img_name" ]]; then
    echo "SKIP $name (no hero image ref)"
    fail=$((fail+1))
    continue
  fi
  out="$dir/images/$img_name"
  og="$dir/images/og-cover.png"
  mkdir -p "$dir/images"
  prompt_text="$(read_prompt "$prompt_file")"

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "DRY $name -> $out"
    ok=$((ok+1))
    continue
  fi

  echo "▶ $name"
  if ooct run "$MODEL" \
      --prompt "$prompt_text" \
      --aspect-ratio "$ASPECT" \
      --resolution "$RESOLUTION" \
      --output "$out"; then
    if [[ -f "$out" ]]; then
      cp "$out" "$og"
      sz=$(sips -g pixelWidth -g pixelHeight "$out" 2>/dev/null | awk '/pixel/ {print $2}' | xargs | tr ' ' 'x' || echo "?")
      kb=$(du -k "$out" | awk '{print $1}')
      echo "  OK $out (${sz}, ${kb}KB) + og-cover.png"
      ok=$((ok+1))
    else
      echo "  FAIL $name (no output file)"
      fail=$((fail+1))
    fi
  else
    echo "  FAIL $name (ooct error)"
    fail=$((fail+1))
  fi
  echo ""
done

echo "Done: ok=$ok fail=$fail"
