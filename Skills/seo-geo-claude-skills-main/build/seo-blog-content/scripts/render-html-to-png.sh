#!/usr/bin/env bash
# HTML → PNG 渲染器（使用 macOS 自带 Chrome / Chrome Canary 的 --headless 模式）
# 与团队现有 visuals/*.html → images/*.png 工作流一致，零外部依赖。
#
# Usage:
#   bash Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/render-html-to-png.sh 03-hero-supabase
#   bash Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/render-html-to-png.sh 04-cover-roadshow
#   bash Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/render-html-to-png.sh all

set -euo pipefail

ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
DST="$ROOT/SEO/Blog"

# 定位 Chrome（按优先级）
CHROME=""
for path in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do
  if [[ -x "$path" ]]; then CHROME="$path"; break; fi
done

if [[ -z "$CHROME" ]]; then
  echo "❌ 未找到 Chrome / Chromium / Brave / Edge，请先安装其一"
  exit 1
fi

echo "ℹ️ 使用浏览器: $CHROME"

# 渲染函数：HTML → PNG @ 1200×630
render() {
  local label="$1"
  local html="$2"
  local png="$3"
  local w="${4:-1200}"
  local h="${5:-630}"

  if [[ ! -f "$html" ]]; then
    echo "⚠️ 跳过 $label：HTML 不存在 $html"
    return
  fi

  mkdir -p "$(dirname "$png")"

  echo "▶ 渲染 $label  ($w × $h)"
  "$CHROME" \
    --headless=new \
    --hide-scrollbars \
    --disable-gpu \
    --force-device-scale-factor=2 \
    --window-size="${w},${h}" \
    --screenshot="$png" \
    --default-background-color=00000000 \
    "file://$html" \
    > /dev/null 2>&1

  if [[ -f "$png" ]]; then
    echo "  ✅ $png"
  else
    echo "  ❌ 渲染失败"
  fi
}

case "${1:-all}" in
  03-hero-supabase|03)
    render "03 hero" \
      "$DST/2026-05-19-ai-analyst-real-data-supabase/visuals/hero-supabase-connect.html" \
      "$DST/2026-05-19-ai-analyst-real-data-supabase/images/hero-supabase-connect.png"
    ;;
  04-cover-roadshow|04)
    render "04 cover" \
      "$DST/2026-05-19-data-agent-harness-roadshow/visuals/cover-roadshow.html" \
      "$DST/2026-05-19-data-agent-harness-roadshow/images/cover-roadshow.png"
    ;;
  all)
    render "03 hero" \
      "$DST/2026-05-19-ai-analyst-real-data-supabase/visuals/hero-supabase-connect.html" \
      "$DST/2026-05-19-ai-analyst-real-data-supabase/images/hero-supabase-connect.png"
    render "04 cover" \
      "$DST/2026-05-19-data-agent-harness-roadshow/visuals/cover-roadshow.html" \
      "$DST/2026-05-19-data-agent-harness-roadshow/images/cover-roadshow.png"
    ;;
  *)
    echo "Usage: $0 {03-hero-supabase|04-cover-roadshow|all}"
    exit 1
    ;;
esac

echo ""
echo "✅ 完成。@2x 实际输出 = 2400×1260，可在 CMS 自动 downscale 到 1200×630。"
