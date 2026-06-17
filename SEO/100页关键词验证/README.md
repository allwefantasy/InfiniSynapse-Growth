# 100 页主题集群关键词验证（v1.1 → 量化定稿）

> **目标**：把 `SEO/100页主题集群规划-v1.md` 里的 100 个英文主关键词跑一次量化验证，用 §11 评分模型把 P0/P1/P2 用 SEMrush 真实数据**重排**，产出"可直接排发布日历"的最终词表。
> **基线**：沿用 `日常运营/SEO选词case-AI-data-analysis/prompts/phase2-SEMrush导出SOP.md` + `phase3-CSV决策分析.md` 双 Phase 模板，把"60 种子词 + 5,400 行 Magic Tool"模式扩展到"100 词全量 Bulk 校验"。

---

## 0. 流程总览（3 步收口）

```
Step A · 关键词数据导出                    （25-60 分钟，运营手动）
   ├── A · SEMrush Business 路径 (25 min) → 走 SEMrush-验证SOP.md
   ├── B · Keywords Everywhere 路径 (30 min, 10 USD) → 走 低成本方案.md §A
   └── C · GKP 全免费路径 (60 min, 0 USD) → 走 低成本方案.md §B
              │
              ▼ 不管走哪条, 最终都得到 output/bulk-export-<日期>.csv (10 列严格对齐)
Step B · InfiniSynapse 一句话决策      （5 分钟自动，跑动 90-120 秒）
   ├── 输入: keywords-100-master.csv + bulk-export.csv（+ optional context-expansion.csv）
   ├── prompt: InfiniSynapse-rerank-prompt.md
   └── 输出: 重排后的 P0/P1/P2 + 3 张决策图表
              │
              ▼
Step C · 排进发布日历                  （10 分钟，运营 + 内容团队）
   └── 把 Step B 输出的真实 P0 24 篇 → 写进 Q3 2026 发布日历
```

---

## 1. 文件清单

| 文件 | 用途 | 谁用 |
|---|---|---|
| **`操作手册-完整版.md`** ⭐ | **zero-decision 完整操作手册**（SEMrush 路径）：每一次点击 / 每一段粘贴 / 每一个验证点都写清 | 任何执行人 |
| **`低成本方案.md`** ⭐ 新 | **没有 SEMrush Business 时走这份**：3 档替代方案（Keywords Everywhere 10 USD / GKP 全免费 / DataForSEO API）含详细步骤 + prompt 调整 | 无 SEMrush 账号时 |
| `keywords-100-master.csv` | 100 个关键词 + 我们的元数据（pillar / slug / planned_priority / content_type / 等）—— 后续 join 关键词数据 | SEO 运营 |
| `keywords-bulk-paste.txt` | 100 行纯关键词，直接复制粘贴进 SEMrush / Keywords Everywhere / GKP 任一工具 | SEO 运营 |
| `SEMrush-验证SOP.md` | 25 分钟手动 SOP 摘要版（含 filter 设定 + 列对齐） | SEO 运营（有 SEMrush）|
| `InfiniSynapse-rerank-prompt.md` | 直接复制进 `app.infinisynapse.com/tasks` 的 prompt，跑完即出最终表 + 3 张图 | 内容增长 Copilot |
| `output/`（待生成） | Step A 的关键词工具 export + Step B 的 InfiniSynapse 任务回填结果 | 自动 |

---

## 2. 时间 / 成本预算（三选一）

| 路径 | 工具 | 一次性成本 | 总耗时 | 推荐场景 |
|---|---|---|---|---|
| **SEMrush** | SEMrush Business | $0（订阅内）| 40 min | 已有 SEMrush Business 账号 |
| **Keywords Everywhere** ⭐ | KE 浏览器插件 | **10 USD**（10 万次信用，够用 2 年）| 45 min | **无 SEMrush 时的最佳选择** |
| **GKP 全免费** | Google Keyword Planner | $0 | 75 min | 不想花钱 + 不在乎数据精度降级 |

> 详细对比和决策表见 [`低成本方案.md` §0 / §D](./低成本方案.md)

---

## 3. 与 v1.1 主规划的衔接

- 本次验证**只调整 P0/P1/P2 分级**，不增删关键词（100 篇主题已定）
- 验证后产出物文件名约定：`SEO/100页关键词验证/output/keywords-100-final-priority-YYYY-MM-DD.csv`
- 用最终 CSV 反向更新 `SEO/100页主题集群规划-v1.md` 的附录 A 速查表（升级为 v1.2）

---

## 4. 下一步动作

| ☐ | 动作 | 责任 |
|---|---|---|
| ☐ | 按 `SEMrush-验证SOP.md` 跑完 Step A → 拿到 `bulk-export.csv` | SEO 运营 |
| ☐ | 把 `keywords-100-master.csv` + `bulk-export.csv` 上传到 `app.infinisynapse.com` 的 `/database/private` | 内容增长 Copilot |
| ☐ | 跑 `InfiniSynapse-rerank-prompt.md` → 拿到最终 P0/P1/P2 | 内容增长 Copilot |
| ☐ | 用结果更新 v1.1 → v1.2，并排 Q3 2026 发布日历 | 内容团队 |
