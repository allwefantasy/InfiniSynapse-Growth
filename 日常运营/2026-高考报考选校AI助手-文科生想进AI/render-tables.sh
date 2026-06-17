#!/usr/bin/env bash
# 将 visuals/*.html 表格图卡渲染为 images/*.png
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
CHROME=""
for path in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
  if [[ -x "$path" ]]; then CHROME="$path"; break; fi
done

if [[ -z "$CHROME" ]]; then
  echo "未找到 Chrome，请先安装"
  exit 1
fi

render() {
  local label="$1" html="$2" png="$3" w="$4" h="$5"
  mkdir -p "$(dirname "$png")"
  echo "▶ $label (${w}×${h})"
  "$CHROME" \
    --headless=new \
    --hide-scrollbars \
    --disable-gpu \
    --force-device-scale-factor=2 \
    --window-size="${w},${h}" \
    --screenshot="$png" \
    --default-background-color=FFFFFFFF \
    "file://${html}" \
    > /dev/null 2>&1
  if [[ -f "$png" ]]; then
    echo "  ✅ $png"
  else
    echo "  ❌ 失败: $png"
    exit 1
  fi
}

render "产品能力表" \
  "$ROOT/visuals/table-features.html" \
  "$ROOT/images/09-你能得到什么.png" \
  760 720

render "数据源表" \
  "$ROOT/visuals/table-datasources.html" \
  "$ROOT/images/10-主要数据源.png" \
  760 420

echo ""
echo "完成。表格已导出为 PNG，可在 article.md 中引用。"
