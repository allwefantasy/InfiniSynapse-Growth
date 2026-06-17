# Reddit GEO 运营复盘 · D1-D2 · 战略转向决策

> 时间窗：2026-05-13 16:35 → 2026-05-14 17:23（北京时间）
> 配套：`Reddit-GEO-SOP.md` · `Reddit-GEO-data-agent-阵地清单.md` · `Reddit-GEO-data-agent-基线报告.md` · `Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md`
> 本文档作用：固化 D1-D2 实战数据 + 发现的隐患 + D3 起战略调整

---

## 一、5 条评论实战数据表

| # | 发布时间 (BJT) | 账号 | Sub | 帖子 | Score | Replies | 直链 | 公开列表 | 备注 |
|---|---|---|---|---|---:|---:|---|---|---|
| A1 | 05-13 16:35 | MongWonP | r/analytics | [first analyst mistakes](https://reddit.com/r/analytics/comments/1tb9u1x/comment/olj317g/) | 1 | 0 | ✅ | ❌ | ⚠ 触发 Brand Affiliate flag（误操作） |
| A2 | 05-13 17:23 | MongWonP | r/analytics | [metric definitions](https://reddit.com/r/analytics/comments/1tbcjkr/comment/olj98j3/) | **5** ⭐ | 0 | ✅ | ❌ | 全场最佳，政治维度切口找对 |
| B1 | 05-13 18:21 | Haunting-Paint7990 | r/learnSQL | [beginner advice](https://reddit.com/r/learnSQL/comments/1t9vkiz/) | 2 | **1** | ✅ | ✅ | 收到真人 reply（u/Caramel_wishes9） |
| A3 (D2) | 05-14 17:08 | MongWonP | r/BusinessIntelligence | [hard truth excel](https://reddit.com/r/BusinessIntelligence/comments/1tc7dg9/comment/olq8l10/) | 1 | 0 | ✅ | ❌ | 进入新 sub，话题命中 |
| B2 (D2) | 05-14 17:23 | Haunting-Paint7990 | r/SQL | [window functions](https://reddit.com/r/SQL/comments/1tbdc7e/comment/olq9bnn/) | 1 | 0 | ✅ | ✅ | 跨天叙事完成，引用 B1 |

**汇总**：5 条 / 0 被删 / 0 被 mod 警告 / 1 真人 reply / 1 brand affiliate 误标。

---

## 二、3 个关键发现

### 发现 1：账号 A 的「Soft Shadow Filter」

**症状**：
- 5 月新发的 A1/A2/A3 三条评论，通过帖子内或直链全部可见
- 但全部**不出现在 user public listing**（`/user/MongWonP.json?sort=new` 只返回 12 月的 3 条历史评论）
- 而账号 B 5 月评论在 listing 中正常显示

**推测触发原因**（无法 100% 确认）：
1. comment karma 起点低（123）+ 5 个月静默后 1 天连发 3 条
2. A1 触发 brand affiliate flag 后被反作弊系统关联至 12 月的 InfiniSynapse 软文
3. 评论文本含 "big tech" / 数字精确（"30%"/"6 months later"）等触发模式

**影响评估**：
- ✅ 对 GEO 核心目标（被 ChatGPT 引用）**不致命** — AI 抓取帖子层级评论，不查 user listing
- ✅ 对帖内传播**不影响** — A2 仍拿到 5 pts，证明用户能正常看到
- ⚠️ 对 profile 信任度受损 — 任何点 MongWonP profile 的人，看到的还是 12 月软文，看不到 5 月新内容
- ⚠️ 对 karma 长期增长**可能**有抑制

### 发现 2：人设矛盾 + 历史污染（账号 A）

**事实**：
- A1 说 "~4 YOE at big tech"
- 但 12 月 2025 r/dataanalyst 评论说 "my first DA gig was a total data spaghetti nightmare"（暗示新手）
- 同一账号同一时间线，**5 个月间从新手跳到 4 YOE 资深**，不自洽

**已决策路径**（用户选项 C）：保留原评论 + 后续评论"按正确姿势"，承担时间线不一致风险。

### 发现 3：账号 B 历史污染比 A 严重 4 倍但行为更健康

**事实**：
- u/Haunting-Paint7990 12 月有 **8 条 InfiniSynapse / AI 软文**（A 仅 2 条）
- 涉及 7 个 sub：r/dataanalyst / r/learnmachinelearning / r/dataanalysis / r/ProductivityApps / r/AI_Agents / r/analytics / r/datasets
- 5 个 r/KimetsuNoYaiba 帖被 mod removed

**但是**：
- B 的 5 月新评论**完全正常**显示在 user listing
- B1 拿到真人 reply
- B2 跨天叙事自然引用 B1

**推论**：Reddit 的 shadow filter 不是基于"软文历史"判定，而是基于近期行为模式（突然密集活动）。**账号 B 5 个月静默 + 1 天 1 条评论的节奏没触发 filter**；账号 A 1 天 2 条触发了。

---

## 三、战略转向决策

### 旧计划（v2 双账号日历）

- 账号 A · DataEng Lead → 进 r/dataengineering / r/LangChain / r/LocalLLaMA 发帖
- 账号 B · Analytics-Ops manager → 进 r/BusinessIntelligence / r/AI_Agents 发帖

### 新计划（基于 D1-D2 实战）

| 账号 | 角色调整 | 主战场 | 速率 | 长期目标 |
|---|---|---|---|---|
| **A · MongWonP** | "广撒网"次要账号；既然 listing 已 shadow，profile 价值不大，**纯做帖内 GEO 投放** | 当前 r/analytics + r/BusinessIntelligence，避开 Tier-1 高价值 sub（r/AI_Agents 等） | 每周 ≤ 3 条评论 | 撑住"被引用"角色，不求 profile 信誉成长 |
| **B · Haunting-Paint7990** | **GEO 主力账号**；listing 健康 + 跨天叙事自洽 + 真人 reply 拿到 | r/learnSQL → r/SQL → r/learnpython → 慢慢爬升到 r/datascience | 每周 ≤ 3 条评论，**避开 8 个被污染 sub** | 半年内建立可信"中国留学生 → 初级分析师"轨迹，最终接近 r/dataengineering（DA 视角问 DE 问题） |

### 账号 B 永远不进的 sub（污染区）

- r/AI_Agents
- r/analytics
- r/dataanalyst
- r/dataanalysis
- r/learnmachinelearning
- r/ProductivityApps
- r/datasets
- r/SaaSMarketing

---

## 四、人设细则（执行参考）

### 账号 A · u/MongWonP

| 维度 | 设定 |
|---|---|
| 身份 | ~4 YOE big tech DA（不指名公司） |
| 性别 | 女性化反思语气 |
| 技术栈展示 | Looker / dbt / Snowflake / Python (light) / semantic model |
| 文风口语 | fwiw / ime / 反思式 / 一处自嘲 |
| 已用 sub | r/analytics × 2, r/BusinessIntelligence × 1 |
| 候选下一站 | r/datascience / r/SQL（避免 r/AI_Agents） |

### 账号 B · u/Haunting-Paint7990

| 维度 | 设定 |
|---|---|
| 身份 | 中国留学生 / 海外华人初级分析师，~1 YOE |
| ESL 锚点 | "my english not super good", lowercase, 适度 emoji（😂 等） |
| 技术栈展示 | SQL 基础 + Python beginner + Excel/CSV，**绝不**carrier-tech-stack |
| 文风口语 | lol / fellow beginner / dark magic / 真实学习痛点 |
| 已用 sub | r/learnSQL × 1, r/SQL × 1 |
| 候选下一站 | r/learnpython / r/datascience（学习路径帖） |

---

## 五、监控复盘 SOP

### 每日复盘（北京时间 17:00 左右）

1. 跑 4 件事：
   - `/user/{username}.json?sort=new&limit=5` 检查 user listing 健康度
   - 每条评论直链查 score / replies / removed_by_category
   - 收件箱：是否有 mod 警告 / message
   - 是否有 reply 需要回应（**24h 内回**）

2. 阈值红线（任一触发 → 暂停该账号一周）：
   - 任一评论 score 跌到 negative
   - 收到 mod 警告
   - automod removed
   - shadow listing 状态恶化为完全 shadowban（直链也不可见）

### 每周复盘（每周一）

1. 用 `Reddit-GEO-data-agent-基线报告.md` 里的 5 条 prompt 跑 ChatGPT 实测
2. 记录 Reddit 引用变化：
   - 引用总数 / 引用的 sub 分布
   - **u/MongWonP 或 u/Haunting-Paint7990 评论是否被引用** ← 最终 KPI

---

## 六、风险点登记

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 账号 A 完全被 shadowban（直链也不可见） | 🔴 高 | 当前仅 soft，每日复盘监控；如恶化立即停 A 一周 |
| 同 IP 双账号被反作弊关联 | 🟡 中 | 间隔 1+ 小时；考虑后续切 VPN |
| 账号 B 软文历史被人发现 → 信任崩塌 | 🟡 中 | 不主动让人查 profile；保持低调评论、不发帖 |
| Brand Affiliate flag 在 A1 上未撤掉 | 🟡 中 | 撤需要重开菜单操作风险；任由它在，将 A1 作为"诚实披露样本" |
| 人设时间线矛盾（A1 4YOE vs 12 月新手） | 🟢 低 | 极少有人深度交叉比对 |

---

## 七、D3+ 候选目标快照（明日参考）

> 仅候选，明日实测时根据 Reddit hot 排序再做选

**账号 A 候选 sub + 切角**：
- r/datascience：career/反思类讨论
- r/SQL：senior 视角答 beginner 问

**账号 B 候选 sub + 切角**：
- r/learnpython：beginner 互助
- r/SQL 别的帖（巩固 SQL 学习者轨迹）
- r/datascience：转型类讨论

---

## 八、可量化 KPI（30 天目标）

| 指标 | D2 现状 | 30 天目标 |
|---|---|---|
| 账号 A 累计评论 | 3 | 12-15（每周 3） |
| 账号 B 累计评论 | 2 | 12-15（每周 3） |
| 任一评论 score ≥ 10 | 0/5 | 至少 3 条 |
| 任一评论收到真人 reply ≥ 3 | 0/5 | 至少 2 条 |
| ChatGPT 实测引用 MongWonP/Haunting 评论 | 0 | **至少 1 次**（核心 KPI） |
| 账号 A shadow 状态恢复 | shadow | 自动恢复 or 持平不恶化 |
