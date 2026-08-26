# 正文数据图规则（Body Data Charts）

适用于 `SEO/Blog/pillar*/**/images/chart-*.png` 及正文中的 matplotlib / HTML 数据插图（**不含** hero / og-cover）。

生成脚本参考：`scripts/gen-data-charts-p26-30.py`（可按 pillar 仿写）。

---

## 硬规则 · 至少 2 个数据维度

**每张正文数据图必须编码 ≥2 个数据维度**，禁止「一个指标 + Before/After 两根柱」这类一维对比。

| 合格示例 | 维度 |
|----------|------|
| 分组柱状图：系统（CRM / Billing / Support）× 阶段（Before / After） | 类别 × 阶段 |
| 多系列折线：月份 × 今年/去年；或月份 × 有无管控 | 时间 × 系列 |
| 堆叠柱：阶段 × 时间用途（reconcile / analyze） | 阶段 × 构成 |
| 散点：X × Y（可再加 size/color） | 连续 × 连续 |
| 水平条：数据类别 × 留存天数 | 类别 × 度量（多类别才算二维对比面） |

| 不合格（禁止） | 原因 |
|----------------|------|
| 仅 `Before` / `After` 两根柱、单一指标 | 只有 1 个对比轴 |
| 仅两个状态标签的单系列条形 | 同上 |
| 单条折线、无对照系列 | 只有时间一维 |

**Before/After 叙事仍可用**，但必须拆到多个类别上做成 **grouped bars**（或等价的多系列图），不得只画两根柱。

---

## 内容与标注

1. **Illustrative**：标题或 alt 标明 illustrative / 示意，数值为教学用，不伪装成客户机密数据。
2. **Alt text**：描述图表类型 + 两个维度（例：`Grouped bar chart: variants by system (CRM/Billing/Support) before vs after MDM`），勿只写 “bar chart before after”。
3. **插入位置**：优先紧跟 `**Practical example:**` 段落后；一文通常 1 张核心数据图即可。
4. **与表格分工**：scorecard / 清单用表格；趋势、对比、构成用 `chart-*.png`。禁止把无信息量表格栅成装饰 PNG。

---

## 视觉（数据图，非 Hero）

- 白底、清晰坐标轴与图例；配色用 teal / blue / rose 等功能色，避免无意义的紫粉渐变堆砌。
- 分组柱必须有 **legend**（Before/After 或系列名）。
- 数值标签可读；勿遮挡图例。

---

## Hero 封面（相关但分层）

Hero / `og-cover.png` 规则见 [blog-hero-cover-spec.md](../../seo-content-writer/references/blog-hero-cover-spec.md) 与 [image-generation-guide.md](./image-generation-guide.md)：

- 必须叠 **精确 H1**（PIL/HTML，禁止 AI 乱字）
- 标题宜居中、科技感光晕；**禁止**黑色底板框、**禁止**黑色描边描字
- AI 背景可保留在 `images/.hero-bg/`，每次从背景重叠加标题

---

## 生成与复检

```bash
# Pillar 26–30 示例：重渲全部正文数据图（≥2 维）
python3 Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/gen-data-charts-p26-30.py

# Hero 标题叠加（居中、无黑框/黑描边）
python3 Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/overlay-hero-titles-p26-30.py
```

抽检：打开任意 `chart-*.png`，应能一眼读出 **两个轴/系列**（不只是 Before vs After 两根柱）。
