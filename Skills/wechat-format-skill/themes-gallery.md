# 主题样式速查与选型

> 提炼自 [`xiaohuailabs/xiaohu-wechat-format`](https://github.com/xiaohuailabs/xiaohu-wechat-format) 的 30 套主题。
> 本表精选 8 套**差异最大**、**适用场景最清晰**的，覆盖 95% 的内容类型。

`bin/md2wechat.py --theme <id>` 即可应用。

---

## 主题选型决策表

```
内容类型              │ 第一推荐      │ 备选 1        │ 备选 2
─────────────────────┼───────────────┼───────────────┼─────────────
深度长文/行业分析      │ newspaper     │ ink           │ magazine
科技产品/AI 工具       │ github        │ midnight      │ newspaper
访谈/对话体           │ terracotta    │ sunset-amber  │ magazine
教程/操作指南         │ github        │ newspaper     │ ink
文艺/随笔/观点         │ sunset-amber  │ terracotta    │ magazine
中国文化/古典主题      │ chinese       │ ink           │ magazine
创意/活动/反差         │ midnight      │ chinese       │ terracotta
品质长文/人物特稿      │ magazine      │ newspaper     │ ink
个人随笔/生活记录      │ sunset-amber  │ terracotta    │ ink
极简理性/哲学思辨      │ ink           │ newspaper     │ magazine
```

---

## 主题速查

### 1. `newspaper`（报纸 / 纽约时报风）

| 维度 | 设定 |
|---|---|
| 主色 | `#326891` 冷蓝灰 |
| 次色 | `#111111` 黑 |
| 背景 | `#ffffff` 纯白 |
| 引用底色 | `#f7f3ee` 米色 |
| 字体 | Georgia / 思源宋体 / 衬线优先 |
| H1 | 29px 加粗，上下双线分隔，左对齐 |
| H2 | 19px 大写字间距，居中，上下细线 |
| H3 | 17px 加粗，左对齐 |
| 正文 | 15px，1.7 行距，0.5px 字间距 |
| 加粗 | 黑色 + 蓝色高亮底（线性渐变模拟划重点） |
| 分割线 | 渐变细线，38% 宽，居中 |

**视觉印象**：克制、严肃、可信。读者第一眼想到的是《纽约时报》《财新》。

**适合**：行业分析、深度评论、观点文章、研究报告。

---

### 2. `terracotta`（赤陶 / 暖橙圆角）

| 维度 | 设定 |
|---|---|
| 主色 | `#C56C3F` 赤陶橙 |
| 次色 | `#8B5E3C` 棕 |
| 背景 | `#fffaf3` 米黄 |
| 字体 | Source Han Serif / 中文衬线 |
| H1 | 24px 白字，满底圆角橙色块 |
| H2 | 20px 加粗，左侧渐变粗装饰条 |
| H3 | 17px，主色 |
| 正文 | 15px，1.75 行距 |
| 加粗 | 主色 |
| 引用 | 浅米底 + 左侧粗橙边 |

**视觉印象**：温暖、亲和、有手作感。不像纽约时报那么严肃，但比 sunset 更有结构。

**适合**：访谈、人物故事、文艺随笔、生活方式内容。

---

### 3. `ink`（墨韵 / 极简纯黑）

| 维度 | 设定 |
|---|---|
| 主色 | `#000000` 纯黑 |
| 次色 | `#666666` 灰 |
| 背景 | `#ffffff` 纯白 |
| 字体 | 思源宋体 / Georgia / 衬线 |
| H1 | 26px 加粗，无装饰，左对齐 |
| H2 | 18px 加粗，无装饰 |
| H3 | 16px 加粗 |
| 正文 | 15px，1.8 行距，0.6px 字间距 |
| 加粗 | 纯黑（不变色，加宽） |
| 引用 | 无底色，左侧 2px 黑细线 |
| 装饰 | 无 |

**视觉印象**：极简、克制、留白多。像一张高级稿纸。

**适合**：哲学思辨、文学性强的散文、不想被视觉抢走注意力的文字。

---

### 4. `github`（GitHub / 开发者风）

| 维度 | 设定 |
|---|---|
| 主色 | `#0969da` GitHub 蓝 |
| 次色 | `#1f2328` 深灰 |
| 背景 | `#ffffff` |
| 代码块 | `#f6f8fa` 浅灰底，圆角 6px |
| 字体 | -apple-system / 系统默认 + Consolas / Menlo |
| H1 | 24px 加粗，下方 2px 浅灰边线 |
| H2 | 20px 加粗，下方 1px 浅灰边线 |
| H3 | 17px 加粗 |
| 正文 | 14px，1.6 行距 |
| 加粗 | 深灰加粗 |
| 行内代码 | 浅灰底 + 暗红字 + 等宽字体 |

**视觉印象**：清晰、技术感、阅读密度高。像 GitHub README。

**适合**：技术教程、开源项目介绍、代码讲解、架构分析。

---

### 5. `chinese`（中国风 / 朱砂红）

| 维度 | 设定 |
|---|---|
| 主色 | `#9F2A2A` 朱砂红 |
| 次色 | `#704214` 茶褐 |
| 背景 | `#fdf6e3` 宣纸黄 |
| 字体 | 思源宋体 / 楷体 / 衬线 |
| H1 | 26px 红字，左右对称装饰（如 ❖ 或印章感） |
| H2 | 20px 红字，下方红色波浪线 |
| H3 | 17px 茶褐 |
| 正文 | 15px，2.0 行距（中文阅读舒适） |
| 加粗 | 朱砂红 |
| 引用 | 米黄底 + 红色印章风左边框 |

**视觉印象**：传统、文化、典雅。

**适合**：传统文化、节气、诗词、古典美学。

> **慎用**：现代主题硬套中国风会显得怪。先确认内容真的是文化主题。

---

### 6. `midnight`（暗夜 / 赛博朋克）

| 维度 | 设定 |
|---|---|
| 主色 | `#00ffaa` 霓虹绿 |
| 次色 | `#ff3399` 霓虹粉 |
| 背景 | `#0a0a0f` 深紫黑 |
| 文字 | `#e8e8f0` 浅灰白 |
| 字体 | -apple-system + 等宽（特定标题） |
| H1 | 28px 霓虹绿，可加发光阴影 |
| H2 | 20px 霓虹粉，左侧色条 |
| H3 | 17px 灰白 |
| 正文 | 15px，1.7 行距，浅灰白 |
| 加粗 | 霓虹粉 |
| 代码块 | 更深的紫黑底 + 霓虹色高亮 |

**视觉印象**：科技、未来感、反差强烈。

**适合**：AI/前沿科技、活动预告、有"创意反差"诉求的内容。

> **注意**：深底白字在某些手机的"护眼模式"下会被强制反色，效果失控。预发前先在不同手机预览。

---

### 7. `sunset-amber`（日落 / 琥珀暖调）

| 维度 | 设定 |
|---|---|
| 主色 | `#D97706` 琥珀橙 |
| 次色 | `#92400E` 深棕 |
| 背景 | `#FFFBF5` 奶油白 |
| 字体 | Georgia / 思源宋体 |
| H1 | 24px 加粗，琥珀橙 |
| H2 | 20px 深棕，下方渐变细线 |
| H3 | 17px |
| 正文 | 15px，1.75 行距 |
| 加粗 | 琥珀橙 |
| 引用 | 奶油白底 + 左侧琥珀渐变边 |

**视觉印象**：温柔、感性、放松。比 terracotta 更柔和。

**适合**：个人随笔、情感内容、生活记录、回忆性文字。

---

### 8. `magazine`（杂志 / 超大留白）

| 维度 | 设定 |
|---|---|
| 主色 | `#1a1a1a` 接近黑 |
| 次色 | `#737373` 中灰 |
| 背景 | `#ffffff` |
| 字体 | Playfair Display / 思源宋体 / 衬线 |
| H1 | 32px 超大，0.8 行距紧凑，居中 |
| H2 | 22px 加粗 |
| H3 | 18px |
| 正文 | 16px（比其他主题稍大），1.85 行距 |
| 加粗 | 纯黑 |
| 段间距 | 24px（比其他主题大） |
| 引用 | 无底色，斜体大字号 |

**视觉印象**：奢侈、有"印刷品质感"、读者会停下来慢慢看。

**适合**：人物特稿、长文叙事、品质内容、需要读者沉浸的文章。

> **代价**：每屏内容少，文章看起来变长。短文不适合。

---

## 跨主题的通用元素样式

下面这些组件**所有主题都支持**，颜色由当前主题的 `primary` / `accent` 自动适配。

### Callout 块（4 种类型）

```html
<!-- [!important] 重要观点 -->
<section style="background: linear-gradient(to right, rgba(50,104,145,0.08), transparent); border-left: 4px solid #326891; padding: 12px 16px; margin: 20px 0; border-radius: 0 4px 4px 0;">
  <p style="font-size: 13px; font-weight: 700; color: #326891; margin: 0 0 6px 0; letter-spacing: 0.5px;">⚡ 重要</p>
  <p style="font-size: 15px; color: #333; margin: 0; line-height: 1.7;">这是核心观点的内容。</p>
</section>

<!-- [!tip] 实战技巧 -->
<section style="background: rgba(34,197,94,0.06); border-left: 4px solid #22c55e; padding: 12px 16px; margin: 20px 0; border-radius: 0 4px 4px 0;">
  <p style="font-size: 13px; font-weight: 700; color: #22c55e; margin: 0 0 6px 0;">💡 提示</p>
  <p style="font-size: 15px; color: #333; margin: 0; line-height: 1.7;">小技巧的内容。</p>
</section>

<!-- [!warning] 注意 -->
<section style="background: rgba(245,158,11,0.06); border-left: 4px solid #f59e0b; padding: 12px 16px; margin: 20px 0; border-radius: 0 4px 4px 0;">
  <p style="font-size: 13px; font-weight: 700; color: #f59e0b; margin: 0 0 6px 0;">⚠️ 注意</p>
  <p style="font-size: 15px; color: #333; margin: 0; line-height: 1.7;">注意事项内容。</p>
</section>

<!-- [!callout] 普通强调 -->
<section style="background: rgba(50,104,145,0.04); padding: 14px 18px; margin: 20px 0; border-radius: 6px;">
  <p style="font-size: 15px; color: #333; margin: 0; line-height: 1.7;">普通强调内容。</p>
</section>
```

### Dialogue 气泡（左右交替）

```html
<section style="margin: 20px 0; padding: 16px; background: #fafafa; border-radius: 8px;">
  <p style="font-size: 12px; color: #888; margin: 0 0 12px 0; font-weight: 700; letter-spacing: 0.5px;">💬 嘉宾对谈</p>

  <!-- 第 1 句：左侧 -->
  <section style="display: flex; align-items: flex-start; margin-bottom: 12px;">
    <span style="font-size: 13px; font-weight: 700; color: #326891; margin-right: 10px; flex-shrink: 0;">张三:</span>
    <section style="flex: 1; background: #ffffff; padding: 10px 14px; border-radius: 12px 12px 12px 0; font-size: 14px; line-height: 1.65; color: #333;">你怎么看这件事？</section>
  </section>

  <!-- 第 2 句：右侧（颜色翻转） -->
  <section style="display: flex; align-items: flex-start; margin-bottom: 12px; flex-direction: row-reverse;">
    <span style="font-size: 13px; font-weight: 700; color: #C56C3F; margin-left: 10px; flex-shrink: 0;">李四:</span>
    <section style="flex: 1; background: #fff3e6; padding: 10px 14px; border-radius: 12px 12px 0 12px; font-size: 14px; line-height: 1.65; color: #333;">我觉得 ……</section>
  </section>

</section>
```

### Gallery（横向滚动多图）

```html
<section style="margin: 20px 0;">
  <p style="font-size: 12px; color: #888; margin: 0 0 8px 0; font-weight: 700;">🖼️ 产品截图</p>
  <section style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px;">
    <img src="https://mmbiz.qpic.cn/.../01.png" style="flex-shrink: 0; max-width: 80%; border-radius: 6px;" />
    <img src="https://mmbiz.qpic.cn/.../02.png" style="flex-shrink: 0; max-width: 80%; border-radius: 6px;" />
    <img src="https://mmbiz.qpic.cn/.../03.png" style="flex-shrink: 0; max-width: 80%; border-radius: 6px;" />
  </section>
</section>
```

> 微信对横向滚动支持有限，移动端通常需要手指拖动；预发前要在手机上确认。

### Long Image（长图固定高度）

```html
<section style="margin: 20px 0; max-height: 600px; overflow-y: auto; border: 1px solid #e0e0e0; border-radius: 4px;">
  <img src="https://mmbiz.qpic.cn/.../longimg.png" style="width: 100%; display: block;" />
</section>
```

---

## 自定义主题

每个主题在脚本里就是一个 dict：

```python
# bin/md2wechat.py 内置（节选）
THEMES = {
  "newspaper": {
    "primary": "#326891",
    "secondary": "#111111",
    "background": "#ffffff",
    "blockquote_bg": "#f7f3ee",
    "code_bg": "#f0ede8",
    "font_serif": True,
    "h1_style": "border-top: 2px solid #111; border-bottom: 1px solid #111; ...",
    ...
  },
  ...
}
```

想加新主题：

1. 在 `THEMES` 里加一个 key
2. 复制最接近的现有主题作为基础
3. 改 5-8 个变量（主色、次色、背景、字体）即可
4. 不要从零写——成本高且出错概率大

---

## 选型反模式

1. ❌ "都行你看着选" → 没确认主题就开排
2. ❌ 长篇技术文章用 `chinese` → 朱砂红 + 文艺装饰会和代码块打架
3. ❌ 商务/财经用 `midnight` → 深底霓虹色读起来不严肃
4. ❌ 个人随笔用 `newspaper` → 太冷峻，读起来不舒服
5. ❌ 同一公众号每篇换主题 → 失去品牌一致性，先固定 1-2 个常用主题
