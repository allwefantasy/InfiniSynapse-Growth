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
  local label="$1" html="$2" png="$3" h="$4"
  mkdir -p "$(dirname "$png")"
  echo "▶ $label (1080×${h})"
  "$CHROME" \
    --headless=new \
    --hide-scrollbars \
    --disable-gpu \
    --force-device-scale-factor=2 \
    --window-size="1080,${h}" \
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

render "退档坑对照表" \
  "$ROOT/visuals/table-pitfalls.html" \
  "$ROOT/images/table-pitfalls.png" \
  720

render "小程序字段对照表" \
  "$ROOT/visuals/table-miniprogram.html" \
  "$ROOT/images/table-miniprogram.png" \
  1100

render "72小时自查表" \
  "$ROOT/visuals/table-72h.html" \
  "$ROOT/images/table-72h.png" \
  680

render "产品能力表" \
  "$ROOT/visuals/table-features.html" \
  "$ROOT/images/table-features.png" \
  620

render "数据源表" \
  "$ROOT/visuals/table-datasources.html" \
  "$ROOT/images/table-datasources.png" \
  560

echo ""
echo "完成。表格已导出为 PNG。"
