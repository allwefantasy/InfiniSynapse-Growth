# SEMrush 100 词量化验证 SOP

> **执行人**：SEO 运营
> **耗时**：25 分钟（含等待 SEMrush 导出）
> **前置**：本目录下 `keywords-bulk-paste.txt`（100 行）+ `keywords-100-master.csv`（含元数据）
> **产物**：`output/bulk-export-YYYY-MM-DD.csv`（5,400 行候选关键词不需要，本次只跑 Bulk Analysis 拿 100 词的量化指标）

---

## A.1 Bulk Keyword Analysis · 一次性 paste 100 词（10 分钟）

### 步骤

1. 登录 [semrush.com](https://www.semrush.com/) → 左侧 `Keyword Research` → **Bulk Keyword Analysis**
2. **数据库 (Database)**：选 `United States`（与已发 6 篇英文文对齐 / 海外 SEO 主战场）
3. 右侧 `Add up to 100 keywords` → **直接 paste `keywords-bulk-paste.txt` 全部 100 行**
   - SEMrush Bulk 一次正好支持 100 词，刚好不用分批
4. 点 `Get keyword data` → 等 30-60 秒跑完
5. 拿到 100 行结果，**默认列**：

   | Keyword | Intent | Volume | KD% | CPC (USD) | Com. | Trend | SERP Features | Results |
   |---|---|---|---|---|---|---|---|---|

### 必须保留的列（用于 Phase B 决策）

```
keyword
volume
kd        (% 数字)
cpc       (美元，无符号即可)
intent    (commercial / informational / navigational / transactional / mixed)
trend     (默认是 12 个月趋势 sparkline，导出为多列；只取最近 3 个月的相对斜率)
serp_features  (逗号分隔，如 "Featured Snippet, People Also Ask, AI Overview, Video")
```

### 导出

- 右上 `Export` → `CSV`
- 命名为 `bulk-export-<YYYY-MM-DD>.csv`，落到 `SEO/100页关键词验证/output/`
- ⚠️ **导出后立刻** Numbers / Excel 打开校验：
  - [ ] 100 行（含 header 101 行）
  - [ ] 关键词 100% 与 `keywords-bulk-paste.txt` 一致（顺序可不同）
  - [ ] `volume / kd / cpc` 三列无 `N/A` 超过 10%（如有，可能是冷词，标记需 manual review）

---

## A.2 Trend 列加工（5 分钟）

SEMrush 默认 trend 是 12 个月 sparkline。**Phase B 决策只要"最近 3 个月相对斜率"**：

| trend_3m | 含义 |
|---|---|
| `up` | 最近 3 个月斜率 > +10% |
| `flat` | 斜率在 ±10% 内 |
| `down` | 最近 3 个月斜率 < -10% |

**做法**（Numbers / Excel 公式）：

1. 加一列 `trend_3m`
2. 用 SEMrush 导出的最后 3 个月数值（一般是 `Trend_M-2`, `Trend_M-1`, `Trend_M-0` 三列）计算：

   ```
   slope = (Trend_M-0 - Trend_M-2) / Trend_M-2
   trend_3m = IF(slope > 0.1, "up", IF(slope < -0.1, "down", "flat"))
   ```

3. 如果 SEMrush 导出只给了一个 sparkline 字符串而不是分月数字，**手动看眼**：上升趋势画 ↗、平 →、下降 ↘，转成 up/flat/down 即可。100 行 10 分钟肉眼可过。

---

## A.3 SERP Features 标准化（3 分钟）

只保留对 GEO 流量放大有意义的 3 个特征，转成 boolean 列：

| 新列 | SEMrush 原值包含 |
|---|---|
| `has_ai_overview` | `AI Overview` |
| `has_featured_snippet` | `Featured Snippet` |
| `has_paa` | `People Also Ask` |

其他 SERP feature（Video / Image Pack / Knowledge Panel / Sitelinks ...）这次先不进决策模型，可放 `serp_features_raw` 留底。

---

## A.4 最终导出列对齐（2 分钟）

`bulk-export-<YYYY-MM-DD>.csv` 调整为以下**严格列顺序**（Phase B prompt 直接按这个列名 SQL 引用）：

```
keyword,volume,kd,cpc,intent,trend_3m,has_ai_overview,has_featured_snippet,has_paa,serp_features_raw
```

存好后跳到 `InfiniSynapse-rerank-prompt.md` 跑 Phase B。

---

## 可选 · A.5 Magic Tool 抽 8 个 Pillar Hub 扩词（15 分钟，只做趋势校验）

> **何时做**：如果时间充裕，对 8 个 Pillar Hub 词 (`#1 #14 #24 #44 #59 #69` 已发 6 篇 + `#7 ai data analyst` + `#82 ai data analysis for product managers` 等)各做一次 Magic Tool 扩词，验证 trend 上升的子分支有哪些。
> **何时跳**：第一轮发布日历就用 Bulk 100 词的数据已经够了。Magic Tool 留到 Q4 做 Cluster 内部子词扩展时再跑。

跳过即可，本流程主线只走 A.1-A.4。

---

## SOP 完成 Checklist

- [ ] `output/bulk-export-<YYYY-MM-DD>.csv` 存在
- [ ] 文件包含 100 行（不含 header）
- [ ] 10 列严格按 §A.4 顺序
- [ ] `volume / kd / cpc / intent / trend_3m / has_ai_overview / has_featured_snippet / has_paa` 8 列无 null（缺失填 0 或 "unknown"）
- [ ] 可以进入 `InfiniSynapse-rerank-prompt.md`
