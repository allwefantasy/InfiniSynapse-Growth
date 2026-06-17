# X Thread Draft

Source article: `article-v2-en.md`

English blog link: https://zhuhailin.com/en/blog/why-code-agent-cannot-solve-enterprise-data-analysis

Cover image: `images/code-agent-data-agent-cover.png`

## Thread

### 1/13

Data Agents are not Code Agents that can write SQL.

A Code Agent tries to make code run. A Data Agent has to find evidence, decide what to trust, execute analysis, leave an audit trail, and admit when the answer cannot be supported.

Thread:

Image: `images/code-agent-data-agent-cover.png`

### 2/13

Many demos look convincing: drop in Excel, ask Claude Code, Codex, or Cursor to write pandas, draw charts, even connect to databases.

For small CSVs and one-off EDA, that is often enough.

Enterprise analysis is a different problem.

### 3/13

In enterprise data work, the hard question is rarely "can this query run?"

It is: which table is authoritative, which metric definition is current, what does this field mean, and can business, data, audit, and IT review the path to the conclusion?

### 4/13

One industry signal: Databricks says Genie moved from 32% to 90%+ accuracy on its internal real-world benchmark after adding specialized knowledge search, parallel thinking, and Multi-LLM design.

Treat the number as internal, but the direction matters.

### 5/13

Databricks names three challenges that separate Data Agents from Coding Agents:

1. million-scale data assets
2. source-of-truth decisions in a changing environment
3. no deterministic test oracle like software tests

### 6/13

Challenge 1: search breaks.

"Revenue" might be ARR in a dashboard, recognized revenue in finance docs, `rev_recognition_fact` in a warehouse, and net revenue in a spreadsheet.

Keyword search finds what looks relevant. Data Agents must find what is actually relevant.

### 7/13

Challenge 2: source of truth is dynamic.

Two dashboards can both be "revenue" while using different time logic. A doc can be outdated. A notebook may contain the real transform.

The dangerous error is not code failing. It is correct-looking numbers from the wrong definition.

### 8/13

Challenge 3: there is no unit test for "why did East China revenue decline last quarter?"

The agent must surface assumptions, verify facts, separate computation from interpretation, and say "not enough evidence" when the data cannot support an answer.

### 9/13

This is where Code Agents drift.

Follow-up questions keep mutating Python or SQL. DataFrames multiply, filters get rewritten, intermediate evidence disappears.

The script may run, but the analysis path becomes hard to review and reproduce.

### 10/13

InfiniSynapse takes a different route.

InfiniSQL turns each tool-call result into a reusable named table. Over time, the agent builds a virtual warehouse for the current investigation: explored, cleaned, aggregated, and business-meaningful.

### 11/13

InfiniRAG handles the other half: business knowledge.

Metric definitions, source-of-truth rules, user preferences, historical analyses, and documents become callable analysis infrastructure, not just text stuffed into context.

### 12/13

So the right split is not Code Agent vs Data Agent as rivals.

Code Agents are great for engineering and small analysis tasks.

Data Agents are for cross-source, multi-turn, auditable enterprise analysis where trust matters more than runnable code.

### 13/13

Full article:

Why Code Agents Cannot Solve Enterprise Data Analysis

https://zhuhailin.com/en/blog/why-code-agent-cannot-solve-enterprise-data-analysis
