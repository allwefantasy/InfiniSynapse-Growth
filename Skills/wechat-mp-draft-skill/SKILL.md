---
name: wechat-mp-draft-skill
description: 用本机 agent-browser CLI 把一篇 Markdown 文章（含本地图片）自动化地发布/更新到微信公众号**草稿箱**。覆盖：本地 md 先落盘到 william-docs 存档、标题/作者/正文粘贴、本地图片批量上传到 mmbiz CDN、图片占位符替换、ProseMirror 编辑器去重 H1、**覆盖更新已有草稿时复用 CDN URL 不重传**、保存草稿后的验证。全程只保存草稿绝不点"发表"。当用户说"帮我写一篇公众号"、"把这篇文章发到公众号草稿"、"粘贴到公众号里"、"上传到 mp.weixin.qq.com"、"保存到草稿箱"、"覆盖上一次的草稿"、"改一下公众号里那篇"时使用。
---

# 微信公众号草稿自动化 Skill

一套基于 `agent-browser` CLI 的**可复现工作流**，把"Markdown 落盘到 william-docs → 打开公众号后台 → 新建图文（或进入已有草稿）→ 填标题作者 → 粘贴富文本正文 → 批量上传图片到 mmbiz CDN → 替换占位符 → 保存为草稿"这个 8~11 步的操作**完全程式化**。

和人工在公众号后台点来点去相比，这个 skill 能在 ~30 秒内把一篇 3000 字 + 6 张图的 Markdown 稳定转成微信草稿，而且**后续每次改稿都能原样覆盖回去**，本地 md 始终是 single source of truth。

---

## ⚠️ 绝对红线

**只保存草稿，绝对不要点"发表"按钮**。

公众号"发表"是**一次性、不可撤销**的动作，点了之后文章立刻推送给全体关注者。本 skill 的全部流程**在"保存为草稿"那一步就必须停下**。如果用户没有明确说"替我真的发出去"，**永远只走到草稿为止**。

最终 URL 里含 `appmsgid=XXXXX` = 草稿已保存；**永远不要访问任何带 `publish` / `send` / `post` 字样的 action**。

---

## 什么时候用这个 skill

| 用户说法 | 走哪条流程 |
|---|---|
| "把这篇文章 / markdown 发到公众号草稿" | 流程 A（新建） |
| "帮我在公众号后台建一个草稿" | 流程 A |
| "把本地的 md + 图片传到微信公众号" | 流程 A |
| "改一下公众号里那篇草稿的标题 / 正文" | **流程 B（覆盖更新）** |
| "把上一版草稿整个换成这个新版本" | **流程 B** |
| "覆盖上次保存的草稿" | **流程 B** |
| "直接替我发出去" | ❌ 先跟用户确认发草稿 or 发表；默认只发草稿 |
| "群发" / "推送给粉丝" | ❌ 不在本 skill 覆盖范围 |

---

## 工具前提

- 全局 Cursor Rule `use-agent-browser-for-web.mdc` 已启用 → **浏览器操作必须走 `agent-browser`**
- 本机 `agent-browser` 路径：`~/.auto-coder/.autocodertools/agent-browser`
- daemon 必须带**持久 profile** 运行（`agent-browser daemon start`），确保微信公众号登录态跨会话保留
- Python 3 + `markdown` 包（`pip3 install markdown`），用于把 md 转成公众号能识别的 HTML
- 配套脚本：[`bin/md2html.py`](bin/md2html.py)
- 姊妹 skill：[web-ui-review-skill](../web-ui-review-skill/SKILL.md)（基础动作和坑复用同一套）

---

## 硬规则：先本地落盘，后操作公众号

**所有 markdown 源文必须先存在 `william-docs` 仓库里，再去动公众号。**

为什么这是硬规则：

- **/tmp 重启就丢**。改了三版之后想回到第二版就找不回了。
- **公众号编辑器里的内容只是"草稿快照"**，每次覆盖更新都会冲掉上一版的正文 DOM。要迁平台（知乎、掘金、少数派）或改样式，都得回到本地 md。
- **走 git 版本控制**，每一稿的 `article-vN.md` 或 commit diff 一看就清楚。
- **Agent 接力的上下文**：下一个 Agent 要改这篇文章时，能从本地拿到最新 md 作为输入，不用反向从公众号编辑器 DOM 里抓。

### 目录约定

```
~/projects/william-docs/产品/<产品名>/文章/<topic>/
├── article.md                    ← 公众号正文源 (必须, 每次发布都以这份为准)
├── images/
│   ├── 01-<step>.png
│   ├── 02-<step>.png
│   └── ...
├── .wechat-mp-meta.json          ← 草稿元数据 (首次发布后记下来)
│   {
│     "appmsgid": "100002236",     // 公众号分配的草稿 ID, 覆盖更新时要用
│     "title": "<当前标题>",
│     "cdn_urls": {                // 每张本地图片对应的 mmbiz CDN URL
│       "images/01-dashboard.png": "https://mmbiz.qpic.cn/...",
│       ...
│     },
│     "last_saved": "2026-04-23 09:04"
│   }
└── article-vN.md                 ← (可选) 历史版本存档
```

`article.md` 是 single source of truth。每次要改公众号文章，**先改这份 md**（用 Read/StrReplace/Write 工具），**再运行 skill 覆盖到公众号**。

### 落盘命令

```bash
ARTICLE_DIR=~/projects/william-docs/产品/Auto-Coder/文章/<topic>
mkdir -p "$ARTICLE_DIR/images"

# 1) 把 markdown 用 Write 工具写到 "$ARTICLE_DIR/article.md"
#    (绝不要用 echo / cat heredoc, 中文转义会出问题)

# 2) 图片用 cp / mv 到 images/ 目录下
cp /path/to/some/screenshot.png "$ARTICLE_DIR/images/01-dashboard.png"

# 3) 确认文件结构
ls -la "$ARTICLE_DIR"
ls -la "$ARTICLE_DIR/images"
```

**落盘完成才开始动 agent-browser**。md 在仓库里有源文，任何阶段出错都能从头重跑，不会丢稿。

---

## 决策树：进来之后先问自己 4 件事

```
Q1. Markdown 源文落盘了吗?
    ├─ NO  ─▶ 先 Write 到 william-docs/产品/.../article.md, 再继续
    └─ YES ─▶ 往下走

Q2. 这次是新建草稿还是覆盖更新?
    ├─ 首次发 / 全新主题     ─▶ 流程 A (新建)
    ├─ 已经有草稿, 只想换正文/标题/图 ─▶ 流程 B (覆盖更新)
    └─ 不确定 ─▶ 看 article.md 同目录下有没有 .wechat-mp-meta.json:
                有 appmsgid 字段 = 走 B, 没有 = 走 A

Q3. daemon 登录态还在吗?
    ├─ 打开 home?token=...  后看到"新的创作"区块 ─▶ 已登录, 继续
    └─ 看到扫码登录页 ─▶ ask 用户手机扫码, 登完再继续

Q4. 图片是本地文件还是网络 URL?
    ├─ 本地文件 ─▶ 走标准流程
    └─ 外链 URL ─▶ ❌ 微信会把外链图替换成默认占位
                 先 curl 下载到 images/, 再走本地上传流程
```

---

# 流程 A：从 0 发布一篇新草稿

**适用场景**：公众号里还没有这篇文章的草稿，全新发布。

### 0. 本地落盘 + daemon 预检

```bash
ARTICLE_DIR=~/projects/william-docs/产品/Auto-Coder/文章/<topic>
# (用 Write/StrReplace 工具写好 article.md 和 images/)
ls "$ARTICLE_DIR/article.md" "$ARTICLE_DIR/images/"

~/.auto-coder/.autocodertools/agent-browser daemon status
# 没跑就: agent-browser daemon start
~/.auto-coder/.autocodertools/agent-browser set viewport 1440 900
```

**md 里图片路径必须用相对路径** `images/XX.png`。绝对路径或 `~/...` 开头的路径会在后面的正则匹配里失败。

### 1. 打开公众号后台首页

```bash
~/.auto-coder/.autocodertools/agent-browser open "https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=<user_token>"
~/.auto-coder/.autocodertools/agent-browser wait 2000
~/.auto-coder/.autocodertools/agent-browser get url
~/.auto-coder/.autocodertools/agent-browser screenshot ./01-home.png
```

**token 怎么来**：用户第一次会把含 `token=` 的完整 URL 给你；存到 `.wechat-mp-meta.json` 或本次会话内复用。token 每天/每次登录会刷新，所以过时了要让用户重新给。

如果截图看到扫码登录页，**先 ask 用户手动扫码**，daemon 的 profile 把登录态存下来，下次就不用再扫。

### 2. 点"文章"打开图文编辑器（注意 tab 切换）

```bash
# 有两个"文章"元素 (页面顶部菜单 + 创作入口), 必须用精确 selector
~/.auto-coder/.autocodertools/agent-browser click --text "文章" --exact
```

**点完当前 tab 没变化** —— 因为公众号点"文章"是**新开 tab**，必须手动切：

```bash
~/.auto-coder/.autocodertools/agent-browser wait 3000
~/.auto-coder/.autocodertools/agent-browser tab list
# 输出类似:
#   [0] 公众号 - .../home?...
#   [1] 公众号 - .../home?...
# → [2] 公众号 - .../appmsg_edit_v2&action=edit&isNew=1&type=77&...
~/.auto-coder/.autocodertools/agent-browser tab 2
~/.auto-coder/.autocodertools/agent-browser wait 3000
~/.auto-coder/.autocodertools/agent-browser get url     # 确认 URL 含 appmsg_edit
```

**判定口径**：URL 含 `appmsg_edit_v2&action=edit&isNew=1` = 在新图文编辑器里。

### 3. 填标题和作者

```bash
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c
# 典型输出:
#  - textbox [ref=e3]                      ← 合集名 (无关)
#  - textbox "请在这里输入标题" [ref=e4]  ← 标题
#  - textbox "请输入作者" [ref=e5]        ← 作者
#  - textbox "选填..."    [ref=e6]        ← 摘要 (可留空)
#  - button "发表" [ref=e12]              ← ⛔ 绝不点
#  - button "预览" [ref=e13]
#  - button "保存为草稿" [ref=e14]         ← 目标

~/.auto-coder/.autocodertools/agent-browser fill @e4 "<标题>"
~/.auto-coder/.autocodertools/agent-browser wait 500
~/.auto-coder/.autocodertools/agent-browser fill @e5 "<作者>"
```

标题 64 字符上限，作者 8 字符上限。超长不会报错，会直接截断。

### 4. 把 Markdown 转成 HTML + Base64

公众号编辑器 **不认 Markdown 语法**。`## xxx` 或 `**xxx**` 直接贴进去只会保留原始符号。必须先转成 HTML。

```bash
cd "$ARTICLE_DIR"
python3 ~/projects/william-docs/skills/global/wechat-mp-draft-skill/bin/md2html.py \
    --in article.md \
    --out-html article.html \
    --out-b64 article.html.b64
# 输出会列出:
#   - md_source: article.md (NNNN chars)
#   - html: article.html (NNNN chars)
#   - b64: article.html.b64 (NNNN chars)
#   - images found (N): images/01-xxx.png, ...
```

`md2html.py` 做 3 件事：

1. **删掉源文件第一个 H1**（`^# 标题`）—— 因为公众号顶部已经有单独的"标题"输入框了，正文 H1 会重复
2. **把 `![alt](images/XX.png)` 转成醒目占位段落**：`<p data-image-placeholder="images/XX.png" style="...">【待上传图片：<alt>】</p>`
3. **输出 base64 版本**：避免 shell 传长字符串时的转义问题

### 5. 把 HTML 通过 paste event 注入 ProseMirror ⭐ 本 skill 最关键一步

公众号编辑器用 **ProseMirror** 做正文富文本。ProseMirror 是一个 "managed document" —— 它内部维护自己的 state 副本，**你直接 `innerHTML = ...` 给 `.ProseMirror` 这个 div 是没用的**，下一次 view 渲染就会把你改的 DOM 覆盖回去。

**唯一稳定的注入方式是模拟用户的 `paste` 事件**：

```bash
# 先把 HTML base64 放到 window 变量上（避开 shell 转义）
B64=$(cat article.html.b64)
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const b64 = '${B64}';
  window.__article_html = decodeURIComponent(escape(atob(b64)));
  return 'html_len=' + window.__article_html.length;
})()"

# 然后触发 paste 事件
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
  if (!pm) return 'NO_PM';
  pm.focus();

  // 清掉 placeholder, 否则 paste 内容会被夹在 placeholder 文字前后
  const ph = pm.querySelector('.editor_content_placehold');
  if (ph) ph.remove();

  const dt = new DataTransfer();
  dt.setData('text/html', window.__article_html);
  dt.setData('text/plain', window.__article_html.replace(/<[^>]+>/g, ''));

  pm.dispatchEvent(new ClipboardEvent('paste', {
    clipboardData: dt,
    bubbles: true,
    cancelable: true,
  }));

  return JSON.stringify({
    pm_inner_len: pm.innerHTML.length,
    first_child: pm.firstElementChild && pm.firstElementChild.tagName,
    text_first_100: pm.innerText.slice(0, 100),
    placeholder_count: pm.querySelectorAll('[data-image-placeholder]').length,
    h1_count: pm.querySelectorAll('h1').length,
  });
})()"
```

**验证 paste 成功的信号**：

- `pm_inner_len` 从几百跳到几千（HTML 实际长度）
- `first_child` = `SECTION`
- `text_first_100` 是文章的开头文字
- `placeholder_count` = 图片数
- `h1_count` = 0（md2html.py 已删 H1；如果不是 0，走 Step 8 去重）

**如果 `pm_inner_len` 没变**：

- 大概率 `.ProseMirror` 选错了节点 —— 公众号有好几个隐藏 ProseMirror 实例（标题栏、摘要栏都是）。确认 `document.querySelectorAll('.ProseMirror').length`，选 `#ueditor_0 .mock-iframe-document` 下那个可见的。
- 或者 placeholder 没清干净，编辑器拒绝了 paste。

**几个容易踩的坑**：

- ❌ `pm.innerHTML = html`：无效，ProseMirror 会回滚
- ❌ `document.execCommand('insertHTML', false, html)`：不稳定
- ❌ eval 里直接嵌几 KB HTML 字符串：shell 转义会吃掉一半引号/反斜杠，必须走 base64
- ✅ `paste` event + DataTransfer 是 ProseMirror **原生支持的用户输入路径**，它会自己走 transaction 处理

### 6. 图片批量上传到 mmbiz CDN

先探入口：公众号编辑器页面有一个**全局隐藏 `input[type=file]`**，挂在 `.tpl_dropdown_menu_item`（工具栏"图片 → 本地上传"菜单项）里：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const fi = document.querySelector('input[type=file]');
  return fi ? JSON.stringify({
    accept: fi.accept,
    multiple: fi.multiple,
    parent: (fi.parentElement.className||'').slice(0,60)
  }) : 'NO';
})()"
# 典型:
#   { accept: "image/gif,image/jpeg,image/jpg,image/png,image/svg,image/webp",
#     multiple: true,
#     parent: "tpl_dropdown_menu_item" }
```

**不需要点工具栏的"图片"按钮**。直接往 input 推文件——`agent-browser upload` 底层就是设置 files + 派发 change：

```bash
~/.auto-coder/.autocodertools/agent-browser upload "input[type=file]" \
    "$ARTICLE_DIR/images/01-xxx.png" \
    "$ARTICLE_DIR/images/02-xxx.png" \
    "$ARTICLE_DIR/images/03-xxx.png" \
    # ... 一次性传所有图片, 顺序就是将来对应到占位符的顺序
~/.auto-coder/.autocodertools/agent-browser wait 5000    # 等上传完成 + CDN 回填
```

**上传发生什么**：

1. 微信后台把每张图压缩上传到 mmbiz CDN
2. 返回 URL 形如 `https://mmbiz.qpic.cn/sz_mmbiz_png/<hash>/0?wx_fmt=png&from=appmsg`
3. **上传完的图全部追加到正文末尾**（按上传顺序），**不会自动插到占位符位置**——搬运要自己做
4. 每张图在 DOM 里是**一对 `<img>`**：一个带真实 src，一个 src 为空（微信编辑器内部 loading 组件，正常现象）

**验证**：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
  const uploaded = [...pm.querySelectorAll('img')]
      .filter(i => i.src && i.src.includes('mmbiz.qpic.cn'));
  return JSON.stringify({
    count: uploaded.length,
    first_3: uploaded.slice(0,3).map(i => i.src.slice(-40))
  });
})()"
# count == 你传的图片数 → 全部上传成功
```

**大坑：upload 后 CDN 没回填 ⚠️**

有些场景下（**尤其是在"流程 B 覆盖更新"中间做补传单张新图时**），`agent-browser upload` 返回成功、`input.files.length = 1`，但**等再久微信也不会真的把图上传到 CDN**——`mmbiz.qpic.cn` 的图一直出不来。原因是 `agent-browser upload` 底层设置完 `files` 属性后派发的 `change` 事件在微信编辑器这个"长会话"里会被吞掉；微信的上传 controller 要靠"用户点了图片菜单 → 选本地上传"这条路径把内部状态激活，直接设 files 会跳过这个激活。

**救场动作**：**手动派发一次 change 事件**，强制触发微信的上传 handler：

```bash
~/.auto-coder/.autocodertools/agent-browser upload "input[type=file]" "$PATH_TO_NEW_IMG"
~/.auto-coder/.autocodertools/agent-browser wait 5000
# ↑ 检查 mmbiz.qpic.cn 的图没出来? 那就派发 change:
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const input = document.querySelector('input[type=file]');
  input.dispatchEvent(new Event('change', { bubbles: true }));
  return 'dispatched, files=' + input.files.length;
})()"
~/.auto-coder/.autocodertools/agent-browser wait 8000   # 派发后多等, CDN 压缩需要时间
```

这一招在"第一次发布时一次性传 N 张图"的场景下**通常不需要**（upload 命令走的正路径一次搞定），但**在"覆盖更新时补传一张新图"的场景下几乎每次都要**。

### 7. 把 CDN 图替换到占位符位置 + 清理末尾 + 记录 CDN URL

**这一步除了替换, 还要顺手把 CDN URL 存进 `.wechat-mp-meta.json`**, 方便下次覆盖更新时直接复用, 不用再重传.

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
  const uploaded = [...pm.querySelectorAll('img')]
      .filter(i => i.src && i.src.includes('mmbiz.qpic.cn'));
  const placeholders = [...pm.querySelectorAll('[data-image-placeholder]')];
  if (uploaded.length < placeholders.length) {
    return 'NOT_ENOUGH: uploaded=' + uploaded.length + ' placeholders=' + placeholders.length;
  }

  // Step A: 记下每个占位符对应的 CDN URL (供后续存 meta)
  const mapping = {};
  for (let i = 0; i < placeholders.length; i++) {
    const key = placeholders[i].getAttribute('data-image-placeholder');
    mapping[key] = uploaded[i].src;
  }

  // Step B: 按顺序把占位符替换成 <p><img/></p>
  for (let i = 0; i < placeholders.length; i++) {
    const src = uploaded[i].src;
    const newP = document.createElement('p');
    newP.style.textAlign = 'center';
    newP.innerHTML = '<img src=\"' + src + '\" style=\"max-width:100%;\" alt=\"\"/>';
    placeholders[i].parentNode.replaceChild(newP, placeholders[i]);
  }

  // Step C: 清理末尾 — 上传的原始图容器 (section 里只含 img 没正文文字)
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

  return JSON.stringify({
    replaced: placeholders.length,
    mapping,
    final_img_count: pm.querySelectorAll('img').length,
    final_placeholders: pm.querySelectorAll('[data-image-placeholder]').length,
  }, null, 2);
})()" > /tmp/paste-result.json

# 从输出里抽出 mapping, 存到 .wechat-mp-meta.json
# (实际操作中可以用 python 读 /tmp/paste-result.json 的 mapping 字段, 合并到 meta)
```

**判定口径**：

- `replaced` == 占位符数
- `final_placeholders` == 0
- `final_img_count` ≈ 2 × 占位符数（每张图的"真 img + loading 占位"都会计入，正常）

### 8. 去掉正文里重复的 H1（仅当 md2html.py 没删掉时用）

如果 `md2html.py` 已经在源头删了 H1（本 skill 提供的脚本默认这么做），跳过此步。

**大坑**：直接 `h1.remove()` 后，1~2 秒内 ProseMirror 会根据它的内部 state 把 H1 重新渲染回来。这不是 race，是 ProseMirror 的设计。

**正确姿势**：选中 H1 的内容范围，走按键事件让 ProseMirror 自己处理删除：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
  const h1 = pm.querySelector('h1');
  if (!h1) return 'NO_H1';
  const range = document.createRange();
  range.selectNodeContents(h1);
  if (h1.nextElementSibling) {
    range.setEndBefore(h1.nextElementSibling);
  } else {
    range.setEndAfter(h1);
  }
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  pm.focus();
  return 'selected: ' + sel.toString().slice(0, 40);
})()"

~/.auto-coder/.autocodertools/agent-browser press Delete
~/.auto-coder/.autocodertools/agent-browser wait 300
~/.auto-coder/.autocodertools/agent-browser press Backspace
~/.auto-coder/.autocodertools/agent-browser wait 500

~/.auto-coder/.autocodertools/agent-browser eval "document.querySelector('.ProseMirror').querySelectorAll('h1').length"
# 应该输出 0
```

### 9. 保存为草稿 + 抽取 appmsgid + 写回 meta

```bash
~/.auto-coder/.autocodertools/agent-browser eval "window.scrollTo(0,0); document.querySelector('.mock-iframe').scrollTop = 0;"
~/.auto-coder/.autocodertools/agent-browser wait 500
~/.auto-coder/.autocodertools/agent-browser screenshot ./09-top-check.png
# 读图确认: 标题/作者/正文第一段正常, 没有多余 H1

# 点"保存为草稿" (⛔ 不是"发表")
~/.auto-coder/.autocodertools/agent-browser click --text "保存为草稿"
~/.auto-coder/.autocodertools/agent-browser wait 3000
~/.auto-coder/.autocodertools/agent-browser screenshot ./10-saved.png

# 抽取草稿 ID
FINAL_URL=$(~/.auto-coder/.autocodertools/agent-browser get url)
echo "$FINAL_URL"
# 应该含 appmsgid=<纯数字> , 这就是草稿 ID
APPMSGID=$(echo "$FINAL_URL" | grep -oE 'appmsgid=[0-9]+' | head -1 | cut -d= -f2)
echo "appmsgid = $APPMSGID"
```

**把 `appmsgid` 和 CDN URL mapping 写回 `.wechat-mp-meta.json`** — 这是流程 B 的前提：

```bash
# 用 Write/StrReplace 工具编辑:
#   $ARTICLE_DIR/.wechat-mp-meta.json
# 结构见前面 "目录约定" 那节
```

### 10. 验证

1. **底部绿色横幅"已保存"** → 截图里可见
2. **URL 含 `appmsgid=<纯数字>`**（保存前是 `isNew=1`）
3. **左下"历史版本"多一条"手动保存"记录**
4. **草稿箱列表首条就是这篇**：
   ```bash
   ~/.auto-coder/.autocodertools/agent-browser open "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=list&begin=0&count=10&isNew=1&type=77&createType=0&token=<token>&lang=zh_CN"
   ~/.auto-coder/.autocodertools/agent-browser wait 3000
   ~/.auto-coder/.autocodertools/agent-browser screenshot ./11-draft-list.png
   ```

**告诉用户**：草稿在草稿箱里，标题 `<...>`，`appmsgid=<...>`，未发表，本地 md 和 meta 都已存档。

---

# 流程 B：覆盖更新已有草稿

**适用场景**：公众号里已经有这篇文章的草稿（有 `appmsgid`），只想换标题/正文/图片，**保持同一张草稿卡**。

**核心优化**：**不重新上传图片**。上次发布时图片已经在 mmbiz CDN 上有 URL，这次直接复用。

### 0. 本地改 md + 读 meta

```bash
ARTICLE_DIR=~/projects/william-docs/产品/Auto-Coder/文章/<topic>
# 先用 Write/StrReplace 改 article.md (源头更新)
# 图片如需增减, 也先改 images/ 目录

# 读 meta 拿 appmsgid
cat "$ARTICLE_DIR/.wechat-mp-meta.json"
# 记下 appmsgid 和 cdn_urls
```

**硬规则**：不要直接在公众号编辑器里"将就改"而不更新本地 md。否则 single source of truth 失守，下次就对不上了。

### 1. 进入已有草稿的编辑页

有两种进入方式，任选其一：

**方式 A：直接开编辑 URL（推荐，少一次点击）**

```bash
~/.auto-coder/.autocodertools/agent-browser open "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&reprint_confirm=0&type=77&appmsgid=<APPMSGID>&token=<TOKEN>&lang=zh_CN"
~/.auto-coder/.autocodertools/agent-browser wait 3000
~/.auto-coder/.autocodertools/agent-browser get url
# 确认含 appmsgid=<APPMSGID>
```

**方式 B：从草稿箱点进去**

```bash
~/.auto-coder/.autocodertools/agent-browser open "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=list&begin=0&count=10&isNew=1&type=77&createType=0&token=<TOKEN>&lang=zh_CN"
~/.auto-coder/.autocodertools/agent-browser wait 2500
~/.auto-coder/.autocodertools/agent-browser click --text "<原标题的任意一段>"
~/.auto-coder/.autocodertools/agent-browser wait 3000
~/.auto-coder/.autocodertools/agent-browser tab list
# 可能会新开 tab, 切过去
```

### 2.（可选）从 DOM 提取现有 CDN URL 重建 meta

如果 `.wechat-mp-meta.json` 丢了或第一次发布时没存，这一步能从编辑器 DOM 里把 CDN URL 抓回来：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
  const urls = [...pm.querySelectorAll('img')]
      .map(i => i.src)
      .filter(s => s && s.includes('mmbiz.qpic.cn'));
  return JSON.stringify(urls, null, 2);
})()"
# 输出按 DOM 顺序的 6 条 mmbiz.qpic.cn URL
# 手动对应到 images/01-xxx.png ... images/06-xxx.png, 写进 .wechat-mp-meta.json 的 cdn_urls
```

**关键假设**：本地 `article.md` 里图片出现的顺序 = 编辑器 DOM 里图片出现的顺序。如果中间换过图/删过图，这个假设会破，要按标题或内容锚点人工对齐。

### 3. 改标题（如需）

```bash
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c | head -20
# 看当前 textbox ref (通常还是 e4/e5/e14)
~/.auto-coder/.autocodertools/agent-browser fill @e4 "<新标题>"
~/.auto-coder/.autocodertools/agent-browser wait 500
# 作者如果也要改: fill @e5 "<新作者>"
```

### 4. 清空 ProseMirror 正文 ⭐ 覆盖更新关键

不能直接把新 HTML paste 上去——会被追加到旧正文后面。必须先清空。

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
  pm.focus();
  const range = document.createRange();
  range.selectNodeContents(pm);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  return 'selected: ' + sel.toString().length + ' chars';
})()"

~/.auto-coder/.autocodertools/agent-browser press Delete
~/.auto-coder/.autocodertools/agent-browser wait 800

# 验证: 正文应只剩 placeholder 和 0 图
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
  return JSON.stringify({
    imgs: pm.querySelectorAll('img').length,
    text_len: pm.innerText.length,
    first_30: pm.innerText.slice(0, 30)
  });
})()"
# 期望: imgs=0, text_len <= 15, first_30 包含 "从这里开始写正文"
```

**为什么能工作**：Range 全选 + Delete 是 ProseMirror 原生支持的编辑动作，和用户按 Cmd+A+Delete 等价，state 会被正确更新，不会被回滚。

### 5. 转新 HTML + paste（跟流程 A Step 4+5 一样）

```bash
cd "$ARTICLE_DIR"
python3 ~/projects/william-docs/skills/global/wechat-mp-draft-skill/bin/md2html.py \
    --in article.md \
    --out-html article.html \
    --out-b64 article.html.b64

B64=$(cat article.html.b64)
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const b64 = '${B64}';
  window.__article_html = decodeURIComponent(escape(atob(b64)));
  return 'html_len=' + window.__article_html.length;
})()"

~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
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
    pm_len: pm.innerHTML.length,
    placeholder_count: pm.querySelectorAll('[data-image-placeholder]').length,
    h1_count: pm.querySelectorAll('h1').length,
  });
})()"
```

### 6. 用缓存的 CDN URL 替换占位符（不走 upload）⭐ 流程 B 的优化点

从 `.wechat-mp-meta.json` 里读 `cdn_urls` 字段，按 key 匹配占位符：

```bash
# 把 JSON 一行化塞进 eval
CDN_JSON=$(cat "$ARTICLE_DIR/.wechat-mp-meta.json" | python3 -c 'import json,sys; m=json.load(sys.stdin); print(json.dumps(m["cdn_urls"]))')
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const urls = ${CDN_JSON};
  const pm = document.querySelector('.ProseMirror');
  const placeholders = [...pm.querySelectorAll('[data-image-placeholder]')];
  const results = [];
  for (const ph of placeholders) {
    const key = ph.getAttribute('data-image-placeholder');
    const url = urls[key];
    if (!url) { results.push({key, status: 'NO_URL'}); continue; }
    const p = document.createElement('p');
    p.style.textAlign = 'center';
    p.innerHTML = '<img src=\"' + url + '\" style=\"max-width:100%;\" alt=\"\"/>';
    ph.parentNode.replaceChild(p, ph);
    results.push({key, status: 'OK'});
  }
  return JSON.stringify({
    replaced: results.length,
    results,
    final_placeholders: pm.querySelectorAll('[data-image-placeholder]').length,
    final_img_count: pm.querySelectorAll('img').length,
  }, null, 2);
})()"
```

**判定口径**：

- 每条结果 `status: 'OK'`，没有 `NO_URL`
- `final_placeholders` == 0
- `final_img_count` == 图片数（**不是 2×**，因为没走上传流程就没有那个 loading 占位 img）

**有 `NO_URL` 怎么办**（新增了本地图但 meta 里没对应 URL）：

这是流程 B 最常见的半路扩展场景 —— "本次改稿新加了一张图"。处理步骤：

```bash
# 1) 单独 upload 这一张新图
~/.auto-coder/.autocodertools/agent-browser upload "input[type=file]" "$ARTICLE_DIR/images/<new>.png"
~/.auto-coder/.autocodertools/agent-browser wait 5000

# 2) 检查 CDN 是否回填 (覆盖更新场景下, 这里经常回填失败, 需要手动派发 change)
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const pm = document.querySelector('.ProseMirror');
  const known = new Set(Object.values(/* meta.cdn_urls */));
  const newOnes = [...pm.querySelectorAll('img')]
      .filter(i => i.src && i.src.includes('mmbiz.qpic.cn') && !known.has(i.src));
  return JSON.stringify({ new_count: newOnes.length });
})()"

# 如果 new_count = 0 (没回填), 手动派发 change 强制触发上传:
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const input = document.querySelector('input[type=file]');
  input.dispatchEvent(new Event('change', { bubbles: true }));
  return 'dispatched';
})()"
~/.auto-coder/.autocodertools/agent-browser wait 8000
```

然后**用"从 DOM 里筛不在 meta.cdn_urls 集合里的 img"**这个策略定位新图的 CDN URL，替换那个 `NO_URL` 占位符，并清理末尾 section。完成后**记得把新图 URL 写回 `meta.cdn_urls`**。

### 7. 保存 + 验证 + 回写 meta

```bash
~/.auto-coder/.autocodertools/agent-browser eval "window.scrollTo(0,0); document.querySelector('.mock-iframe').scrollTop = 0;"
~/.auto-coder/.autocodertools/agent-browser wait 500
~/.auto-coder/.autocodertools/agent-browser screenshot ./b-top.png

~/.auto-coder/.autocodertools/agent-browser click --text "保存为草稿"
~/.auto-coder/.autocodertools/agent-browser wait 3000
~/.auto-coder/.autocodertools/agent-browser get url
# URL 中 appmsgid 应该保持不变 → 说明是覆盖更新, 不是新建
~/.auto-coder/.autocodertools/agent-browser screenshot ./b-saved.png
```

**判定覆盖更新成功**：

- 绿色"已保存"横幅 ✓
- URL 里的 `appmsgid` 和流程 B Step 0 读到的一致（未产生新 ID）
- 草稿箱里还是一张卡片（数量没变），但更新时间变了
- 左下"历史版本"列表多一条

最后更新 `.wechat-mp-meta.json` 的 `last_saved` 字段 + 新标题。

---

## 反模式（见到就阻止自己）

1. ❌ **点了"发表"按钮** —— 不可撤销，会推送给所有粉丝。永远只点"保存为草稿"
2. ❌ **md 只放在 `/tmp/` 或工作目录里就开干** —— 改几版就找不回原稿。源 md 必须先进 `william-docs/产品/.../文章/<topic>/article.md`
3. ❌ **没写 `.wechat-mp-meta.json` 就结束了** —— 下次想覆盖更新时拿不到 `appmsgid` 和 CDN URL，只能退化成重建新草稿（旧草稿变孤儿）
4. ❌ **覆盖更新时重新 upload 所有图片** —— 浪费 CDN 配额、浪费时间、产生重复素材。正确做法是从 meta / DOM 提取现有 URL 再 paste
5. ❌ **直接在公众号编辑器里改字却不同步回本地 md** —— single source of truth 失守，下次覆盖时会丢掉这次改动
6. ❌ **直接 `pm.innerHTML = html`** —— ProseMirror 会回滚。必须用 paste event
7. ❌ **外链图片 URL (`http://xxx.com/foo.png`)** —— 微信会替换成默认占位。先 `curl` 下载到 `images/` 再上传
8. ❌ **直接 `h1.remove()`** —— ProseMirror 会自动恢复。用 Range.selectNodeContents + press Delete
9. ❌ **清空正文时用 `pm.innerHTML = ''`** —— 同理会被回滚。必须用 Range 全选 + press Delete（流程 B Step 4 的做法）
10. ❌ **忘了切 tab** —— 点"文章"是新开 tab
11. ❌ **忘了等上传** —— `agent-browser upload` 返回快，但 CDN 要 3~5 秒。没 `wait 5000` 就去找 `mmbiz.qpic.cn` 会捞到空
12. ❌ **覆盖更新补传新图后, 只调 upload 不派发 change 事件** —— 微信编辑器在"长会话"里会吞掉 `agent-browser upload` 自带的 change，`files.length=1` 但 CDN 永远不回填。解决：手动 `input.dispatchEvent(new Event('change', { bubbles: true }))` 再 wait（见流程 B Step 6 的"有 NO_URL 怎么办"）
13. ❌ **eval 里直接嵌长字符串** —— shell 转义会吃引号/反斜杠。长 HTML 必须走 base64
14. ❌ **image alt 含单引号或反引号** —— 放在 `innerHTML` 里会破坏字符串
15. ❌ **跨会话复用 @eN ref** —— 编辑器 DOM 频繁重渲染，ref 很快失效
16. ❌ **让 AI 自己决定"发表还是草稿"** —— 除非用户**明确说**"替我发出去"，默认永远只发草稿

---

## 与其他 skill / rule 的关系

- **前置规则**：`~/.cursor/rules/use-agent-browser-for-web.mdc`（所有浏览器操作走 agent-browser）
- **姊妹 skill**：
  - [web-ui-review-skill](../web-ui-review-skill/SKILL.md) —— 基础 8 个通用动作和"ProseMirror / DnD / 超长字符串"那类坑的处理，本 skill 直接复用
  - [screen-subtitled-recording-skill](../screen-subtitled-recording-skill/SKILL.md) —— 如果想给公众号配视频 + 字幕，先跑这个再来发
- **可选配合**：公众号草稿存好后，用 `markdown2pdf` 工具（`~/.auto-coder/.autocodertools/markdown2pdf convert article.md`）同时导一份 PDF 作为备份分发

---

## 一张图总结：两条流程并排

```
         ┌─────────────────────────────────────┐
         │ 先落盘 william-docs/产品/.../article.md │
         │         + images/ + (或已有 meta)       │
         └──────────────────┬──────────────────┘
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
   有 .wechat-mp-meta.json                  没有 meta
   (已存在草稿)                              (首次发布)
          │                                   │
          ▼                                   ▼
    ━━ 流程 B ━━                        ━━ 流程 A ━━
    1. 读 meta 拿 appmsgid               1. open home
    2. open appmsg_edit&appmsgid=<id>   2. click "文章" → tab 2
       (或从草稿箱点)                    3. fill 标题/作者
    3. (可选) 从 DOM 抓 CDN URL          4. md2html → b64
       重建 meta                         5. paste event 注入 ProseMirror
    4. fill 新标题                       6. upload 本地图片到 mmbiz CDN
    5. Range 全选 + press Delete         7. eval: 占位符↔CDN URL 替换
       清空正文                             + 清理末尾 + 抓 CDN URL mapping
    6. md2html → paste 新 HTML           8. (如有 H1 残留) Range+press Del
    7. 用 meta.cdn_urls 替换占位符       9. click "保存为草稿" ⛔ 不是发表
       (不重 upload)                       抽 appmsgid
    8. (新图才 upload)                  10. 写 meta (appmsgid + cdn_urls)
    9. click "保存为草稿"               11. 验证
       URL 里 appmsgid 不变 = OK
   10. 更新 meta.last_saved
          │                                   │
          └─────────────────┬─────────────────┘
                            ▼
                       草稿箱里就是它
                       (未发表, 本地有源, 有 meta)
```

---

## 记住 8 个口诀就够了

1. **先本地 md 后公众号**，article.md 是 single source of truth，meta 记草稿 ID
2. **永远只点"保存为草稿"**，绝不点"发表"
3. **点"文章"要切 tab**，新 tab 在 `tab 2`
4. **正文不能 innerHTML**，用 `paste` 事件注入 `text/html`
5. **长 HTML 走 base64**，eval 参数别直接传字符串
6. **图片直接推 `input[type=file]`**，上传完自己搬占位符，**第一次发布完立刻把 CDN URL 存进 meta**
7. **覆盖更新不重传图**，用 meta.cdn_urls 匹配占位符；只有新增的图才 upload
8. **清空正文用 Range + Delete**，H1 去重也一样，`remove()` 会被 ProseMirror 回滚

---

*本 skill 的每一条实践来自 2026-04-23 发两版公众号文章的真实工作流（3192 字新建 + 3312 字覆盖更新，两次复用同一套 6 张 mmbiz CDN 图）。后续遇到新坑请直接更新此文件。*
