#!/usr/bin/env bash
# 发布到微信公众号草稿箱（流程 A：新建）
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$ARTICLE_DIR/../../Skills/wechat-mp-draft-skill" && pwd)"
AGENT=~/.auto-coder/.autocodertools/agent-browser
TITLE="普通家庭大学生如何自己填志愿？出分后 72 小时，先把这 6 件事算清楚"
AUTHOR="InfiniSynapse"

cd "$ARTICLE_DIR"

# 1) HTML 准备
python3 "$SKILL_DIR/bin/md2html.py" --in article.md --out-html article-mp.html --out-b64 article-mp.html.b64
python3 "$SKILL_DIR/bin/inject-styles.py" --in article-mp.html --out-html article-mp.html --out-b64 article-mp.html.b64

# 2) 检查登录
$AGENT open "https://mp.weixin.qq.com/"
sleep 2
URL=$($AGENT get url 2>&1 | tail -1)
if [[ "$URL" != *"home/index"* ]]; then
  echo "❌ 未登录公众号。请在 agent-browser 打开的 Chrome 窗口里扫码登录，然后重新运行本脚本。"
  exit 2
fi
TOKEN=$(echo "$URL" | grep -oE 'token=[0-9]+' | head -1 | cut -d= -f2)
echo "✓ 已登录, token=$TOKEN"

# 3) 新建图文
$AGENT click --text "文章" --exact
sleep 3
$AGENT tab list
TAB=$($AGENT tab list 2>&1 | grep 'appmsg_edit' | sed -n 's/.*\[\([0-9]*\)\].*/\1/p' | tail -1)
if [[ -z "$TAB" ]]; then
  TAB=2
fi
$AGENT tab "$TAB"
sleep 3

# 4) 填标题作者
$AGENT snapshot -i -c | head -15
$AGENT fill @e4 "$TITLE"
sleep 0.5
$AGENT fill @e5 "$AUTHOR"
sleep 0.5

# 5) paste 正文（正文 ProseMirror = index 1）
B64=$(cat article-mp.html.b64)
$AGENT eval "(() => {
  const b64 = '${B64}';
  window.__article_html = decodeURIComponent(escape(atob(b64)));
  return 'html_len=' + window.__article_html.length;
})()"

$AGENT eval "(() => {
  const pms = document.querySelectorAll('.ProseMirror');
  const pm = pms[1] || pms[0];
  if (!pm) return 'NO_PM';
  pm.focus();
  const ph = pm.querySelector('.editor_content_placehold');
  if (ph) ph.remove();
  const dt = new DataTransfer();
  dt.setData('text/html', window.__article_html);
  dt.setData('text/plain', window.__article_html.replace(/<[^>]+>/g, ''));
  pm.dispatchEvent(new ClipboardEvent('paste', {
    clipboardData: dt, bubbles: true, cancelable: true,
  }));
  return JSON.stringify({
    pm_inner_len: pm.innerHTML.length,
    placeholder_count: pm.querySelectorAll('[data-image-placeholder]').length,
    h1_count: pm.querySelectorAll('h1').length,
  });
})()"

# 6) 上传图片（按 md 出现顺序）
IMGS=(
  "$ARTICLE_DIR/images/家族群聊-退档焦虑.png"
  "$ARTICLE_DIR/images/张雪峰-普通家庭选专业.png"
  "$ARTICLE_DIR/images/table-pitfalls.png"
  "$ARTICLE_DIR/images/table-miniprogram.png"
  "$ARTICLE_DIR/images/小程序界面.jpg"
  "$ARTICLE_DIR/images/下载报告.jpg"
  "$ARTICLE_DIR/images/报告pdf.jpg"
  "$ARTICLE_DIR/images/table-72h.png"
  "$ARTICLE_DIR/images/table-features.png"
  "$ARTICLE_DIR/images/小程序组件.jpg"
  "$ARTICLE_DIR/images/table-datasources.png"
)
$AGENT upload "input[type=file]" "${IMGS[@]}"
sleep 8

# 7) 替换占位符 + 记录 CDN mapping
$AGENT eval "(() => {
  const pm = document.querySelectorAll('.ProseMirror')[1] || document.querySelector('.ProseMirror');
  const uploaded = [...pm.querySelectorAll('img')]
      .filter(i => i.src && i.src.includes('mmbiz.qpic.cn'));
  const placeholders = [...pm.querySelectorAll('[data-image-placeholder]')];
  if (uploaded.length < placeholders.length) {
    return 'NOT_ENOUGH: uploaded=' + uploaded.length + ' placeholders=' + placeholders.length;
  }
  const mapping = {};
  for (let i = 0; i < placeholders.length; i++) {
    const key = placeholders[i].getAttribute('data-image-placeholder');
    mapping[key] = uploaded[i].src;
    const newP = document.createElement('p');
    newP.style.textAlign = 'center';
    newP.innerHTML = '<img src=\"' + uploaded[i].src + '\" style=\"max-width:100%;\" alt=\"\"/>';
    placeholders[i].parentNode.replaceChild(newP, placeholders[i]);
  }
  for (const img of uploaded) {
    let section = img.closest('section');
    while (section && section.parentElement && section.parentElement.tagName === 'SECTION') {
      const parent = section.parentElement;
      const parentText = (parent.innerText || '').replace(/\\s+/g, '');
      const selfText = (section.innerText || '').replace(/\\s+/g, '');
      if (parentText.length > selfText.length + 3) break;
      section = parent;
    }
    const selfText = (section && section.innerText || '').replace(/\\s+/g, '');
    if (section && selfText.length < 3 && section.parentElement) {
      section.remove();
    }
  }
  window.__cdn_mapping = mapping;
  return JSON.stringify({
    replaced: placeholders.length,
    mapping,
    final_placeholders: pm.querySelectorAll('[data-image-placeholder]').length,
  }, null, 2);
})()" > /tmp/mp-paste-result.json

cat /tmp/mp-paste-result.json

# 8) 保存草稿
$AGENT eval "window.scrollTo(0,0); const mi = document.querySelector('.mock-iframe'); if (mi) mi.scrollTop = 0;"
sleep 0.5
$AGENT click --text "保存为草稿"
sleep 4
FINAL_URL=$($AGENT get url 2>&1 | tail -1)
echo "FINAL_URL=$FINAL_URL"
APPMSGID=$(echo "$FINAL_URL" | grep -oE 'appmsgid=[0-9]+' | head -1 | cut -d= -f2 || true)
echo "appmsgid=$APPMSGID"

# 9) 写 meta
python3 - <<PY
import json, re
from pathlib import Path
from datetime import datetime

art = Path("$ARTICLE_DIR")
result = Path("/tmp/mp-paste-result.json").read_text()
# extract mapping JSON from eval output
m = re.search(r'\{[\s\S]*"mapping"[\s\S]*\}', result)
mapping = json.loads(m.group())["mapping"] if m else {}

meta = {
    "appmsgid": "$APPMSGID",
    "title": "$TITLE",
    "author": "$AUTHOR",
    "token": "$TOKEN",
    "last_saved": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "cdn_urls": mapping,
}
(art / ".wechat-mp-meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Wrote .wechat-mp-meta.json")
PY

$AGENT screenshot "$ARTICLE_DIR/mp-draft-saved.png"
echo "✅ 草稿已保存"
