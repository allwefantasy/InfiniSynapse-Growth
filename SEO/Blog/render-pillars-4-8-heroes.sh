#!/usr/bin/env bash
set -euo pipefail
ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth/SEO/Blog"
for p in pillar4-data-source-connectors pillar5-nl2sql-text-to-sql pillar6-ai-excel-csv-spreadsheet pillar7-use-cases-role-industry pillar8-skills-templates-glossary; do
  echo "=== $p ==="
  bash "$ROOT/$p/render-all-images.sh"
done
echo "✅ All Pillar 4-8 heroes rendered."
