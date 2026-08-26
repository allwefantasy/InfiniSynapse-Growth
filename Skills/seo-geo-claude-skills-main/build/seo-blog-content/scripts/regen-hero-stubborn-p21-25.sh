#!/usr/bin/env bash
# Regenerate stubborn hero images with ultra-minimal geometric prompts.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../../../../.." && pwd)"
BLOG="$ROOT/SEO/Blog"
MODEL="${MODEL:-openoctopus/imagen-4-fast}"

ULTRA='Minimal abstract editorial hero. Soft dark gradient background with glowing geometric shapes only: circles, bars, dots, curves. No screens, no UI, no dashboards, no documents, no people with devices. ZERO text, ZERO numbers, ZERO labels, ZERO logos. Pure color and shape composition. 16:9.'

regen() {
  local name="$1" palette="$2"
  local art
  art="$(find "$BLOG"/pillar2[1-5]-* -maxdepth 1 -type d -name "$name" | head -1)"
  local img_name out
  img_name="$(grep -oE 'images/hero-[^)]+\.png' "$art/article.md" | head -1 | sed 's|images/||')"
  out="$art/images/$img_name"
  echo "▶ $name"
  if ooct run "$MODEL" \
      --prompt "$ULTRA Color palette: $palette" \
      --aspect-ratio 16:9 \
      --resolution 2k \
      --output "$out"; then
    echo "  OK $out"
  else
    echo "  FAIL $name"
    return 1
  fi
}

regen "314-types-of-data-analysis" "deep navy and sky blue"
regen "335-data-analysis-software" "dark teal and emerald"
regen "337-tools-for-data-analysis" "dark teal and emerald"
regen "338-software-for-data-analysis" "dark teal and emerald"
regen "349-excel-data-analysis-toolpak" "dark teal and emerald"
regen "377-data-analyst-courses" "midnight blue and periwinkle"
echo "Done."
