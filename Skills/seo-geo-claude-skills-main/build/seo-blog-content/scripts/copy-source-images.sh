#!/usr/bin/env bash
# 把源稿里已有的图复制到 4 个博客 bundle 的 images/ 目录
# Usage: bash Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/copy-source-images.sh

set -euo pipefail

ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
SRC="$ROOT/外部合作/外部文章/data-agent-selected-articles-2026-05-17-to-2026-05-19"
DST="$ROOT/SEO/Blog"

# 01: 直接复用已有 hero
cp "$SRC/01-why-code-agent-cannot-solve-enterprise-data-analysis/images/code-agent-data-agent-cover.png" \
   "$DST/2026-05-19-why-code-agents-cannot-solve-enterprise-data-analysis/images/code-agent-data-agent-cover.png"

# 02: 直接复用 1080p 封面
cp "$SRC/02-data-agent-new-civilization/cover-1080p.png" \
   "$DST/2026-05-19-data-agent-new-civilization/images/cover.png"

# 04: 复用所有架构截图（演讲文章引用了多张），按需在 article.md 里挑用
mkdir -p "$DST/2026-05-19-data-agent-harness-roadshow/images/assets"
cp "$SRC/04-data-agent-harness-roadshow/assets/logo-full.png"               "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/live-home.png"               "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/data-source-management.png"  "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/database-connectors-menu-1440.png" "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/data-sources-bound-rag.png"  "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/rag-research-step.png"       "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/rag-enhanced-final-report.png" "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/task-view-sql-data.png"      "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/completed-task-delivery.png" "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/files-panel.png"             "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/effect-1400-tables.png"      "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"
cp "$SRC/04-data-agent-harness-roadshow/assets/agentic-loop-long-slide.png" "$DST/2026-05-19-data-agent-harness-roadshow/images/assets/"

echo "✅ 已复用图全部 copy 完成"
echo "    01 hero → SEO/Blog/2026-05-19-why-code-agents.../images/"
echo "    02 cover → SEO/Blog/2026-05-19-data-agent-new-civilization/images/"
echo "    04 assets → SEO/Blog/2026-05-19-data-agent-harness-roadshow/images/assets/"
echo ""
echo "⚠️ 还需要新做："
echo "    03 hero        → bash Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/render-html-to-png.sh 03-hero-supabase"
echo "    03 Task View   → 真实产品截图（见 Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/README.md）"
echo "    04 cover       → bash Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/render-html-to-png.sh 04-cover-roadshow"
