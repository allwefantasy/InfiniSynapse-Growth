# 微信公众号编辑器兼容性硬规则

> 提炼自 [`xiaohuailabs/xiaohu-wechat-format`](https://github.com/xiaohuailabs/xiaohu-wechat-format) 的实战经验。
> 这些**不是技巧**，是**兼容性问题**——不遵守就显示不出来或样式被抹掉。

---

## 1. 样式必须 100% 内联

微信公众号编辑器（基于 ProseMirror + 自定义 sanitizer）会**激进地清洗 HTML**：

| 元素 | 命运 |
|---|---|
| `<style>` 块 | 整段删除 |
| `<link rel="stylesheet">` | 删除 |
| `class="xxx"` 属性 | 全部抹掉 |
| `id="xxx"` 属性 | 抹掉 |
| `<script>` | 删除 |
| `data-*` 属性 | 大部分抹掉（保留少数白名单） |
| **`style="..."`** | **保留** ✅ |

### ✅ 正确

```html
<p style="font-size: 16px; line-height: 1.7; color: #333; margin: 16px 0;">段落内容。</p>
```

### ❌ 错误（无效）

```html
<style>p { font-size: 16px; }</style>
<p>段落内容。</p>

<p class="paragraph">段落内容。</p>
```

### 实操要点

- 每个标签都要带完整 `style`，**不要靠继承**（部分继承也会被规则化吞掉）
- `<strong>` `<em>` 这类语义标签**也要内联样式**，否则就是默认浏览器样式
- 颜色用 hex 或 rgb，**不要用 CSS variable**（`var(--primary)` 在 sanitize 时可能被丢）

---

## 2. `<ul>` / `<ol>` 的样式会被抹平

这是微信最坑的一条：你写

```html
<ul style="padding-left: 20px; margin: 16px 0;">
  <li style="margin-bottom: 8px;">item 1</li>
  <li style="margin-bottom: 8px;">item 2</li>
</ul>
```

微信会把 `padding`、`margin`、`list-style` 全部抹回零，你看到的就是 bullet 紧贴版心、行距零。

### 解决方案：用 `<section>` + flexbox 模拟列表

```html
<section style="margin: 16px 0;">

  <section style="display: flex; align-items: flex-start; margin-bottom: 8px;">
    <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #326891; margin-top: 9px; margin-right: 12px; flex-shrink: 0;"></span>
    <section style="flex: 1; font-size: 15px; line-height: 1.7; color: #333;">item 1</section>
  </section>

  <section style="display: flex; align-items: flex-start; margin-bottom: 8px;">
    <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #326891; margin-top: 9px; margin-right: 12px; flex-shrink: 0;"></span>
    <section style="flex: 1; font-size: 15px; line-height: 1.7; color: #333;">item 2</section>
  </section>

</section>
```

**有序列表**：把 `<span>` 里的圆点换成数字（`1.`、`2.`），并改 `width`、`background`、`color`：

```html
<span style="display: inline-block; min-width: 22px; font-weight: 700; color: #326891; margin-right: 8px; flex-shrink: 0;">1.</span>
```

### 嵌套列表

最多嵌套 2 层。第二层把 `margin-left` 加大（如 24px），bullet 颜色变浅、变小。

> ProTip：`md2wechat.py` 自动做这个转换。手写很容易漏。

---

## 3. 外部链接会被微信屏蔽

微信公众号**所有非微信域名的链接都不可点击**。直接放 `<a href="https://example.com">` 等于：

- 蓝色下划线样式还在
- 但点击没反应
- 被微信小程序内置浏览器拦截 / 提示"非官方链接"

### 解决方案：转脚注

正文里：

```html
本文参考了 OpenAI 的官方博客<sup style="color: #326891;">[1]</sup>，特别是关于 ...
```

文末附脚注列表：

```html
<section style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #e0e0e0;">
  <p style="font-size: 13px; color: #888; margin-bottom: 6px;">
    [1] OpenAI Blog: https://openai.com/blog/...
  </p>
  <p style="font-size: 13px; color: #888; margin-bottom: 6px;">
    [2] ...
  </p>
</section>
```

读者会**手动复制 URL**到浏览器去访问。这是公众号生态的现实。

### 例外：微信生态内的链接

- 公众号自家文章（`mp.weixin.qq.com/s/...`）：可点击 ✅
- 微信视频号、小程序：用专门 schema，可跳转 ✅
- 其他所有外链：必须转脚注

---

## 4. 代码块横向滚动

代码长行多，必须能横向滚动而不撑爆版心。

```html
<section style="background: #f6f8fa; border-radius: 6px; padding: 14px 16px; margin: 16px 0; overflow-x: auto; font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; line-height: 1.5; color: #24292e;">
<pre style="margin: 0; white-space: pre;"><code>def hello():
    print("一行很长很长很长很长很长很长很长很长很长很长的代码")</code></pre>
</section>
```

关键：

- 外层 `<section>` 上 `overflow-x: auto`
- `<pre>` 用 `white-space: pre`（不要 `pre-wrap`，否则不滚动）
- `<code>` 不带额外样式，让 pre 控制

### 行内代码

```html
<code style="background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-family: Consolas, Menlo, monospace; font-size: 0.9em; color: #d6336c;">code</code>
```

---

## 5. CJK（中英混排）排版细节

这是中文公众号 vs 英文 blog 的关键差异。**职业作者一眼就能看出来排版的好坏**。

### 5.1 中英文/中数字之间加空格

| 错误 | 正确 |
|---|---|
| `Chrome浏览器` | `Chrome 浏览器` |
| `iOS17系统` | `iOS 17 系统` |
| `100亿美元` | `100 亿美元` |
| `今年Q3财报` | `今年 Q3 财报` |

规则：CJK 字符 + 拉丁字母/数字 之间，加一个**半角空格**。

`md2wechat.py` 用正则 `(?<=[\u4e00-\u9fa5])(?=[a-zA-Z0-9])` 自动处理。

### 5.2 中文标点必须在加粗标记**外**

| 错误 | 正确 |
|---|---|
| `**重要观点，**这里说的是` | `**重要观点**，这里说的是` |
| `**核心结论。**` | `**核心结论**。` |
| `**注意：**接下来是细节` | `**注意**：接下来是细节` |

为什么？加粗里包标点，渲染出来的标点会带上加粗样式（在某些字体里看起来突兀），且标点和后续文字的间距会不自然。

### 5.3 引号统一

中文文章里的引号有三种习惯：

| 风格 | 示例 |
|---|---|
| 全用直角引号 | `所谓"AI"就是...` （**推荐**，公众号通用） |
| 全用方头括号 | `所谓「AI」就是...`（台版风格） |
| 混用 | ❌ 同一篇文章里 `"X" "Y" "Z"` 不一致 |

选定一种**全文统一**。

### 5.4 破折号

中文破折号用全角 `——`（两个 U+2014），不要用：

- 英文 `--` 或 `-`
- 全角省略号 `……` 当破折号用

---

## 6. 图片处理

### 图片必须独占一行 + 居中 + 圆角

```html
<section style="text-align: center; margin: 16px 0;">
  <img src="<URL或本地路径>" style="max-width: 100%; border-radius: 4px; display: block; margin: 0 auto; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" alt="描述">
</section>
```

### 图说（caption）

紧跟图片下方，居中灰色小字：

```html
<p style="text-align: center; color: #888; font-size: 13px; margin-top: 6px; margin-bottom: 16px; font-style: italic;">
  图 1: 看板首页，左侧泳道为状态分组
</p>
```

### 图片来源

- 本地路径：必须经过 `wechat-mp-draft-skill` 上传到 mmbiz CDN，不能直接放外链
- 已上传的 mmbiz CDN URL（`https://mmbiz.qpic.cn/...`）：可直接用
- 第三方图床（imgur 等）：**会被微信压缩 + 转码**，可能丢失或变形，**强烈不推荐**

---

## 7. 表格

公众号编辑器对原生 `<table>` 支持不好，且移动端窄屏会溢出版心。按列数决策：

| 列数 | 策略 |
|---|---|
| 1–3 列 | 原生 `<table>`（见下模板） |
| 4 列及以上 / 单元格含长文 | **图片化**——走 [`SKILL.md` 的 Step 2.5](SKILL.md)，用 HTML 画好后截成 PNG 插进正文 |
| 对比矩阵 / 流程图 / 时间线 / 架构图 | **图片化**（原生 HTML 无法优雅表达，`<table>` 更不行） |

1–3 列的简单表模板：

```html
<table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px;">
  <thead>
    <tr style="background: #f6f8fa;">
      <th style="padding: 10px; text-align: left; border-bottom: 2px solid #326891; color: #326891;">列 1</th>
      <th style="padding: 10px; text-align: left; border-bottom: 2px solid #326891; color: #326891;">列 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">值 1</td>
      <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">值 2</td>
    </tr>
  </tbody>
</table>
```

> **为什么不硬做 4+ 列的花哨表格**：即使你用 `<section>` + flex 模拟，微信的 sanitizer 会抹掉一部分样式，移动端窄屏会把列挤到 30% 字号，读者完全看不清。**图片化是唯一稳定方案**。

---

## 8. 不要用的 HTML 特性

会被微信删除或不渲染，永远不要写：

- `<iframe>` —— 直接删
- `<video>` 和 `<audio>` —— 必须用公众号"插入视频/音频"功能，不能裸标签
- `<form>` `<input>` `<button>` —— 删
- `<svg>` —— 大部分情况删（少数 inline svg 会保留）
- CSS 动画 `@keyframes` —— 没用，删
- `position: fixed/absolute` —— 一般会被改成 `static`
- `transform` 复杂变换 —— 不一定支持，谨慎用
- `flex-direction: column-reverse` 等反向布局 —— 可能被改

---

## 9. 在浏览器中复制再粘贴

**最容易踩的运营坑**：写完 `article.html` 直接拖进公众号编辑器，**会以 plain text 形式插入**，所有样式丢失。

### 正确流程

1. `open ./article.html`（在浏览器中打开）
2. 浏览器里 `Cmd+A` 全选，`Cmd+C` 复制
3. 公众号编辑器里 `Cmd+V` 粘贴

浏览器复制的是**渲染后的富文本**（带 inline style），公众号能识别。

或者用 `wechat-mp-draft-skill` 的脚本流程，**自动 base64 → eval 注入**到 ProseMirror，跳过浏览器复制粘贴。

---

## 10. 自查清单

发布前过一遍：

- [ ] 所有 `style` 都内联（搜 `<style>` 应无结果）
- [ ] 所有 `<ul>`/`<ol>` 都改成 flex（搜 `<ul` `<ol` 应无结果）
- [ ] 所有外链都转成脚注（搜 `<a href` 应只剩公众号自家链接）
- [ ] 代码块都包了 `overflow-x: auto`
- [ ] 中英文/中数字间有空格（抽查 5 处）
- [ ] 加粗里没有中文标点（搜 `**[^*]*[，。！？：；]\*\*` 应无结果）
- [ ] 第一个 `<h1>` 已删除（公众号编辑器顶部有独立标题输入框）
- [ ] 图片都已上传到 mmbiz（如还是本地路径，让 `wechat-mp-draft-skill` 接力上传）
- [ ] 在浏览器中预览过实际效果
