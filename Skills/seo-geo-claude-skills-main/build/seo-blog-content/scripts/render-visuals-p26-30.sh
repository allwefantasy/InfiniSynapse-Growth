#!/usr/bin/env bash
# Render P26-30 body table HTML to PNG via headless Chrome.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
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

tables=0
MODE="${1:-tables}"

for pillar in "$BLOG"/pillar2[6-9]-* "$BLOG"/pillar30-*; do
  [[ -d "$pillar" ]] || continue
  for art in "$pillar"/[0-9][0-9][0-9]-*/article.md; do
    [[ -f "$art" ]] || continue
    dir="$(dirname "$art")"
    name="$(basename "$dir")"
    if [[ "$MODE" == "all" || "$MODE" == "tables" ]]; then
      table_html="$dir/visuals/table-${name}.html"
      if [[ -f "$table_html" ]]; then
        out="$dir/images/table-${name}.png"
        render "$table_html" "$out" 1200 720 1
        tables=$((tables+1))
        echo "table $name"
      fi
    fi
  done
done

echo "Done: tables=$tables"
