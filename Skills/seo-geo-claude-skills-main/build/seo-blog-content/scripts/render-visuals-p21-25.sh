#!/usr/bin/env bash
# Render P21-25 hero + body table HTML to PNG via headless Chrome.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../../../../.." && pwd)"
BLOG="$ROOT/SEO/Blog"

CHROME=""
for path in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do
  if [[ -x "$path" ]]; then CHROME="$path"; break; fi
done
[[ -n "$CHROME" ]] || { echo "Chrome not found"; exit 1; }

render() {
  local html="$1" png="$2" w="$3" h="$4" force="${5:-0}"
  [[ -f "$html" ]] || return 0
  if [[ "$force" != "1" ]] && [[ -f "$png" ]] && [[ $(stat -f%z "$png" 2>/dev/null || stat -c%s "$png") -gt 5000 ]]; then
    return 0
  fi
  mkdir -p "$(dirname "$png")"
  "$CHROME" --headless=new --hide-scrollbars --disable-gpu \
    --force-device-scale-factor=2 --window-size="${w},${h}" \
    --screenshot="$png" --default-background-color=00000000 \
    "file://$html" > /dev/null 2>&1 || true
  sleep 0.12
}

heroes=0
tables=0

MODE="${1:-all}"  # all | heroes | tables

for art in "$BLOG"/pillar2[1-5]-*/[0-9][0-9][0-9]-*/article.md; do
  [[ -f "$art" ]] || continue
  dir="$(dirname "$art")"
  name="$(basename "$dir")"

  if [[ "$MODE" == "all" || "$MODE" == "heroes" ]]; then
    hero_html="$dir/visuals/hero.html"
    hero_img="$(grep -oE 'images/hero-[^)]+\.png' "$art" | head -1 | sed 's|images/||')"
    if [[ -f "$hero_html" && -n "$hero_img" ]]; then
      out="$dir/images/$hero_img"
      render "$hero_html" "$out" 1200 630 1
      cp "$out" "$dir/images/og-cover.png"
      heroes=$((heroes+1))
      echo "hero $name"
    fi
  fi

  if [[ "$MODE" == "all" || "$MODE" == "tables" ]]; then
    table_html="$dir/visuals/table-${name}.html"
    if [[ -f "$table_html" ]]; then
      out="$dir/images/table-${name}.png"
      render "$table_html" "$out" 1200 720
      tables=$((tables+1))
      echo "table $name"
    fi
  fi
done

echo "Done: heroes=$heroes tables=$tables"
