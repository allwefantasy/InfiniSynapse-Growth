# 活动方案：InfiniSynapse × CSDN「Vibe Coding」应用开发大赛

## 一、活动概述

我们提议与 CSDN 联合发起一场 **7 月中旬上线、预计 7 月底结束**的 Vibe Coding 主题有奖开发竞赛，以「基于 InfiniSynapse API 开发并上线一款数据分析 App」为核心玩法。

激励体系分两层：**注册激励**（新用户申请 API 即送 500 积分）和**终极大奖**（仅设一二三等奖，综合用户指标、落地情况、专家意见三维度评定）。

活动全程通过**微信活动群**运营答疑，活动由 InfiniSynapse 承担奖励成本，CSDN 提供社区资源和活动页面支持，目标吸引 100+ 支参赛队伍。

---

## 二、活动目标

| 维度 | 目标 | 衡量方式 |
| --- | --- | --- |
| 参赛规模 | 收到有效应用 提交 ≥ 100 个 | CSDN 活动专区提交数 |

---

## 三、核心玩法设计

### 3.1 活动主题

**「让 Data Infra 创造无限可能」—— InfiniSynapse × CSDN 首届 Vibe coding 泛数据分析应用开发大赛**

![InfiniSynapse×CSDN-参与海报](https://cdn.gooo.ai/gen-images/3eb611375c66e43b28bc9a2e513b7ac976f72e610ea4e3cea98506479c1132ec.png)

![image.png](https://cdn.gooo.ai/web-images/12f4768ef946258b63525fef6c45cca59941ef5b47d94f6b8f0d51533f749c16)

### 3.2 参赛方式

**参赛唯一方式：基于 InfiniSynapse 底座，开发并上线一款应用。**

选手在自己的应用中集成 InfiniSynapse，通过 HTTP API 以编程方式发起分析任务、管理数据源、获取结果。

<u>应用形态不限：Web 应用、移动 App、微信小程序、桌面应用均可。不接受纯命令行脚本、Jupyter Notebook 或未部署的代码仓库。</u>

完整接口文档：[InfiniSynapse Server API Reference](https://infinisynapse.cn/en/docs/InfiniSynapse%20Server%20API%20Reference)

InfiniSynapse Skill:<https://github.com/Octo-o-o-o/InfinisynapseAssistant>

**参赛流程：**

1. 注册 InfiniSynapse 账号并申请 API Key，新用户默认赠送 **500 积分**

2. 基于 InfiniSynapse API 开发一款应用。应用须具备明确的使用场景（如：电商运营分析、金融数据看板、社交媒体舆情监控等），通过 API 调用 InfiniSynapse 完成数据的查询、分析和报告生成

3. 将应用部署上线，提供可公网访问的 URL（或可下载安装包）

4. 在 CSDN 活动专区提交作品，包含：应用介绍、技术方案、上线地址、使用截图（CSDN 可直接贴上应用链接）

### 3.3 参赛作品要求

每位选手 / 队伍在 CSDN 活动专区提交一份作品，包含：

- **应用介绍**：应用叫什么、解决什么场景问题、目标用户是谁

- **上线地址**：公网可访问的 URL 或应用商店 / 小程序入口。评委将实际访问和使用

- **技术方案说明**：如何使用 InfiniSynapse API、系统架构简述、数据源说明

- **使用截图**：展示应用核心功能和数据分析结果

- **演示视频（可选）**：从打开应用到完成一次完整数据分析的录屏

---

## 四、评审规则

**综合评定制**——奖项综合两个维度加权评分，总分 100 分。

### 4.1 评分维度

| 维度 | 权重 | 评分标准 | 数据来源 |
| --- | --- | --- | --- |
| 用户指标 | 60% | 应用上线后的注册用户数（30%）+ 活跃使用量（30%）。以活动截止日的后台数据为准 | InfiniSynapse 平台埋点数据 |
| 专家意见 | 40% | 场景价值（是否解决真实问题）、技术完成度（API 集成质量、架构合理性）、创新性（是否提供了新颖的数据应用思路） | 评审团打分 |

> **注意**：不使用 GitHub 下载量或 Star 数作为评判标准。用户指标以 InfiniSynapse 平台后台的注册和使用数据为准，确保数据真实可审计。

### 4.2 前置准入条件

参赛 应用须同时满足以下条件方可进入评分：

1. **形态**：必须是可运行的应用（Web 应用、移动 App、小程序、桌面应用均可），不接受纯脚本、命令行工具或 Jupyter Notebook

2. **已上线**：已完成部署，提供可访问的公网 URL（或可下载安装包），评委能够实际打开并使用

3. **集成 InfiniSynapse**：后端通过 Server API 调用 InfiniSynapse 完成数据分析功能，调用日志可在平台后台查验

### 4.3 评审团构成

- InfiniSynapse 产品负责人 1 人（侧重技术完成度和 API 集成质量）

- InfiniSynapse 运营负责人 1 人（侧重用户指标和场景价值）

- CSDN 社区运营 1 人（侧重社区影响力和创新性）

- 外部技术专家 1 人（侧重架构设计和技术实现）

### 4.4 评审流程

1. **准入审核**（活动截止后 3 个工作日）：InfiniSynapse 团队逐一核验提交的应用是否满足前置准入条件

2. **数据采集**（准入审核后 2 个工作日）：从平台后台导出各参赛应用的注册用户数和活跃使用量数据

3. **专家打分**（数据采集后 3 个工作日）：4 位评委独立对落地情况和专家意见维度打分

4. **加权汇总**：用户指标（客观数据）+ 落地情况 + 专家意见加权计算总分，取前 6 名

5. **公示**：获奖名单在 CSDN 活动页面和 InfiniSynapse 官方渠道同步公示 3 个工作日

---

## 五、奖励设置

奖励体系分为两层：**注册激励**（新用户申请 API 即送 500 积分）+ **终极大奖**（活动结束后综合评定）。活动期间不设每日奖金池，所有现金奖金集中在终极大奖发放。

### 5.1 注册激励：申请 API 即送 500 积分

 所有在活动期间注册 InfiniSynapse 并申请 API Key 的新用户，

> 此激励与参赛者的应用推广形成闭环：选手拉新 → 新用户获得 500 积分 → 新用户用积分兑换 token 深度体验应用内的数据分析功能 → 转化为应用的活跃用户 → 提升选手的用户指标评分。

### 5.2 终极大奖

延续 InfiniSynapse 一贯的程序员文化基因，奖金均采用 2 的幂次方金额：

<div class="tableWrapper">
<table style="min-width: 100px"><colgroup><col style="min-width: 25px"><col style="min-width: 25px"><col style="min-width: 25px"><col style="min-width: 25px"></colgroup><tbody><tr><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">奖项</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">名额</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">奖金（RMB）</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">附加权益</p></td></tr><tr><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">🥇 一等奖</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">2 人</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">4096</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">实际价值 1800 RMB 的 InfiniSynapse 年度 Pro 会员</p></td></tr><tr><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">🥈 二等奖</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">4 人</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">2048</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">实际价值 450 RMB 的 InfiniSynapse 三个月 Pro 会员</p></td></tr><tr><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">🥉 三等奖</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">6 人</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">1024</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">实际价值150RMB 的 InfiniSynapse 月度 Pro 会员</p></td></tr><tr><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">🎁 优秀奖</p></td><td colspan="1" rowspan="1"><p class="youmind-editor-node-paragraph-ui">50人</p></td><td colspan="2" rowspan="1"><p class="youmind-editor-node-paragraph-ui">实际价值 150RMB 的 InfiniSynapse 月度 Pro 会员</p></td></tr></tbody></table>
</div>

**累计费用：23w6328** 终极大奖现金部分：**22，528 RMB**，附加权益奖励共** 13800 **RMB，同时提供开发 Token 支持费用预算：**20w**

---

## 六、活动时间线

活动于 **7 月中旬正式上线，预计 7 月底结束**，整体项目周期约 4 周：

| 阶段 | 时间 | 关键动作 | 负责人 |
| --- | --- | --- | --- |
| 筹备期 | 7 月第 1 周 | 活动页面搭建、评审规则定稿、积分赠送配置 | @闫韶峰（CSDN 活动页面需对方配合） |
| 预热期 | 7 月第 2 周 | CSDN 首页 Banner 上线、社区预告帖发布、社交媒体预热 | @庞梦媛（CSDN 资源位待确认） |
| 正式期 | 7 月 15 日 — 7 月 31 日（2.5 周） | 应用开发与征集 | 双方联合 |
| —— 第 1 周 | 7/15 - 7/21 | 活动正式上线，CSDN 首页推送 + 公众号推文 + 社群推送；发布官方 demo App 和接入手册；建立微信活动群 | CSDN 运营 |
| —— 第 2 周 | 7/22 - 7/28 | 发布技术指南和最佳实践；微信活动群内组织技术答疑和进度提醒 | InfiniSynapse 团队 |
| —— 冲刺期 | 7/29 - 7/31 | 最终提交提醒；**作品提交截止（7 月 31 日 23:59）** | 双方 |
| 评审期 | 8/1 - 8/9 | 准入审核 + 数据采集 + 专家打分 + 加权汇总 | InfiniSynapse 团队 |
| 公示期 | 8 月 11 日 | 获奖名单公布 + 奖金发放 + 获奖 App 合集上线 | 双方 |

---

## 七、推广策略

### 7.1 CSDN 渠道（待确认）

> 以下为提议的资源位，具体排期和位置需与 CSDN 运营团队协商确认。

| 资源位 | 形式 |
| --- | --- |
| CSDN 首页 Banner | 活动期间持续展示 |
| CSDN 技术区推荐位 | 活动帖置顶 |
| CSDN 公众号头条 | 活动启动 + 获奖公布各一篇 |
| CSDN 社群推送 | 覆盖 Python / AI / 大数据等垂直社群 |
| CSDN 站内信 | 向数据分析、AI 编程兴趣标签用户推送 |

### 7.2 InfiniSynapse 自有渠道

| 渠道 | 形式 | 作用 |
| --- | --- | --- |
| 官方网站 | 活动专题页 + Banner | 承接流量、引导参赛 |
| 微信活动群 | 参赛者主阵地：技术答疑、进度打卡、作品互评、活动通知 | 深度运营、提高完赛率、沉淀开发者关系 |
| 小红书官方号 | 活动预热 + 作品精选 + 获奖公布 | 品牌曝光、案例传播 |
| 知乎 | 发起「Vibe Coding 数据分析」话题讨论 | 长尾搜索流量 |
| 小红书 / 公众号 | 活动通告 | 品牌声量 |

> 微信活动群是活动运营的核心载体。活动上线首日建群，所有参赛者在注册后引导入群。群内承担三大职能：
>
> **技术答疑**（API 接入问题、部署问题实时响应）、**进度运营**（每周进度打卡、中期精选作品群内首发）、**关系沉淀**（活动结束后群保留，转化为 InfiniSynapse 开发者社区种子群）。

---

## 八、预算明细（合计 227，710RMB）

| 项目 | 金额（RMB） | 说明 |
| --- | --- | --- |
| 现金大奖 | 22528 | 一二三等奖现金奖金 |
| 注册积分 | 200，000 | 新用户申请 API 即送 500 积分，不额外产生现金成本，每日最多5000RMB |
| 会员奖励 | 13800 | 2名年度 Pro 会员，4名季度 Pro 会员，56名月度 Pro 会员， |
| 合计 | 236，328 |  |

---

## 九、附件

[参赛指引：InfiniSynapse × CSDN「Vibe Coding」应用开发大赛](https://ccnej8avri03.feishu.cn/wiki/RfQPw2lgqixwRXkP0dUclEKGnnc)