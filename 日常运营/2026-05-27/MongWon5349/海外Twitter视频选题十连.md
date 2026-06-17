# 海外 X (Twitter) 视频选题十连 · InfiniSynapse

> **产出日期**：2026-05-27 · **作者**：MongWon5349
> **目标平台**：X (Twitter) 海外账号
> **对标对象**：[@cursor_ai](https://x.com/cursor_ai) · [@ExaAILabs](https://x.com/ExaAILabs) · [@AnthropicAI](https://x.com/AnthropicAI)
> **拍摄能力假设**：⭐ 仅支持简单屏幕录制 + 后期加几行字幕 + BGM。**没有**剪辑师做画中画/二分屏/关键帧动画/真人出镜。
> **用途**：海外内容矩阵冷启动 / 视频同学拍摄选题池

---

## 〇、极简拍摄约束（先读这里 ⭐）

考虑到拍摄/剪辑资源有限，所有选题已按**「一镜到底屏幕录制 + 静态字幕叠加」**的能力上限重写。

### 后期只允许做这 5 件事

| 能做 ✅ | 不能做 ❌ |
|---|---|
| 黑屏标题卡（开头 1.5s + 结尾 1.5s） | 二分屏 / 左右对比 |
| 静态文字 caption 叠在屏幕底/顶（不动） | 画中画 / 多源拼接 |
| 简单 cut（前后裁掉无用片段） | 关键帧 / 缩放 / 平移动画 |
| 选 1 段轻 BGM（Lofi / ambient） | 倍速突变 / 慢动作 |
| 加一个 logo 水印（右下角小） | 真人出镜 / 配音口播 |

**核心方法**：把"剪辑该做的工作"转嫁到**录屏过程本身**做对。具体走 `Skills/infinisynapse-app-skill/SKILL.md` 里的 agent-browser 自动化脚本，让一镜到底自然成型。

### 录屏标准设置

| 项 | 值 |
|---|---|
| 工具 | agent-browser daemon（按 SKILL.md §0-§7） |
| 视口 | 1440×900（横版 16:10 录屏，最终竖版用居中裁切） |
| 终版尺寸 | 1080×1920（X 竖版优先） |
| 单条时长 | 22–45s（X 自动循环播放，30s 是甜区） |
| 字体 | Inter 或 JetBrains Mono，白字配半透明黑底条 |
| BGM 音量 | -18 dB，全程同一段，不切歌 |

---

## 一、对标方法论速查

| 账号 | 借鉴点（只借**我们能拍**的部分） |
|---|---|
| **@cursor_ai** | 黑底等宽字 caption / 一镜到底录屏 / 0-3s 出 wow |
| **@ExaAILabs** | 一段稳定 voiceover 改成 = 一行稳定的屏幕字幕；"喝杯咖啡就跑完"的体感节奏 |
| **@AnthropicAI** | 慢节奏揭示 reasoning —— 我们直接录 `.compact-tool-row` 最大化看 SQL 全过程 |

⚠️ Cursor / Exa 常用的"二分屏 old vs new"我们**不做**，改用 caption 文字立场来替代视觉对比。

---

## 二、十条主题（已按极简录屏重写）

### 主题 2 ·「One prompt, full report」30 秒魔法 demo ⭐⭐⭐ 首拍

> 移到 #1，因为这是录制难度最低、爆款概率最高的一条。

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐ 极易（一镜到底，0 后期动效） |
| **Hook (0-3s)** | 黑屏 1.5s → 切到 InfiniSynapse 任务页，输入框里**已经预填**一句：`why did our SEA revenue drop in Q3?` 镜头停一拍 |
| **录屏脚本** | (1) 按 Enter → Agent 自动跑 5 个 phase（**录全程，不要倍速**，X 平台播放器自带跳过）<br>(2) 自动跳出最终图表 + 三句话归因结论<br>(3) 鼠标停在 "Save to memory" 按钮上 1s<br>(4) 黑屏 1.5s 收 |
| **字幕（只 2 行）** | 0:00–0:03 顶部白字：`One prompt.`<br>结尾 2s 底部白字：`28 seconds. 4 data sources. 1 verifiable answer.` |
| **时长** | 30s |
| **配文** | `1 prompt → full report. What used to be a Monday-morning Slack thread.` |
| **CTA** | `app.infinisynapse.com` |
| **对标视频** | Cursor *Composer 2.5* 发布推 ⭐ —— [x.com/cursor_ai](https://x.com/cursor_ai) (2026-05-18 那条，`pic.twitter.com/N87ojcXlOC`)<br>同款长版：https://www.youtube.com/watch?v=43r9OZ1a8nk |
| **录屏命令** | SKILL.md §4 提交问题 + §7 任务轮询 + §5.1 看进度 |

---

### 主题 3 ·「Show the SQL it ran」可审计性视频 ⭐⭐⭐ 必拍

> 这条是 InfiniSynapse 跟所有 BI 工具最强差异。SKILL.md §5.2 已经把录屏路径写死了。

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐ 极易（agent-browser 自动点 `.compact-tool-row` + 最大化即可） |
| **Hook (0-3s)** | 黑屏 → 大白字：`"Trust me, the chart is right." — every BI tool ever` |
| **录屏脚本** | (1) 跳到一个已经跑完的任务详情页（带最终图表）<br>(2) 鼠标点对话流里某一行 `.compact-tool-row`（按 SKILL.md §5.2.3）<br>(3) 右侧弹出 SQL + 表数据 → **按 `.anticon-expand` 最大化**（这一步是高潮，停 2s）<br>(4) 鼠标点另一个步骤行 → 面板原地切换成图表查看器（按 SKILL.md §5.2.5）<br>(5) 黑屏 1.5s 收 |
| **字幕（3 行）** | 0:03 起 caption：`Every SQL step is replayable.`<br>0:15：`Every data table is auditable.`<br>结尾：`The trail is the deliverable.` |
| **时长** | 30–35s |
| **配文** | `"The answer" is not the deliverable. The trail is.` |
| **对标视频** | Cursor *demos, not diffs* ⭐ —— https://www.youtube.com/watch?v=XbZvC4KTH68 |
| **录屏命令** | SKILL.md §5.2.3 完整脚本（已包含点行 / 最大化 / 切换 / 关闭） |

---

### 主题 5 ·「Connect any DB in 30 seconds」上手即用

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐ 极易（普通新建数据源 + 提问录屏） |
| **Hook** | 黑屏 → 大字：`Snowflake. Postgres. MySQL. Hive.` 静态字（**不要动效**） |
| **录屏脚本** | (1) 进入 `/database/private` → 点 "New Data Source" → 选 Snowflake<br>(2) 粘贴连接串（**用 ⌘+V，过程录全**）→ 点 Test → Save<br>(3) 立刻 `open /tasks` → 输入 `list my top 10 customers by ACV` → 按 Enter<br>(4) 等结果出来 → 黑屏 1.5s 收 |
| **字幕** | 视频左上角始终显示固定计时器（**用 OBS 内置 timer 或 macOS 时间叠加，不要做后期动画**）：`00:00 → 00:31`<br>结尾 caption：`From "data source connected" to "first insight". Under a minute.` |
| **时长** | 35s |
| **配文** | `No semantic layer to pre-build. Just connect.` |
| **对标视频** | Exa *Voice Pipeline*（极致 latency 体感）：https://demo.exa.ai/voice/how-it-works |
| **录屏命令** | SKILL.md §2 路由 + §4 提交问题 |

---

### 主题 4 ·「Recall, don't redo」记忆库召回

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐⭐ 中等（涉及 2 个会话切换，但 SKILL.md §6 有现成脚本） |
| **Hook** | 黑屏 → `What if your data agent remembered last week's analysis?` |
| **录屏脚本** | (1) 进入一个 3 周前的旧任务（侧边栏带绿色 ✓）<br>(2) 点 `.task-item.active .task-more-btn` → 弹出菜单 → 点 "Save to memory"<br>(3) 等 "Save successful!" toast 闪过<br>(4) **直接 `open /tasks` 跳新会话**（避免来回切窗口）<br>(5) 输入 `Recall the unemployment analysis I ran in May — refresh with this week's data` → 按 Enter<br>(6) 等 Phase 1 = `RAG Research` 出现（**caption 这时叠上去**）<br>(7) 等结构化卡片回填 → 出新图 → 黑屏收 |
| **字幕** | 0:18 出现 Phase 1 时叠：`Phase 1 = RAG Research` 高亮（用半透明黑底白字框住屏幕里那行字，**不要画箭头/圈红**）<br>结尾：`Memory ≠ chat history. It's structured context the agent can re-execute.` |
| **时长** | 50–60s |
| **配文** | `Stop re-explaining your tables every week.` |
| **对标视频** | Cursor *Memories* feature 综述：https://www.youtube.com/watch?v=4Vqk-qSo36U（`02:31` 起） |
| **录屏命令** | SKILL.md §6 完整脚本（Save to memory + 召回 prompt 模板） |

---

### 主题 6 ·「Cross-source join, one sentence」高阶能力

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐⭐ 中等（需要预先配置好 3 个数据源） |
| **拍摄前置** | 提前在账号里挂好 Stripe (Postgres) + Salesforce (Snowflake) + 上传一份 customer_tier.csv |
| **Hook** | 黑屏 → `Stop writing pipelines. Just ask.` |
| **录屏脚本** | (1) 任务页输入：`Join our Stripe revenue with Salesforce deals and segment by the customer tier sheet I uploaded`<br>(2) 按 Enter → 录全程跑（不超过 90s，剪掉中间冗余）<br>(3) 跑完后**点其中一个 `.compact-tool-row`** → 看到 InfiniSQL 自动命名的中间表（如 `t_stripe_sf_joined`）<br>(4) 最大化展示这张虚拟表 → 黑屏收 |
| **字幕** | 0:25 中间表出现时叠：`Auto-named virtual table. Reusable tomorrow.`<br>结尾：`3 sources. 0 ETL.` |
| **时长** | 45s |
| **配文** | `Every tool call becomes a reusable named table. A virtual warehouse, built one question at a time.` |
| **对标视频** | Exa *Websets* launch ⭐：[x.com/ExaAILabs/status/1864013080944062567](https://x.com/ExaAILabs/status/1864013080944062567) |

---

### 主题 1 ·「Data Agent ≠ Code Agent」立场定义视频

> **重要改造**：原计划是二分屏对比 Claude Code，我们**做不到**。改成纯文字立场 + InfiniSynapse 单边录屏。

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐ 极易（纯文字开场 + 一段录屏） |
| **Hook (0-5s)** | 黑屏 5s 大字（**3 张静态字卡，每张 1.5s**，不要做转场动画）：<br>① `A code agent makes code run.`<br>② `A data agent makes answers trustworthy.`<br>③ `Same prompt. Two definitions of "done".` |
| **录屏脚本** | (1) 切到 InfiniSynapse → 输入一个企业级模糊问题，如 `which of our 4 "revenue" tables should I use to report Q3 ARR?`<br>(2) 等 Agent 先调 RAG 查口径定义、再选表、再算<br>(3) 重点录两步：**RAG Research phase** 和 **最终带证据链的回答**<br>(4) 黑屏 1.5s 收 |
| **字幕** | 录屏中段一行：`Asks the knowledge layer first. Computes second.` |
| **时长** | 40s |
| **配文** | `Code agents ≠ data agents. The trustworthiness comes from the harness, not the model.` |
| **对标视频** | Anthropic *Code with Claude Keynote*（26:28 起 positioning 段）：https://www.youtube.com/watch?v=EvtPBaaykdo |

---

### 主题 7 ·「The question your dashboard can't answer」叙事视频

> **重要改造**：原计划要"模拟点击普通 BI 仪表盘 → 死链"。**做不到**。改成纯 InfiniSynapse 录屏 + 一句立场字幕。

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐ 极易（一镜到底） |
| **Hook (0-4s)** | 黑屏 → 大字：`"Why did East China revenue decline last quarter?"`<br>下一帧小字：`A dashboard can't answer this.` |
| **录屏脚本** | (1) 切到 InfiniSynapse → 输入这个问题 → 按 Enter<br>(2) 录全程 5 个 phase 跑：检索旧分析 → 验证表 → 跑分组对比 → 归因分解 → 输出 |
| **字幕（关键）** | 在 Phase 之间叠 3 行（每行停 3s）：<br>① `Surfaces assumptions before computing.`<br>② `Says "not enough evidence" when warranted.`<br>③ `Separates computation from interpretation.` |
| **时长** | 55s |
| **配文** | `The most dangerous BI answer is a confident wrong one. Agents that say "not enough evidence" are agents you can trust.` |
| **对标视频** | Anthropic *Computer Use · Orchestrating Tasks* ⭐：[x.com/AnthropicAI/status/1848742761278611504](https://x.com/AnthropicAI/status/1848742761278611504) |

---

### 主题 10 ·「Drop a messy CSV → board-ready chart in 30s」（**新**）

> 替换原 "CFO 11pm"。原方案需要伪造邮件截图 + 复杂下载演示，新方案是**最简单的一镜到底**——拖一个文件、问一句话，结束。

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐ 极易（拖拽 + 1 prompt + 等图表，全程一镜到底） |
| **拍摄前置** | 准备一个故意"脏"的 CSV：列名不规范（`Q1_revenue`、`q1 revenue (USD)`、`revenue_q1`）、日期格式混杂、有缺失值。文件名建议 `quarterly-sales-raw.csv` |
| **Hook (0-5s)** | 黑屏 5s 大字（2 张静态字卡）：<br>① `Your CSV has 4 different date formats.`<br>② `Your boss wants a chart by EOD.` |
| **录屏脚本** | (1) 切到 InfiniSynapse 任务页 → 把准备好的 CSV 直接拖进输入框区域<br>(2) 输入 prompt：`clean this file, surface the 3 metrics that matter, and chart Q-over-Q trend`<br>(3) 按 Enter → 录全程跑（**不要倍速**）<br>(4) 等出最终图表（柱状或折线）→ 鼠标停在图表上 1s<br>(5) 黑屏 1.5s 收 |
| **字幕** | 录屏中段叠：`No formulas. No VLOOKUP. No Python.`<br>结尾：`A clean chart. Auditable. Reusable.` |
| **时长** | 30–40s |
| **配文** | `Your messiest CSV, your cleanest chart. The agent does the cleaning, the picking, and the explaining — in one shot.` |
| **CTA** | `Drop your file at app.infinisynapse.com` |
| **对标视频** | Cursor *demos, not diffs*（同样"拖一个东西进去，看 agent 干完"叙事）：https://www.youtube.com/watch?v=XbZvC4KTH68 |
| **录屏命令** | SKILL.md §4 提问 + §7 任务轮询（拖拽文件走的是 InfiniSynapse 输入框上方的 `picture` 按钮 / 直接 drag-drop，详见 §4.0 任务详情页 vs 首页输入框） |
| **为什么这条值得拍** | "Excel/CSV 救我" 是 X 上 evergreen 话题，几乎任何角色都能共情；拖拽动作有强烈视觉锚点；规避了"企业级数据源"的高门槛认知 |

---

### 主题 8 ·「Subscribe to a curated dataset → analyze in one breath」（**新**）

> 替换原 "Benchmark drop" 数字 thread。新方案是**仅 InfiniSynapse 独有**的差异化能力 —— Cursor / Exa / Claude 都没有的"数据集市场"。

| 项 | 内容 |
|---|---|
| **录制难度** | ⭐⭐ 中等（涉及订阅流程的 antd 弹窗按钮陷阱，按 SKILL.md §3.3 + §8.3 走必稳） |
| **拍摄前置** | 确认目标数据集是"未订阅"状态，否则录不到"+订阅"那段（必跑 SKILL.md §8.3 的 hygiene 检查脚本） |
| **Hook (0-5s)** | 黑屏 5s 大字（2 张静态字卡）：<br>① `A code agent without code.`<br>② `A data agent without your data.` |
| **录屏脚本** | (1) 进入 Data Marketplace（数据市场）→ 上下滚一下数据集卡片（**控制速度，不要快滑**）<br>(2) 停在一张目标卡片（推荐选"global unemployment" / "AI industry salary" / "consumer sentiment" 这类有公共吸引力的）<br>(3) 点 `+ 订阅` → antd 弹窗 → 用 SKILL.md §3.3 的 JS 选择器点 `确认`<br>(4) 卡片状态变成"已启用 + 查看"<br>(5) 直接 `open /tasks` → 输入 `using the dataset I just subscribed, show me the top 3 patterns I should care about`<br>(6) 录全程跑 → 出图收 |
| **字幕** | 0:15 订阅成功时叠：`Subscribed. Live in your agent's reach.`<br>结尾：`No ETL. No cleanup. Just subscribe, then ask.` |
| **时长** | 45–55s |
| **配文** | `The data agent comes with a marketplace. Subscribe to a curated dataset, then ask in plain English. Closest analog: npm install, but for analysis-ready data.` |
| **对标视频** | Exa *Introducing Websets* ⭐ —— [x.com/ExaAILabs/status/1864013080944062567](https://x.com/ExaAILabs/status/1864013080944062567)<br>同款长版：https://www.youtube.com/watch?v=6BctPbNSjqg |
| **录屏命令** | SKILL.md §8.3 完整订阅生命周期 + §3.3 antd 弹窗按钮空格陷阱（`确 认` 带空格必须用 JS） |
| **为什么这条值得拍** | 数据市场是 InfiniSynapse vs Cursor / Exa / Claude 最大的产品级差异；"npm install for data" 这个类比对 X 开发者人群特别 sticky |

---

### 主题 9 ·「Source of truth」深度技术 —— **改为视频 + thread 联动** ❌

> 视频部分降级：原计划"列出 4 个候选 + 业务知识卡 + agent 路径"，需要做信息图。**改成**：

| 项 | 内容 |
|---|---|
| **形式** | thread 头条 1 条短视频（20s）+ 后续 7 条纯文字 thread |
| **短视频内容（极简）** | 黑屏静态字卡 3 张：<br>① `"Revenue" exists 4 times in your warehouse.`<br>② `arr_dashboard / recognized_revenue / rev_recognition_fact / net_revenue`<br>③ `Which one is right? 🧵 (1/8)`<br>**全程黑底白字静态**，无任何录屏 |
| **后续 thread** | 配 InfiniRAG 实际界面截图 7 张（一张一条 tweet） |
| **为什么这样简化** | 不需要任何动效，1 个 Keynote/PPT 导出 3 张字卡拼成 mp4 即可 |

---

## 三、按"录制难度从低到高"排序的拍摄计划

| 序 | 主题 | 难度 | 一句话 |
|---|---|---|---|
| 1 | **主题 2**（30s magic demo） | ⭐ | 直接录一次 prompt → output，最容易先试水 |
| 2 | **主题 3**（Show the SQL） | ⭐ | SKILL.md §5.2 有现成 agent-browser 脚本 |
| 3 | **主题 10**（Drop a messy CSV）⭐新 | ⭐ | 拖文件 + 1 prompt，最强 X 通用共情 |
| 4 | **主题 1**（Data ≠ Code Agent） | ⭐ | 3 张静态字卡 + 1 段录屏 |
| 5 | **主题 7**（Dashboard can't answer） | ⭐ | 同样一镜到底 + 字幕立场 |
| 6 | **主题 5**（Connect any DB） | ⭐ | 全程 1 个操作流，加 OBS 计时器 |
| 7 | **主题 4**（Recall）| ⭐⭐ | 需要预先存好一份记忆 + 新会话切换 |
| 8 | **主题 8**（Subscribe a dataset）⭐新 | ⭐⭐ | InfiniSynapse 独有差异化，按 §8.3 走稳 |
| 9 | **主题 6**（Cross-source join） | ⭐⭐ | 需要预配 3 个数据源 |
| 10 | **主题 9**（Source of truth） | thread | 1 个 20s 静态字卡视频 + 7 张截图 thread |

**建议节奏**：每周 1–2 条。先把 ⭐ 类全部拍完（5 条），验证 X 受众反馈再投入 ⭐⭐ 类。

---

## 四、字幕样式统一规范（**减少剪辑决策**）

只有 2 种字幕样式，全文件统一用：

| 类型 | 用法 | 样式 |
|---|---|---|
| **A. 标题字卡** | 黑屏静态 1.5s | 白字居中 / Inter Bold 96px / 行距 1.2 |
| **B. 录屏叠加字** | 录屏过程中底部叠 | 白字 / 半透明黑底条 / Inter 56px / 始终居底部 1/4 处 |

**严禁**：渐入渐出动画、缩放、颜色变化、emoji、表情符号、箭头标注、圈红、马赛克。

---

## 五、对应的 agent-browser 录屏脚本（按主题给到视频同学）

每个 ⭐ 难度的主题都对应 SKILL.md 里现成的章节，视频同学按章节直接复制粘贴即可：

| 主题 | 必读 SKILL.md 章节 |
|---|---|
| 2, 5 | §0 域名 / §1 登录预检 / §4 提问 + Enter / §7 轮询 |
| 3 | §5.2 完整脚本（含 textContent 匹配、最大化、切换、关闭） |
| 4 | §6 Save to memory + 召回 prompt 模板 |
| 6 | §4 提问 + §5.2 看中间表 |
| 1, 7 | §4 提问 + §7 等 phase 跑动 |
| 8（订阅数据集）| §8.3 订阅生命周期 + §3.3 antd 弹窗按钮空格陷阱（必读）|
| 10（拖 CSV）| §4.0 任务详情页 vs 首页输入框（拖拽走首页 textarea） + §7 轮询 |

⚠️ **录制前必跑一次** SKILL.md §1 的登录预检 + §3.3 antd 弹窗按钮空格陷阱，否则中途 UI 报错重录浪费时间。

---

## 六、对标账号 X 主页（每周扫一次）

| 账号 | X 主页 | 借鉴重点（**只看我们能做的**） |
|---|---|---|
| **Cursor** | [x.com/cursor_ai](https://x.com/cursor_ai) | 黑底字卡节奏 + caption 文案 |
| **Exa** | [x.com/ExaAILabs](https://x.com/ExaAILabs) | 一句话定义产品类别 + 配文写法 |
| **Anthropic** | [x.com/AnthropicAI](https://x.com/AnthropicAI) | 第一视角一镜到底录屏 + 慢节奏 caption |

---

## 七、下一步

1. **视频同学**：从主题 2 开拍（最简单），跑通拍摄+剪辑+发布完整链路
2. **运营同学**：
   - 准备主题 10 的"故意脏 CSV"样本（4 种日期格式 + 重复列名 + 缺失值）
   - 准备主题 6 的 3 个数据源连接（Stripe Postgres / Salesforce Snowflake / customer_tier.csv）
   - 准备主题 8 的目标数据集"未订阅" hygiene check（按 SKILL.md §8.3 末段）
3. **本文档维护**：每拍完一条，回来更新"实际拍摄时长 / 实际录制难度 / 数据反馈"

> 如需主题 2 的逐帧拍摄脚本（含 agent-browser 命令、caption 出现时间码、剪辑节奏点），单独开一份 `视频脚本-主题02-30s-magic-demo.md`。
