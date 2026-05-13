---
name: bilibili-upload-skill
description: 用本机 agent-browser CLI 把本地 mp4 自动化投稿到 B 站（member.bilibili.com），覆盖单集投稿（上传 → 填标题/简介/标签/分区/类型 → 立即投稿）、系列加合集（创建合集 → 把多个稿件按顺序加入合集）和封面制作（写 HTML/SVG → headless 渲染成 PNG → 上传到稿件 + 合集）。专门为脚本化批量投稿系列短视频/UP 主连续剧设计。当用户说"把视频发到 B 站"、"投稿到 bilibili"、"批量发 5 集到 B 站"、"在 B 站建合集"、"把这几个视频组成合集"、"给视频做个封面"时使用。
---

# B 站视频投稿自动化 Skill

一套基于 `agent-browser` CLI 的**可复现工作流**，把"打开 B 站创作中心 → 选文件上传 → 填详情 → 立即投稿 → 把多稿件组成合集"这个操作**完全程式化**，专为系列短视频/UP 主连续剧批量投稿设计。

和人工在 B 站后台点来点去相比，这个 skill 能稳定地：
- 一键上传 mp4，自动避开"开启通知"引导弹窗
- 自动把屏幕录屏视频从 B 站默认的"vlog"分区改到"人工智能"等正确主分区
- 自动清掉 B 站默认推荐的乱七八糟标签（REACTION/电视剧/日剧 之类），换成自己的标签
- 自动填 Quill 富文本简介（不会被"matched 2 elements"卡住）
- 真正点上"立即投稿"按钮（而不是被静默存成草稿）
- 投完后批量加进合集
- **写 HTML+SVG 设计封面**，用 `agent-browser set viewport + screenshot` 渲染成 4:3 / 16:9 PNG，自动走 B 站的"双比例同步改动"上传到稿件 + 合集

---

## ⚠️ 红线 / 安全提示

1. **B 站"立即投稿"是不可撤销的公开发布**（投稿后会进 B 站审核流，1-2 小时内就会出现在你的主页）。**只在用户明确说"发到 B 站"时才点立即投稿**；否则只点"存草稿"。
2. **稿件标签里不要塞名人姓名**（B 站会静默拒绝带人名的标签，比如"宁南山"会被丢弃；不会报错，只是没加上）。
3. **合集是公开属性**，命名要用最终对外的名字，不要用 demo/test 这种字眼。

---

## 何时用这个 skill

| 用户说法 | 走哪条流程 |
|---|---|
| "把这个 mp4 发到 B 站" | 流程 A（单集投稿） |
| "投稿到 bilibili / 哔哩哔哩" | 流程 A |
| "批量把这 5 集发到 B 站" | 流程 A × N + 流程 B（建合集） |
| "在 B 站组个合集" / "做成系列" | 流程 B（创建/管理合集） |
| "改一下我那个稿件的标题" | 流程 C（编辑已有稿件） |
| "给视频做个封面" / "封面写 HTML 然后导出图片" | 流程 E（封面制作 + 上传） |
| "删掉那个稿件" | 流程 D（删除稿件，含人机滑块） |
| "替我帮粉丝群发" / "推送给关注者" | ❌ 不在本 skill 范围 |

---

## 工具前提

- 全局 Cursor Rule `use-agent-browser-for-web.mdc` 已启用 → **浏览器操作必须走 `agent-browser`**
- 本机路径：`~/.auto-coder/.autocodertools/agent-browser`
- daemon 必须带**持久 profile** 运行（`agent-browser daemon start`），保证 B 站登录态跨会话保留
- B 站账号需要**已开通投稿权限**（新号要先实名 + 答题）；如果系列要进合集，账号还得**已开通合集权限**（粉丝数 ≥ 1000 自动解锁，左侧栏会出现"恭喜你已获得合集权限"提示气泡）
- 视频文件要求：B 站现行限制是 **≤16GB / 时长 ≤10 小时 / 推荐 MP4/MOV/MKV / 推荐 1080P 或 4K**
- 姊妹 skill：[web-ui-review-skill](../web-ui-review-skill/SKILL.md)（基础动作和坑复用同一套）

---

## 关键 URL

| 用途 | URL |
|---|---|
| 投稿（新视频） | `https://member.bilibili.com/platform/upload/video/frame` |
| 投稿（编辑草稿） | `https://member.bilibili.com/platform/upload/video/frame?type=draft&draftId=<ID>` |
| 稿件管理 | `https://member.bilibili.com/platform/upload-manager/article` |
| 草稿列表 | `https://member.bilibili.com/platform/upload-manager/article?group=draft` |
| 合集管理 | 在稿件管理页顶部 Tab "合集管理 NEW" 进入（无独立 URL，跟随导航） |

---

## 流程 A：单集投稿（约 12 步）

### A0. 准备工作目录 + 检查 daemon

```bash
mkdir -p /tmp/bilibili-upload && cd /tmp/bilibili-upload
~/.auto-coder/.autocodertools/agent-browser daemon status
# 没跑就：agent-browser daemon start
```

### A1. 打开投稿页（**每次都要重新 open**）

```bash
~/.auto-coder/.autocodertools/agent-browser open "https://member.bilibili.com/platform/upload/video/frame"
~/.auto-coder/.autocodertools/agent-browser wait 4000
~/.auto-coder/.autocodertools/agent-browser get url
~/.auto-coder/.autocodertools/agent-browser get title    # 应该是"创作中心"，不是登录页
```

> ⚠️ **大坑**：daemon 控制的 tab 会随用户在浏览器里手动切换而漂移。即使上一次刚操作完 B 站，下一次也可能在 DeepSeek/InfiniSynapse 之类的别的 tab 上。**每次开始操作前必须 open 一次目标 URL**，不能省。

### A2. 截图前先等字体就绪

```bash
~/.auto-coder/.autocodertools/agent-browser eval "document.fonts.ready.then(()=>'fonts ready')"
~/.auto-coder/.autocodertools/agent-browser screenshot /tmp/bilibili-upload/01-frame.png
```

> ⚠️ B 站页面字体加载慢，第一次 screenshot 经常报 `Timeout 10000ms - waiting for fonts to load`。先 `document.fonts.ready` 再截图就 OK。

> ⚠️ **截图必须用绝对路径**（`/tmp/<task>/01.png`）。daemon 当前工作目录不在你 shell 的 cwd，相对路径会报"Saved to ./xxx"但实际找不到文件。

### A3. 上传 mp4（**关键 selector**）

B 站投稿页里有 3 个 `input[type=file]`，**只有藏在 `.bcc-upload-wrapper` 里的那个能真正触发上传流程**：

```bash
~/.auto-coder/.autocodertools/agent-browser upload \
  ".bcc-upload-wrapper input[type=file]" \
  "/绝对路径/EP01.mp4"
~/.auto-coder/.autocodertools/agent-browser wait 5000
```

> ⚠️ **不要**用 ref（`@e7`/`@e8`）或 `input[name="buploader"]`。那两个是 B 站老版本残留的 file input，setInputFiles 上去后页面纹丝不动。
>
> ⚠️ 如果 upload 后页面没变，先 eval 看一下都有几个 file input，找父容器是 `bcc-upload-wrapper` 的那个：
> ```bash
> agent-browser eval "[...document.querySelectorAll('input[type=file]')].map(i=>({accept:i.accept.slice(0,30), parent:i.parentElement?.className}))"
> ```

### A4. 关掉"开启通知"引导弹窗

上传成功后页面会跳转到投稿编辑页，并弹出"开启后视频上传完成第一时间通知"的引导浮层，挡住下面的表单：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "
(() => {
  const btn = [...document.querySelectorAll('button, span')].find(b => 
    ['知道了','取消','确定'].includes(b.innerText.trim()) && b.offsetParent !== null);
  if (btn) { btn.click(); return 'closed'; }
  return 'no popup';
})()"
~/.auto-coder/.autocodertools/agent-browser wait 1500
```

### A5. 填标题（input.input-val）

```bash
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c   # 拿当前 ref
# 标题字段是 placeholder="请输入稿件标题"，maxlength=80
~/.auto-coder/.autocodertools/agent-browser fill @e9 "【系列名 1/5】具体标题，不超过 80 字"
```

### A6. 选"自制"类型（必填，B 站默认两个都没选）

类型字段不是 `<input type=radio>` 而是自定义 div 组件 `.check-radio-v2-container`：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "
(() => {
  const cont = [...document.querySelectorAll('.check-radio-v2-container')].find(n => n.innerText.trim()==='自制');
  if (!cont) return 'not found';
  cont.click();
  return 'clicked';
})()"
```

### A7. 清掉默认推荐标签 + 加入自己的标签

#### A7.1 清掉默认（B 站会瞎猜推荐 REACTION/电视剧/日剧 之类）

每个标签的 × 是 SVG，没有 close class。要找父容器 `.label-item-v2-container` 内的 svg 派发 click，**循环多次**（一次 dispatch 通常只删一个）：

```bash
for i in 1 2 3 4 5; do
  ~/.auto-coder/.autocodertools/agent-browser eval "
  (() => {
    const items = [...document.querySelectorAll('.label-item-v2-container')];
    if (items.length === 0) return 'empty';
    for (const it of items) {
      const close = it.querySelector('svg, [class*=close]');
      if (close) close.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true}));
    }
    return items.length + ' clicked';
  })()"
  ~/.auto-coder/.autocodertools/agent-browser wait 500
done
```

#### A7.2 加自己的标签（**关键：必须用 React 原生 setter + 三连 keydown/press/up 派发**）

普通的 `agent-browser type` 在 B 站标签输入框上**不工作**（看似 type 上去了但 B 站不识别，按 Enter 也无反应）。必须用 native value setter 触发 React onChange：

```bash
for tag in "DeepSeek" "AI大模型" "开源" "人工智能" "深度求索"; do
  ~/.auto-coder/.autocodertools/agent-browser eval "
  (() => {
    const inp = document.querySelector('.input-instance input.input-val[placeholder*=\"Enter\"]');
    if (!inp) return 'no input';
    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    setter.call(inp, '$tag');
    inp.dispatchEvent(new Event('input', {bubbles:true}));
    inp.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', code:'Enter', keyCode:13, bubbles:true}));
    inp.dispatchEvent(new KeyboardEvent('keypress', {key:'Enter', code:'Enter', keyCode:13, bubbles:true}));
    inp.dispatchEvent(new KeyboardEvent('keyup', {key:'Enter', code:'Enter', keyCode:13, bubbles:true}));
    return 'sent: $tag';
  })()"
  ~/.auto-coder/.autocodertools/agent-browser wait 400
done
# 验证最终标签
~/.auto-coder/.autocodertools/agent-browser eval \
  "[...document.querySelectorAll('.label-item-v2-container')].map(i=>i.innerText.trim())"
```

> ⚠️ **B 站标签静默拒绝清单**（实测会被丢弃但不报错）：
> - **人名**（如"宁南山"、"雷军"等任何 KOL/明星名）
> - **复合敏感词**（如"AI大模型"——拒绝；但拆成 "AI" 和 "大模型" 单独加就 OK）
> - **含"国家"/政府机构名**（如"国家统计局"——拒绝；但单独"统计局"或"统计数据"通常 OK）
> - **重复同义词**（一个稿件里"AI" 和 "人工智能"只能留一个，B 站会自动去重）
> - 单个稿件最多 **10 个标签**
>
> 添加完后**必须 eval 实际标签数组核对**，不要相信"sent: xxx"的返回——它只表示派发成功，不代表 B 站收下：
> ```bash
> agent-browser eval "[...document.querySelectorAll('.label-item-v2-container')].map(i=>i.innerText.trim())"
> ```
> 比对预期数组，少了的就是被静默拒绝的，记到 `.bilibili-meta.json` 的 `tags_rejected` 字段方便下次绕开。

### A8. 填简介（Quill 富文本，**关键：用 inserttext 不能用 fill**）

简介字段是 Quill 富文本编辑器，DOM 是 `<div class="ql-editor ql-blank" contenteditable=true>`。页面里有 2 个 ql-editor（一个真的、一个隐藏的 clipboard），所以 `agent-browser fill .ql-editor` 必报 "matched 2 elements"。

正确做法是先 eval focus 第一个，然后 `agent-browser inserttext`：

```bash
~/.auto-coder/.autocodertools/agent-browser eval \
  "document.querySelectorAll('.ql-editor')[0].focus(); 'focused'"

~/.auto-coder/.autocodertools/agent-browser inserttext "你的简介正文，最多 2000 字。

支持换行，支持中文逗号、emoji 📺。

#标签 #放在最后才行 (B 站简介里的 # 标签不会变成实际标签，纯文本)"
```

### A9. 选分区（**屏幕录屏会被默认到 vlog**，AI/数据/技术内容必须手动改）

B 站现在按主分区组织：影视、娱乐、音乐、舞蹈、动画、绘画、鬼畜、游戏、资讯、知识、**人工智能**（新主分区，AI/Agent/数据分析/Prompt/编程教程首选）、科技数码、汽车、生活...

**坑**：屏幕录屏类视频（看上去像 IDE/网页操作）会被 B 站默认归类到"vlog"（属于"生活"主分区），即使内容是技术教程。**必须手动改**。

```bash
# 1. 打开分区下拉
agent-browser eval "document.querySelector('.video-human-type .select-controller').click()"
agent-browser wait 800

# 2. 点中目标主分区（这里以"人工智能"为例）
agent-browser eval "
(() => {
  const items = [...document.querySelectorAll('.drop-list-v2-item-cont')].filter(n=>n.offsetParent!==null);
  const hit = items.find(n => (n.innerText||'').trim()==='人工智能');
  if (!hit) return 'not found';
  hit.click();
  return 'ok';
})()"
agent-browser wait 800
```

> ⚠️ **二级子分区不需要单独选**：B 站点完主分区"人工智能"就直接生效，没有二级菜单展开。
>
> ⚠️ "参与话题"会跟着主分区变（人工智能分区会推荐"科技猎手/动物总动员/萌宠UP主加更计划"之类话题，看着不太搭——这是 B 站后台逻辑，不影响投稿）。

### A10. 关闭浮层提示气泡（**关键：会挡住投稿按钮**）

B 站投稿页底部经常飘着一个 "信息填完后，就可投稿！不需等待上传完成哦~ ×" 的引导气泡，**它正好压在"立即投稿"按钮上方**。先关掉它：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "
(() => {
  const tip = [...document.querySelectorAll('span, i, [class*=close]')].find(n => 
    n.parentElement?.innerText?.includes('信息填完后'));
  if (tip) tip.click();
  return tip ? 'closed' : 'no tip';
})()"
```

### A11. 真正点击"立即投稿"（**关键：必须用 mouse move/down/up，普通 click() 会被当成存草稿**）

`.submit-add` 这个按钮 Vue/React 组件**对合成的 `.click()` 反应是"存草稿"，对真鼠标事件才反应"立即投稿"**。这是本 skill 最大的坑。

正确做法：

```bash
# 1. 先滚到按钮位置
~/.auto-coder/.autocodertools/agent-browser eval "
  document.querySelector('.submit-add').scrollIntoView({block:'center'}); 'scrolled'"
~/.auto-coder/.autocodertools/agent-browser wait 800

# 2. 取按钮中心坐标
~/.auto-coder/.autocodertools/agent-browser eval "
  (() => {
    const r = document.querySelector('.submit-add').getBoundingClientRect();
    return JSON.stringify({cx: r.x + r.width/2, cy: r.y + r.height/2});
  })()"
# → 假设拿到 {cx:564, cy:668}

# 3. 模拟真鼠标点击（agent-browser mouse 没有 click 子命令，要拼三步）
~/.auto-coder/.autocodertools/agent-browser mouse move 564 668
~/.auto-coder/.autocodertools/agent-browser mouse down
~/.auto-coder/.autocodertools/agent-browser mouse up

# 4. 等 8+ 秒（前 5 秒 URL 不变是正常的，B 站后端在审核+发布）
~/.auto-coder/.autocodertools/agent-browser wait 8000
~/.auto-coder/.autocodertools/agent-browser get url
```

**判断成功**：URL 跳到 `https://member.bilibili.com/platform/upload-manager/article`（**没有** `?group=draft`）= 投稿成功，进了"已通过/审核中"。
**判断失败**：URL 跳到 `https://member.bilibili.com/platform/upload-manager/article?group=draft` = **被存成草稿了**，需要回去重点。

### A11.5 ⚠️ 投稿成功的 3 种页面状态（容易误判）

点完投稿后，**URL 不一定会跳转**。判断成功的正确方式（按出现频率排序）：

| 状态 | URL | 页面文字 |
|---|------|------|
| ① 跳成功页 | `upload/video/frame`（**没变**） | 显示"稿件投递成功" + "查看进度/再投一个" |
| ② 跳稿件管理 | `upload-manager/article`（**没有 group=draft**） | 列表页显示新稿件 |
| ③ 跳草稿箱 | `upload-manager/article?group=draft` | 表示**没成功**，被存草稿了 |

**别只看 URL 判断**！`URL == upload/video/frame` 可能是状态①（成功）也可能是状态没变（失败）。必须再 eval 检查：

```bash
agent-browser eval "
(() => {
  const t = document.body.innerText || '';
  if (t.includes('稿件投递成功') || t.includes('再投一个')) return 'YES';
  return 'NO';
})()"
```

> ⚠️ **真实事故**：本 skill 早期版本只用 URL 判断，结果一次脚本误报"失败"，重跑后导致 EP02 重复投稿（同样内容投了 2 个稿件）。删除重复稿件需要人机滑块验证（agent-browser 自动化不了），只能让用户手动滑。

### A12. 验证 + 记录 BV 号

投稿后回到稿件管理页，第一条就是新发布的视频。用 eval 拿 BV 号备用（后面加合集和分享要用）：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "
(() => {
  const links = [...document.querySelectorAll('a[href*=\"BV\"], a[href*=\"video/BV\"]')];
  return links.slice(0,3).map(a => a.href);
})()"
```

把 BV 号 + 标题写到本地存档（参考微信公众号那套 `.wechat-mp-meta.json`）：

```json
{
  "bilibili": {
    "EP01": {
      "title": "【DeepSeek 三年发展史 1/5】...",
      "bv": "BVxxxxxxx",
      "url": "https://www.bilibili.com/video/BVxxxxxxx",
      "submitted_at": "2026-05-05 12:00"
    }
  }
}
```

---

## 流程 B：把多个稿件组成合集

B 站合集机制：**先建合集，再把已投稿的视频按顺序拉进合集**。投稿时虽然有"加入合集"下拉框，但**那个下拉的列表只显示已存在的合集**——空账号下拉打不开（看上去像 bug，其实就是空状态），所以**必须先去合集管理页建合集**。

### B1. 进入合集管理

```bash
~/.auto-coder/.autocodertools/agent-browser open \
  "https://member.bilibili.com/platform/upload-manager/article"
~/.auto-coder/.autocodertools/agent-browser wait 3000
# 然后点击顶部 Tab "合集管理 NEW"
~/.auto-coder/.autocodertools/agent-browser eval "
(() => {
  const tab = [...document.querySelectorAll('a, button, span, div')].find(n => 
    n.innerText?.trim()==='合集管理' && n.offsetParent !== null);
  if (tab) tab.click();
  return tab ? 'clicked' : 'not found';
})()"
~/.auto-coder/.autocodertools/agent-browser wait 3000
```

### B2. 创建新合集

合集管理页右上角有"+添加合集"按钮（注意：**实际文本就是"添加合集"或"+添加合集"，没有空格**）。点击后会进入"编辑合集"页，包含：

- **合集标题**（必填，≤ 50 字，placeholder 是"请输入合集标题"，selector `input[placeholder*="合集标题"]` 或 `input[maxlength="50"]`）
- **合集简介**（≤ 500 字，selector 是页面里唯一可见的 `<textarea>`）
- **合集封面**（≥ 960×540，**点击区域是 `.ep-edit-cover-input` 容器**，对应的 file input selector 是 `input[type=file].ep-edit-cover-input` 或父级带这个 class，accept `image/jpeg, image/jpg, image/png`）

```bash
# 标题（用 React 原生 setter 触发 onChange）
agent-browser eval "
(() => {
  const inp = document.querySelector('input[placeholder*=\"合集标题\"]');
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(inp, '和 AI 一起学数据分析');
  inp.dispatchEvent(new Event('input', {bubbles:true}));
  inp.dispatchEvent(new Event('change', {bubbles:true}));
})()"

# 简介（textarea 也走 native setter）
agent-browser eval "
(() => {
  const ta = document.querySelector('textarea');
  const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
  setter.call(ta, '...合集简介，180 字以内最佳，超过 500 会被截...');
  ta.dispatchEvent(new Event('input', {bubbles:true}));
  ta.dispatchEvent(new Event('change', {bubbles:true}));
})()"

# 封面：先按流程 E1-E4 渲染好 cover-16x9.png（≥ 960×540），然后 upload + 处理裁切框
agent-browser upload "input[type=file].ep-edit-cover-input, .ep-edit-cover-input input[type=file], input[type=file][accept*=jpeg]" \
  "<video-dir>/cover/cover-16x9.png"
agent-browser wait 4000
# B 站会弹"裁切对话框"，默认裁切框已合理，点"确认"即可（见流程 E8）
```

> ⚠️ 提交合集后**会拿到 `合集ID: <seasonId>`**，立刻 eval 抓下来落盘 `.bilibili-meta.json`：
>
> ```bash
> agent-browser eval "
> (() => {
>   const m = (document.body.innerText||'').match(/合集ID[:：]\s*(\d+)/);
>   return m ? m[1] : 'not found';
> })()"
> ```

### B3. 把稿件加入合集

合集创建完后会进入合集详情页，里面有"+ 添加视频"按钮（实际文本是"+添加视频"，无空格）。每加一批视频要：

1. 点"+添加视频" → 弹出"添加单集"对话框
2. 在搜索框搜稿件标题前缀（避免列表只显示最近 3 个）
3. 勾选要加入的稿件 —— **B 站的勾选 selector 是 `.ep-select-box-item-all-checkbox`**
4. 点"下一步" → step 2 设置每集的"单集标题"（**必改成 `EP{N} ...` 前缀**，见 B4 workaround）
5. 点"完成" → 回到合集编辑页
6. **再次点合集编辑页底部的"立即提交"**保存改动（不点会丢）

```bash
# 列出弹窗里所有候选稿件
agent-browser eval "
[...document.querySelectorAll('.ep-select-box-item-all-checkbox')]
  .filter(n=>n.offsetParent !== null)
  .map((c,i)=>{ let p=c; let txt=''; for(let k=0;k<6;k++){p=p.parentElement; if(!p)break;
    const t=(p.innerText||'').slice(0,80); if(t.includes('DeepSeek')){txt=t; break;}}
    return {i, txt}; })"

# 一次性勾选
agent-browser eval "
const cbs=[...document.querySelectorAll('.ep-select-box-item-all-checkbox')].filter(n=>n.offsetParent!==null);
[5,4,2,1,0].forEach(i=>cbs[i]?.click());"
```

> ⚠️ **改 step 2 的"单集标题"输入框 selector 必须限定到 `.ep-table-tr` 内**（合集主表单的"合集标题"也是个 input，不限定的话会把合集名给覆盖了）。**真实事故**：本 skill 早期版本用过 `inp = [...document.querySelectorAll('input')].find(i => i.offsetParent !== null && i.value)` 这种泛 selector，第一次匹配到的是合集主表单的"合集标题"input，结果合集名被改成了"EP01 ..."，事后还得手动改回去。
>
> ⚠️ **添加视频对话框的"单集标题"input 是动态出现的**（点铅笔图标 `.ep-section-edit-video-list-item-title img.title-icon` 后才显示），需要先 click 再 setTimeout 或 wait 几百 ms 才能拿到 input ref。

### B4. ⚠️ 合集顺序：agent-browser 改不动，必须人工拖

**这是本 skill 第二大坑**。合集编辑页每行右侧有 ⇕ drag handle (`.sort-drag` class)，但：

| 尝试 | 结果 |
|---|---|
| HTML5 DnD `DragEvent` dispatchEvent | ❌ 不响应 |
| 真鼠标 `mouse move + down + move...+ up` | ❌ 不响应 |
| `click()` ⇕ handle | 选中行（蓝色高亮）但不弹菜单 |
| 选中后再 click 目标行 ⇕ | ❌ 不交换 |
| 点表头"单集标题"列的 `.ep-table-tr-sort-popover` | ❌ 不是排序，可能是 popover 切换 |

**结论**：B 站合集排序当前**只能人工拖拽**。agent-browser / Playwright 真鼠标都搞不定。

**workaround**（强烈推荐）：在 step 2 修改"单集标题"时，**给每行加 EP01..EP05 前缀**。这样：
1. 合集页观众一眼能识别每集顺序
2. 后台编辑页可以让用户按"单集标题"列升序快速重排（B 站后台允许 UP 主拖，前端拖响应正常，只是 agent-browser 不行）
3. 即使顺序错了，观众也不会迷路

```bash
# 编辑某行的"单集标题"
agent-browser eval "
const row = [...document.querySelectorAll('.ep-table-tr')].filter(r=>r.offsetParent!==null)[ROW_IDX];
const editImg = row.querySelector('.ep-section-edit-video-list-item-title img.title-icon');
editImg.click();
setTimeout(() => {
  const inp = [...document.querySelectorAll('input')].find(i =>
    i.offsetParent !== null && i.value && i.parentElement?.closest('.ep-table-tr'));
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(inp, 'EP01 简短描述');
  inp.dispatchEvent(new Event('input', {bubbles:true}));
  inp.blur();
}, 400);"
```

### B5. 提交合集 + 验证公开 URL

点合集编辑页底部"立即提交"。**这个按钮的 class 是 `.ep-button-primary`**（不是稿件投稿那种 `.submit-add`），但**安全起见仍然用真鼠标 `mouse move + down + up` 点击**：

```bash
# 滚到按钮可见
agent-browser eval "document.querySelector('.ep-button-primary').scrollIntoView({block:'center'})"
agent-browser wait 800

# 取按钮中心坐标 + 真鼠标点击
agent-browser eval "
(() => {
  const btns = [...document.querySelectorAll('.ep-button-primary')].filter(b=>b.offsetParent!==null && (b.innerText||'').trim()==='立即提交');
  const r = btns[0].getBoundingClientRect();
  return JSON.stringify({cx: Math.round(r.x+r.width/2), cy: Math.round(r.y+r.height/2)});
})()"
# 用返回的 cx, cy 走 mouse move/down/up
```

提交后会跳回合集管理列表页，对应卡片显示"正常显示"+ 第一集缩略图。**新创建/修改的合集状态会先短暂显示"正在审核"** 再变"正常显示"，公开 URL 立即可访问。

合集公开 URL：

```
https://space.bilibili.com/<UID>/lists/<seasonId>
```

UID 可以从空间链接拿（B 站后台头像点击 → 个人空间）：

```bash
agent-browser open "https://space.bilibili.com/" && \
agent-browser wait 4000 && \
agent-browser get url   # → https://space.bilibili.com/22610047
```

把 UID + seasonId 写进本地 `.bilibili-meta.json`：

```json
{
  "uploader": {"uid": "22610047", "nick": "..."},
  "collection": {
    "id": "8054209",
    "title": "DeepSeek 这三年",
    "public_url": "https://space.bilibili.com/22610047/lists/8054209"
  },
  "episodes": { ... }
}
```

---

## 流程 D：删除稿件（含人机滑块）

```bash
# 在稿件管理页 hover 到目标行 → 点最右侧 ⋮ → 弹出菜单 → 点"删除稿件"
agent-browser eval "
(() => {
  const link = document.querySelector('a[href*=BV<目标BV>]');
  let row = link;
  while (row && !row.querySelector?.('.bcc-icon-icon_list_more_x')) row = row.parentElement;
  row.querySelector('.bcc-icon-icon_list_more_x').dispatchEvent(new MouseEvent('mouseover',{bubbles:true}));
})()"
agent-browser wait 1000

# 点"删除稿件"
agent-browser eval "
[...document.querySelectorAll('span,div,button,li')].find(n => 
  n.innerText?.trim()==='删除稿件' && n.offsetParent !== null)?.click()"
```

⚠️ **删除时会弹出滑块人机验证**，agent-browser 自动化不了。只能：

1. 让用户手动在浏览器里滑一下
2. 或者用 `AskQuestion` 工具暂停等用户确认完滑块再继续

## 流程 C：编辑已发布稿件

B 站稿件发布后**只能改简介、标签、合集归属、封面**，不能改标题（会触发重新审核）。

```bash
# 1. 在稿件管理页拿到该行的"编辑"链接 → 直接 .click()（普通 a.bili-btn）
agent-browser eval "
(() => {
  const link = document.querySelector('a[href*=BV1evRCBSEUv]');
  let row = link;
  while (row && !((row.className||'').toString().includes('article-card'))) row = row.parentElement;
  const editA = [...row.querySelectorAll('a.bili-btn')].find(a => (a.innerText||'').trim()==='编辑');
  editA.click();
})()"
agent-browser wait 5000

# URL 跳到 https://member.bilibili.com/platform/upload/video/frame?type=edit&bvid=BV...
# 后面跟 A5-A11 一样
```

> ⚠️ **编辑页底部按钮文字仍是"立即投稿"**（不是"立即更新"），且**仍然要走真鼠标 `.submit-add`**——这个 React 行为和投新稿件完全一致。点完再用 A11.5 的"稿件投递成功"文本判断。
>
> ⚠️ 类型（自制/转载）和分区在编辑页是**灰掉不可改**的，所以投稿时一次选对很重要。

---

## 流程 E：制作并上传封面（HTML → PNG → B 站稿件 + 合集）

B 站封面是**首屏点击转化率最大的杠杆**。比起截视频帧，**写 HTML+SVG 渲染**有几个不可替代的好处：

- 字体大小、配色、版式可精细控制（视频帧上的字往往太小）
- SVG 折线图/数据可视化天然适合数据/技术内容封面
- 一份 HTML 可同时输出 4:3（首页推荐）和 16:9（个人空间）两种比例
- 改文案/换 EP 号只改 HTML，不用每次重新设计

### E1. 设计 HTML（建议布局）

工作目录：`<视频目录>/cover/`

```bash
mkdir -p <video-dir>/cover && cd <video-dir>/cover
# 写 cover.html。关键 CSS：
#   html, body { width: 1146px; height: 860px; overflow: hidden; }   /* 4:3 */
#   或 height: 717px;                                                /* 16:9 */
```

布局推荐（grid 三行 `auto 1fr auto`）：

| 区域 | 内容 | 设计要点 |
|---|---|---|
| top | 左：EP 角标（`EP·01 · 系列名`），右：品牌签名 | 字号小（14-16px），不抢主标题 |
| middle 左 | 大标题（66-78px）+ 副标题 | 标题用渐变色 + 高对比，副标题灰白 |
| middle 右 | 一张数据可视化卡片（SVG 折线图/柱图/对比图） | 加圈出框 + 标注箭头，让"故事"一眼看到 |
| footer | hashtag pills + 站点 URL | 与 middle 之间用 `border-top` 分隔 |

> ⚠️ **不要在 chart 里堆 X 轴文字标签**（`jan ── feb ── mar...`）—— 自动换行容易塌成两行。直接在 SVG 里用 `<text>` 画月份数字 1-12。

### E2. 起本地 HTTP 服务（**关键：不能用 `file://`**）

```bash
cd <video-dir>/cover
python3 -m http.server 17812 > /dev/null 2>&1 &
```

> ⚠️ **agent-browser open `file:///path/to/x.html` 会被错误地处理成 `https://file///path/...`**（把 `file:` 当成域名前缀）—— 必须用 http server 绕开。
>
> 17812 是随便挑的端口，避开 8000 之类常用端口减少冲突。

### E3. 用 `set viewport` + `screenshot` 渲染成精确尺寸 PNG

**关键**：daemon 默认 viewport 是 1440×900，截图会带额外区域。必须先 `set viewport <w> <h>` 调成目标尺寸：

```bash
# 4:3 版本（B 站首页推荐封面，必填）
~/.auto-coder/.autocodertools/agent-browser tab new
~/.auto-coder/.autocodertools/agent-browser set viewport 1146 860
~/.auto-coder/.autocodertools/agent-browser open "http://localhost:17812/cover.html"
~/.auto-coder/.autocodertools/agent-browser wait 2000
~/.auto-coder/.autocodertools/agent-browser eval "document.fonts.ready.then(()=>'ok')"
~/.auto-coder/.autocodertools/agent-browser wait 1500    # 等 webfont
~/.auto-coder/.autocodertools/agent-browser screenshot "<video-dir>/cover/cover-4x3.png"

# 16:9 版本（合集封面用，要求 ≥ 960×540）
# 改 cover.html 里 body 的 height 为 717px 后重复上述步骤，输出 cover-16x9.png
```

> ⚠️ **不要试图用 `chrome --headless=new --window-size=W,H --screenshot=...`** —— 实测 chrome headless 经常截到的尺寸对，但内容布局被诡异截断（chart 卡片底部 footer 不见了，但 DOM 里 footer 实际存在）。`agent-browser set viewport + screenshot` 走的是 daemon 浏览器，截图所见即所得。
>
> ⚠️ **新开 `tab new`** 截图，避免你的 cover daemon tab 跟 B 站 tab 互相切换导致截图把 B 站截下来了。完事后 `tab list` 找到 B 站 tab 切回去（`tab <n>`）。

### E4. 验证截图尺寸

```bash
file <video-dir>/cover/cover-4x3.png
# → PNG image data, 1146 x 860, 8-bit/color RGB, non-interlaced
```

### E5. 把封面应用到稿件（编辑模式）

```bash
# 1. 进稿件管理 → 点该行"编辑"（流程 C）
# 2. 在编辑页找"封面设置"按钮并点击
agent-browser eval "
(() => {
  const btn = [...document.querySelectorAll('*')].find(n => 
    (n.innerText||'').trim()==='封面设置' && n.offsetParent !== null && n.children.length === 0);
  btn.click();
})()"
agent-browser wait 2500

# 3. 弹出"封面制作"模态框。直接 upload 到 image 类型的 file input
#    selector: input[type=file][accept*=image]   父节点是 .bcc-upload-wrapper（display:none 但能 setInputFiles）
agent-browser upload "input[type=file][accept*=image]" "<video-dir>/cover/cover-4x3.png"
agent-browser wait 4000
```

### E6. 勾选"双比例同步改动"（一图变两个比例）

模态框右上角有 4:3 和 16:9 两个面板，旁边有 `双比例同步改动` 复选框（class `.sync-checkbox-wrapper`）。**勾上以后只上传 4:3 一张图，B 站会自动从中间裁切派生 16:9**：

```bash
agent-browser eval "document.querySelector('.sync-checkbox-wrapper').click()"
agent-browser wait 1500
```

> ⚠️ **设计封面时要把"重要内容"放在中央 644 px 高的区域**（4:3 → 16:9 的中央带）。EP 角标和底部 hashtag 在 16:9 派生时会被裁掉是预期行为。

### E7. 完成 + 立即投稿

```bash
# 关 4:3/16:9 模态：找文本"完成"的 button
agent-browser eval "
(() => {
  const btn = [...document.querySelectorAll('button, span, div')].find(n => 
    (n.innerText||'').trim()==='完成' && n.offsetParent !== null && n.children.length === 0);
  let p = btn;
  while (p && p.tagName !== 'BUTTON' && !(p.className||'').toString().includes('btn')) p = p.parentElement;
  (p||btn).click();
})()"
agent-browser wait 3000

# 然后走流程 A11 / C 的真鼠标 .submit-add 点击 + A11.5 的"稿件投递成功"判断
```

### E8. 同一张图也用作合集封面

合集封面要求 **≥ 960×540（16:9）**。直接复用 `cover-16x9.png`（1146×717）：

```bash
# 在合集创建/编辑页的"合集封面"区
agent-browser upload "input[type=file].ep-edit-cover-input, .ep-edit-cover-input input[type=file], input[type=file][accept*=jpeg]" \
  "<video-dir>/cover/cover-16x9.png"
agent-browser wait 4000
```

> ⚠️ **B 站合集封面会弹一个"裁切对话框"**（不是直接覆盖）。`<= 960×540` 等比缩放后展示一个可拖动的裁切框 + 右侧最终效果预览。一般默认裁切框已覆盖你的主要内容，**不需要拖动，直接点底部"确认"**：
>
> ```bash
> agent-browser eval "
> (() => {
>   const btn = [...document.querySelectorAll('button, span, div')].find(n => 
>     (n.innerText||'').trim()==='确认' && n.offsetParent !== null && n.children.length === 0);
>   let p = btn;
>   while (p && p.tagName !== 'BUTTON' && !(p.className||'').toString().includes('btn')) p = p.parentElement;
>   (p||btn).click();
> })()"
> ```

### E9. 落盘 meta

```json
{
  "cover": {
    "html": "cover/cover.html",
    "png_4x3": "cover/cover-4x3.png",
    "png_16x9": "cover/cover-16x9.png",
    "applied_to_video": true,
    "sync_dual_ratio": true,
    "updated_at": "2026-05-05 15:05"
  }
}
```

### E10. 清理

```bash
pkill -f "python3 -m http.server 17812"
agent-browser set viewport 1440 900   # 恢复 daemon 默认 viewport，避免影响其它任务
```

---

## 常见报错 → 修法对照

| 报错 / 现象 | 修法 |
|---|---|
| `Selector matched N elements` | 用 `agent-browser eval` 列出所有候选，加 nth/可见性过滤 |
| 截图 `waiting for fonts to load` 超时 | 先 `eval "document.fonts.ready..."` 再截图 |
| upload 后页面纹丝不动 | 换 selector 到 `.bcc-upload-wrapper input[type=file]` |
| 标签输入 type 后没反应 | 改用 React native value setter + dispatch 三连 |
| `.submit-add` 点了跳到 `?group=draft` | 改用 `mouse move + down + up` 真鼠标点击 |
| 立即投稿点了 5 秒内 URL 没变 | **正常**，B 站后端慢，再等 5-8 秒；**必须 eval 检查"稿件投递成功"文本**而不是只看 URL |
| 标签里某个词加不上 | 大概率是人名 / 敏感词 / 含"国家"，换一个；用 eval 实际数组核对最终标签 |
| 简介不显示填的内容 | 滚动 ql-editor 容器；filter 的内容可能在最上面 |
| 弹窗关不掉 | `eval` 找文本是"知道了/我知道了/确定"的 button 强行 click |
| daemon 不在 B 站 tab | 直接 `agent-browser open <URL>` 重新打开，不要点 sidebar |
| 分区被默认成 vlog | A9：手动展开 `.video-human-type .select-controller`，点 `.drop-list-v2-item-cont` 含目标分区文本的项 |
| 合集列表只有 3 个候选 | 在搜索框搜稿件标题前缀（默认列表分页/限量） |
| 合集顺序拖不动 | **承认 agent-browser 搞不定**，用"单集标题"加 EP01..EP05 前缀作 workaround，让用户人工拖 |
| 删除稿件弹滑块验证 | **承认搞不定**，用 AskQuestion 让用户手动滑或者保留重复稿件 |
| 误判投稿失败导致重复投稿 | 严守 A11.5 的成功判断逻辑（必查"稿件投递成功"文字） |
| 合集名被改成了 EP01 单集标题 | 改单集标题时 selector 必须限定到 `.ep-table-tr` 内，否则匹配到的是合集主表单的"合集标题"input |
| `agent-browser open file:///x.html` 报 `https://file///x.html` 错 | 必须用 `python3 -m http.server <port>` 起本地 http，再 `open http://localhost:<port>/x.html` |
| 渲染封面截图被截断/尺寸不对 | 不要用 `chrome --headless=new --window-size`；必须用 `agent-browser set viewport <w> <h>` + `screenshot` |
| 合集封面上传完没生效 | 注意会先弹"裁切对话框"，要再点一次"确认"；裁切框已默认覆盖好不需要拖 |
| `.ep-button-primary "立即提交"` `.click()` 不响应 | 改用真鼠标 `mouse move + down + up`；坐标用 `getBoundingClientRect` 拿 |
| 编辑页找不到"立即更新"按钮 | **B 站没有"立即更新"按钮**，编辑模式下底部按钮文字仍是"立即投稿"（且仍要真鼠标点 `.submit-add`） |

---

## 反模式（见到就阻止自己）

1. ❌ 用 `agent-browser fill` 操作 Quill `.ql-editor` → 必报 "matched 2 elements"
2. ❌ 用 `.click()` 点立即投稿（含编辑模式） → 静默被存成草稿，看不出区别但视频没真发
3. ❌ 不关浮层气泡就点投稿 → 气泡挡住按钮，点到的可能是气泡的 dismiss 区
4. ❌ 标签里塞名人名字 / 含"国家"的政府机构名 → 静默拒绝，标签数对不上但不报错
5. ❌ 投稿后 5 秒内 URL 没变就以为失败 → B 站后端常用 8+ 秒
6. ❌ 默认推荐标签不清就加自己的 → 标签会越加越多，超过 10 个上限被自动截断（**例外**：B 站给的 3 个默认标签如"数据/人工智能/数据分析"如果对题就保留，省一个标签数）
7. ❌ 跨任务复用 daemon 的 tab → tab 早飘到别的站点了，每次必须重新 open 目标 URL
8. ❌ screenshot 用相对路径 → 写到了 daemon 的 cwd（不知道在哪），找不到文件
9. ❌ 用 `agent-browser open file:///x.html` → CLI 会拼成 `https://file///x.html` 导致 ERR_CONNECTION_CLOSED；必须 http server
10. ❌ 用 `chrome --headless=new --window-size --screenshot` 渲封面 → 截图尺寸看似对但内容异常（footer 不见、底部留空带），改用 `agent-browser set viewport + screenshot`
11. ❌ 屏幕录屏视频投稿不改分区 → 默认在 vlog 区，AI/技术内容曝光会被错误的同分区视频稀释
12. ❌ 改合集里某行的"单集标题"用泛 `input` selector → 会先匹配到合集主表单的"合集标题"input，把合集名给覆盖；必须限定到 `.ep-table-tr` 内
13. ❌ 改完合集就不再点"立即提交" → 改动会丢；step 2/3 完成只是关掉添加视频弹窗，外层合集编辑页还要再 submit 一次

---

## 与其他 skill / rule 的关系

- **前置规则**：`~/.cursor/rules/use-agent-browser-for-web.mdc` —— 决定"所有浏览器操作走 agent-browser"
- **姊妹 skill**：
  - [`web-ui-review-skill`](../web-ui-review-skill/SKILL.md) —— 基础动作（snapshot / eval / click / 截图）的母 skill
  - [`wechat-mp-draft-skill`](../wechat-mp-draft-skill/SKILL.md) —— 同样基于 agent-browser 操控发布平台，结构可对比参考
  - [`article-to-narrated-video-skill`](../article-to-narrated-video-skill/SKILL.md) —— 把文章变成口播视频（产出本 skill 要发布的 mp4 文件）

---

## 实战案例

### 案例 1：DeepSeek 三年发展史（5 集系列，无封面 HTML）

参考 `~/projects/william-docs/宣发/微信公众号文章/2026-05-04-DeepSeek三年发展史宁南山风格/video/` 里的 5 集系列：

- 5 集 mp4 文件在 `video/output/EP01..05.mp4`
- 投稿 helper 脚本在 `video/tools/publish_bilibili.sh`（覆盖 A1-A12 所有步骤，单集 30 秒搞定）
- meta 信息（BV 号、合集 URL、UID、已知问题）写在 `video/.bilibili-meta.json`（必须首次投稿后立即落盘，方便后续编辑/删除）

发布成果：
- 合集"DeepSeek 这三年" → https://space.bilibili.com/22610047/lists/8054209
- 5 集 BV 号对应关系见 `.bilibili-meta.json`
- 已知遗留：1 个重复 EP02 待删（人机滑块）；合集顺序待人工拖

每一集的标题/简介按以下模板：

```
【系列名 N/M】具体标题
↓
EP{N} 主题（本集）
EP{1..M} 系列目录列表
↓
#标签 #分集 #系列
```

### 案例 2：和 AI 一起学数据分析 EP01（首次跑流程 E 封面 + 流程 B 合集）

参考 `~/projects/william-docs/产品/InfiniSynapse/视频/infinisynapse-unemployment-tutorial/`：

- 视频源：`数据分析追问思维-青年失业率AI实操.mp4`（从 `v9-3-with-subs-narrated.mp4` 重命名）
- 封面：`cover/cover.html`（手写 HTML+SVG，含 2024/2025 同月对比折线图 + 6-7 月跳升标注）
  - `cover/cover-4x3.png` 1146×860（首页推荐封面）
  - `cover/cover-16x9.png` 1146×717（个人空间封面 + 合集封面）
- 投稿 + 编辑 + 合集 meta：`.bilibili-meta.json`

发布成果：
- 单集 BV1evRCBSEUv → https://www.bilibili.com/video/BV1evRCBSEUv/
- 合集"和 AI 一起学数据分析" seasonId=8055478 → https://space.bilibili.com/22610047/lists/8055478
- 分区改成"人工智能"主分区（B 站新增）
- 标签 `国家统计局` 被静默拒绝（含"国家"），其余 10 个全部进了
- 流程 E：先用 1146×860 渲染 4:3 PNG → 上传时勾选"双比例同步改动"→ 16:9 自动从中间裁切派生

每一集的"单集标题"按以下模板（合集排序 workaround 必备）：

```
EP{N} {主题} · {主问题描述}
```

例：`EP01 青年失业率 · 主问题 + 追问 + AI 自我纠错`

---

## 与流程 A 配套的 helper 脚本骨架

完整可运行版见 `<project>/video/tools/publish_bilibili.sh`，核心结构：

```bash
#!/usr/bin/env bash
set -e
EP="$1"; VIDEO="$2"; TITLE="$3"; DESC_FILE="$4"
AB="$HOME/.auto-coder/.autocodertools/agent-browser"

# A1 open  → A3 upload → A4 dismiss popup → A5 fill title (eval native setter)
# → A6 自制 → A7 clear+add tags → A8 inserttext desc → A10 close tip
# → A11 mouse 三步 → A11.5 eval 检查"稿件投递成功"文字 → A12 拿 BV 号

# 关键：投稿成功判断必须双重 (URL + 文本)
SUCCESS=$("$AB" eval "
  (document.body.innerText||'').includes('稿件投递成功') ? 'YES' : 'NO'" | tail -1 | tr -d '\"')
if [[ "$URL" == *"upload-manager/article"* && "$URL" != *"group=draft"* ]] || [[ "$SUCCESS" == "YES" ]]; then
  echo "✅ $EP success"
fi
```

调用示例：

```bash
bash publish_bilibili.sh EP02 \
  "/path/to/EP02.mp4" \
  "【DeepSeek 三年发展史 2/5】..." \
  /tmp/desc/EP02.txt
```

---

*本 skill 的每一条实践都来自 2026-05 真实投稿验证：*

*— 第一波（无封面）：5 集 DeepSeek 系列，UID 22610047，合集 ID 8054209，覆盖流程 A/B/C/D*

*— 第二波（含封面）：InfiniSynapse "和 AI 一起学数据分析" EP01 (BV1evRCBSEUv)，UID 22610047，合集 ID 8055478，覆盖流程 E（HTML→PNG 封面）+ 流程 B 重新走通*

*后续遇到新坑请直接更新此文件。*
