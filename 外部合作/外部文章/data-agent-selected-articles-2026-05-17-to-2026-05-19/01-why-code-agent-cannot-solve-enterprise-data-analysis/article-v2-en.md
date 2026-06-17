# Why Code Agents Cannot Solve Enterprise Data Analysis

![The Paradigm Boundary Between Code Agents and Data Agents](images/code-agent-data-agent-cover.png)
*Figure: Code Agents care whether the code runs. Data Agents care whether the answer can be trusted.*

I recently read Databricks' article on Data Agents, and it hit me quite hard.

Over the past year, many people have started using Code Agents such as Claude Code, Codex, and Cursor to analyze Excel files. You drop in a spreadsheet, ask the agent to write pandas code, run EDA, draw charts, and generate an HTML dashboard. The results can look genuinely impressive. Take one more step, and a Code Agent can even connect to multiple databases through tools, write SQL, run queries, and assemble the results into a report.

So people naturally ask:

> If Code Agents can already analyze Excel and connect to databases, why do we still need a dedicated Data Agent?

The mistake behind this question is that it treats data analysis as "writing code to process data."

But enterprise data analysis is not really about whether the code can run. It is about:

- which table should be trusted;
- which metric definition should be used;
- what a field actually means in the business context;
- whether the conclusion can be reviewed by business, data, audit, and IT teams;
- whether the agent can admit that a question is currently unanswerable when data is missing or definitions conflict.

The objective function of a Code Agent is: write code and make it run.

The objective function of a Data Agent is: produce trustworthy answers inside a messy, dynamic, semantically dense enterprise data environment.

Once these two objective functions enter a real enterprise setting, they diverge completely.

---

## The Industry Signal from Databricks Genie

On May 8, 2026, Databricks published "Pushing the Frontier for Data Agents with Genie." The article is not about an ordinary Text2SQL demo. It explains why enterprise-grade Data Agents are a separate problem.

Genie is not aimed at a single CSV file or one isolated database. It works over structured and unstructured assets across the Lakehouse:

- tables;
- dashboards;
- notebooks;
- files;
- Apps;
- Google Drive;
- SharePoint;
- business definitions;
- metadata and historical analysis assets.

One result in the article is especially important: on Databricks' internal real-world data analysis benchmark, after adding specialized knowledge search, parallel thinking, and Multi-LLM design, Genie improved from 32% accuracy with a leading coding agent to over 90%.

Of course, this is Databricks' own internal benchmark. It should not be treated as a universal industry metric. But it does show one thing:

> Enterprise data analysis cannot be solved by simply asking a model to write a few more lines of SQL. Search, semantics, reasoning, execution, verification, and cost control all have to become part of the system design.

Databricks summarizes three unique challenges for Data Agents compared with Coding Agents. I think these three challenges explain exactly why Code Agents cannot solve enterprise data analysis.

---

## Challenge One: Million-Scale Data Assets Break Traditional Search

When a Code Agent works on a codebase, it may still need to deal with many files. But the world of code has relatively stable organizing structures:

- file paths;
- function names;
- type definitions;
- import relationships;
- tests;
- Git history;
- README files and comments.

It can gradually understand an engineering system through search, navigation, dependency analysis, and test feedback.

Enterprise data is not like that.

A medium or large enterprise may have data assets such as:

- thousands or tens of thousands of business tables;
- multiple warehouses, lakehouses, and real-time databases;
- historical dashboards;
- notebooks;
- data dictionaries;
- Feishu, Notion, Google Docs, and SharePoint documents;
- temporary Excel reports;
- APIs;
- metric notes maintained by business teams;
- analysis scripts left behind years ago.

These assets are not only large in number. They are also inconsistent in structure, naming, and quality.

A user may ask:

> Why do two revenue dashboards show different peak dates?

The truly relevant information may be scattered across:

- an order fact table;
- a financial revenue recognition table;
- a dashboard filter configuration;
- a pricing document;
- transformation logic inside a notebook;
- an old Slack or Feishu discussion;
- a recently updated metric definition.

Ordinary keyword search breaks down very easily. The user may say "revenue," but the table may be called `rev_recognition_fact`, the dashboard may use `ARR`, the document may say "recognized revenue," and finance may define it as "net revenue."

If a Code Agent only searches the file system or database schema, it can easily find assets that look relevant, rather than assets that should actually be trusted.

This is the first challenge Databricks points to: the massive scale of data assets breaks conventional search methods.

The first capability of an enterprise Data Agent is not writing SQL. It is finding relevant data assets and understanding how they relate to each other.

---

## Challenge Two: Source of Truth Is Hard to Determine in a Dynamic Environment

The second challenge is even harder.

Finding assets is only the beginning. The real question is: which asset is the source of truth?

This happens all the time inside enterprises:

- two tables are both called order tables, but one is a raw business-system table and the other is a cleaned warehouse table;
- two dashboards both show revenue, but one uses order time and the other uses revenue recognition time;
- a document contains an old definition, but the business team changed the metric last month;
- a notebook contains the real transformation logic, but no one synchronized it to the data dictionary;
- a field is called `status`, but it means different things across business lines;
- an Excel file was temporarily modified by an executive and should not be used for formal analysis.

Code Agents are easy to mislead in these scenarios because they are good at "continuing to write code with the existing context." They are not designed to judge the authority of enterprise knowledge assets.

If a Code Agent sees a field called `gmv`, it is likely to use it directly. If it sees a dashboard named "Revenue Dashboard," it may assume that it contains the correct definition. If it finds a document explaining a metric, it may quote it immediately.

But in enterprise data analysis, the most dangerous failure is not a code error. It is this:

> The code runs, the number is calculated, and the metric definition is wrong.

This is the hardest kind of error to catch, because it looks like a correct answer.

A real Data Agent must be able to handle dynamic business knowledge:

- which metric definition is the latest;
- which dashboard is certified;
- which notebook contains the real transformation logic;
- which historical analyses are outdated;
- which documents are only background material;
- which pieces of knowledge should override schema;
- which conclusions can only be marked as uncertain.

So a Data Agent does not merely query data. It also judges the authority of data and knowledge.

This is why InfiniRAG is so important inside InfiniSynapse.

---

## Challenge Three: Data Agents Lack Deterministic Verification Like Code Tests

Code Agents have a major advantage: they can often rely on a test loop.

After writing code, an agent can run:

- unit tests;
- integration tests;
- lint;
- type checks;
- builds;
- e2e tests.

If tests fail, the agent fixes the code. If tests pass, the result at least satisfies some explicit specification.

Data Agents are not so lucky.

A user asks:

> Why did revenue in East China decline last quarter?

There is no unit test that tells the agent whether the answer is correct.

The question itself may hide many assumptions:

- does "last quarter" mean calendar quarter or fiscal quarter;
- is East China defined by customer location, store location, or sales organization;
- does revenue mean order amount, payment amount, recognized revenue, or net revenue after refunds;
- does decline mean year-over-year, quarter-over-quarter, or against budget;
- has the data fully landed in the warehouse;
- are exchange rates, pricing policy, refund cycles, or business changes involved.

Worse, some questions are simply unanswerable.

Maybe a key data source is missing. Maybe definitions cannot be aligned across systems. Maybe historical data broke at a certain point in time. A good Data Agent must be able to say:

> The current data is not sufficient to support this conclusion.

The default habit of a Code Agent is different. It tends to keep writing code and produce some result.

This is the third Data Agent challenge: there is no oracle like a code test.

So Data Agent reliability cannot rely only on "a smarter model." It must be compensated for by system design:

- search must find relevant assets;
- knowledge must help determine the source of truth;
- execution must leave a trace;
- intermediate results must be reviewable;
- reports must separate database facts from business interpretation;
- uncertainty must be expressed explicitly.

This is no longer the capability boundary of a Code Agent. It is a different class of system.

---

## Why These Three Challenges Break the Code Agent Paradigm

Now we can return to the opening question:

> Why can't Code Agents solve enterprise data analysis?

Because Code Agents and Data Agents operate in different worlds.

| Dimension | Code Agent | Data Agent |
|---|---|---|
| Working environment | Codebase, file system, test framework | Dynamic enterprise data environment |
| Main object | Code text and engineering dependencies | Tables, fields, metrics, documents, dashboards, historical analysis |
| Success criterion | Code runs, tests pass | Answer is trustworthy, definition is correct, process is reviewable |
| Feedback mechanism | Errors, failed tests, failed builds | Business validation, evidence chain, metric consistency, uncertainty |
| Main failure mode | Does not compile, tests fail, behavior is wrong | Wrong table, wrong metric definition, calculation is technically correct but interpretation is wrong |

Code Agents can approach a runnable state by continuously modifying code.

Data Agents cannot approach trustworthy answers merely by continuously modifying SQL or Python.

Because errors in data analysis are often not syntax errors or runtime errors. They are semantic errors.

Semantic errors do not throw exceptions.

They quietly generate a professional-looking wrong report.

---

## The Illusion of "Code Agent + Excel / Database Connection"

Why is this misunderstanding so common?

Because Code Agents really can perform some data tasks, and they can do them quite well.

Typical scenarios include:

- one-off EDA on a small CSV;
- cleaning and summarizing Excel files;
- generating temporary charts;
- generating frontend dashboards;
- writing simple SQL;
- connecting to one database and running basic queries.

These scenarios share the same traits: small data scale, single context, limited risk, and low verification cost.

They can be temporarily packaged as programming problems.

But enterprise data analysis is different.

Real enterprise analysis is usually a chain of follow-up questions:

1. First look at the overall revenue trend;
2. discover that one region declined;
3. drill down by industry;
4. identify a certain type of abnormal customer;
5. compare with the same period last year;
6. check whether pricing policies changed;
7. connect sales campaigns;
8. exclude holiday and exchange-rate effects;
9. recompute net revenue;
10. form conclusions and risk notes.

The default behavior of a Code Agent is to keep modifying code.

Step 3 adds a DataFrame. Step 5 adds a merge. Step 7 connects another database. Step 9 changes a filter. Step 10 folds previous logic into a final script.

The code gets larger. Variables multiply. Intermediate logic gets overwritten. The agent's attention starts shifting from the business problem to engineering details:

- is the package installed;
- are the API parameters correct;
- can the database driver connect;
- how should types be converted;
- will memory blow up;
- where should temporary files be stored;
- how should the charting library be made compatible.

In the end, the code may run.

But enterprises do not need "code that runs." They need trustworthy analysis.

Complex code is already anti-human. It is hard for humans to read, and hard for agents to maintain. In data analysis, once the exploration process is repeatedly edited, intermediate evidence easily disappears.

The questions enterprises care about most become hard to answer:

- Why was this table selected in the first place?
- Why was the filter changed the second time?
- At which step was the metric inconsistency discovered?
- Which intermediate result supports the final conclusion?
- If we rerun this next week, can we reproduce the same path?

So "Code Agents can analyze Excel" is true.

But "therefore Code Agents can solve enterprise data analysis" is false.

---

## InfiniSQL: Replacing Constant Code Modification with Agentic Tool Calls

InfiniSynapse's first answer to this problem is InfiniSQL.

InfiniSQL is not about inventing a fancier SQL dialect. It is about giving Data Agents a working language designed for agentic analysis.

Here is a minimal example:

```sql
select region, sum(amount) as revenue
from orders
group by region
as region_revenue;

select *
from region_revenue
where revenue < 0
as abnormal_region_revenue;
```

This code should not be understood as "a script written all at once."

It is closer to two tool calls inside an agentic workflow.

The first tool call produces `region_revenue`, abstracting raw order details into a "revenue by region" table.

The second tool call directly uses `region_revenue` to continue the analysis, finds abnormal regions, and produces `abnormal_region_revenue`.

The key point is not SQL itself. The key point is that the result of every tool call can be used by the next tool call.

As the number of tool calls grows, the InfiniSQL session gradually accumulates intermediate tables that have been explored, cleaned, aggregated, and named:

- `region_revenue`;
- `abnormal_region_revenue`;
- `east_customer_detail`;
- `refund_adjusted_revenue`;
- `campaign_revenue_bridge`;
- `final_business_readout`.

Together, these tables form a "virtual data warehouse" for the current problem.

This virtual data warehouse is not prebuilt by the data team. It is not a static schema. It grows naturally during the agent's analysis process.

The further the analysis goes, the less the agent needs to return to the raw detail tables and understand everything from scratch. It can continue analysis on top of intermediate tables that are already highly abstracted and already carry business meaning.

This is completely different from a Code Agent constantly modifying a Python script.

In Python, more follow-up questions usually mean more complex code.

In InfiniSQL, more follow-up questions mean a richer virtual data warehouse and easier downstream analysis.

That is the point of an agent-friendly language.

It allows the agent to focus on "what should I analyze next," rather than "what was my DataFrame variable called," "will this code overwrite previous results," or "is this package API version correct."

---

## InfiniSQL Also Makes Heterogeneous Joins a Native Semantics

Enterprise data never lives in one place.

An ordinary-looking question may involve:

- orders in MySQL;
- customers in PostgreSQL;
- campaign lists in Excel;
- event logs in ClickHouse;
- historical detail data in OSS or Hive;
- real-time status from APIs.

A Code Agent's natural approach is to pull these datasets locally, turn them into DataFrames, and merge them.

That works in demos. In enterprises, it quickly creates risk:

- once data volume grows, local memory cannot hold it;
- data is pulled out of the production environment, raising compliance pressure;
- computation cannot be pushed down;
- intermediate files and caches become new leakage surfaces;
- the cross-source join process becomes hard to audit.

InfiniSQL's approach is to let different data sources coexist as tables inside the same session:

```sql
connect jdbc where url="mysql://..." as mysql_biz;
connect jdbc where url="postgresql://..." as pg_ops;

load jdbc.`mysql_biz.orders` as orders;
load jdbc.`pg_ops.customers` as customers;
load excel.`/data/campaign.xlsx` as campaign;

select o.order_id, o.amount, c.level, campaign.channel
from orders o
left join customers c on o.customer_id = c.id
left join campaign on o.campaign_id = campaign.id
as order_customer_campaign;
```

The agent does not need to become a data engineer.

It does not need to handle drivers, pagination, caching, memory, temporary files, or cross-source merge logic. It only needs to express the business relationship, while the engine handles the execution details.

This matters enormously for enterprise data analysis.

Because the job of a Data Agent is not to prove that it can write complex code. Its job is to move the analysis forward reliably.

---

## InfiniRAG: Business Knowledge Is Not Context, It Is Analysis Infrastructure

The second challenge mentioned by Databricks is source of truth.

InfiniSynapse's answer to this challenge is InfiniRAG.

Many people think RAG means "retrieve a few document snippets and stuff them into the context." That is far from enough for enterprise data analysis.

Business knowledge inside an enterprise is not decorative context. It is part of the analysis itself.

The database can only tell the agent what happened.

The knowledge base tells the agent what it means.

For example, suppose the database has a field called `metric_key`. It can tell you:

- how many times `PAGEVIEW` appeared;
- how many times `DOWNLOAD` appeared;
- how many times `download:tool:windows:x64:agent_excel` appeared.

But it cannot reliably tell you:

- whether `DOWNLOAD` means download intent or confirmed installation;
- whether `agent_excel` belongs to Office automation or file processing;
- whether this metric is safe to publish externally;
- which keys should be grouped into the same demand cluster;
- what funnel definition is currently accepted by the business.

This knowledge usually lives in:

- data dictionaries;
- product documents;
- historical analyses;
- business rules;
- user preferences;
- team experience;
- even conversation history where a person repeatedly corrected the agent.

InfiniRAG is not trying to "show the model more text." It turns this knowledge into callable capability inside the agent's analysis process.

A serious Data Agent should be able to ask the knowledge base before writing SQL:

- how should this metric be defined;
- which definition is the latest;
- what business restrictions apply to this field;
- how were similar questions analyzed in the past;
- what chart and report structure does the user prefer;
- which conclusions must be marked as uncertain.

Then it should use SQL to verify computable facts.

This is the complementary binding of structured data and unstructured knowledge.

Structured data is responsible for fact computation. Unstructured knowledge is responsible for business interpretation, definition boundaries, historical experience, and preference constraints.

Separated, the agent merely knows how to query numbers.

Bound together, the agent starts to behave like an analyst.

---

## A Real Data Agent Is an Auditable Workflow

The third challenge Databricks mentions is that Data Agents lack deterministic verification like code tests.

This means Data Agents must build trust in another way: through auditable workflows.

Enterprises are not unable to accept AI.

They are unable to accept AI without an evidence chain.

A qualified enterprise Data Agent should at least leave behind:

- which data sources were used;
- which tables were queried;
- which intermediate tables were generated;
- what SQL was executed at each step;
- which conclusions came from database facts;
- which interpretations came from the knowledge base;
- which metric definitions were used;
- which assets were judged to be the source of truth;
- where data was insufficient;
- which conclusions require human confirmation;
- which charts, files, and query results support the final report.

This is the meaning of InfiniSynapse's Task View, SQL traces, named tables, charts, files, and reports.

They are not there to make the UI look busier. They are there so enterprises can review the agent.

A Code Agent often gives you a final script.

A Data Agent must give you an analysis evidence chain.

---

## The Right Relationship Between Code Agents and Data Agents

So this article is not saying that Code Agents are unimportant.

Code Agents are extremely important. They have already changed software development.

But they are good at:

- writing code;
- refactoring;
- debugging;
- generating pages;
- fixing tests;
- understanding engineering context.

Data Agents are good at:

- finding data;
- judging metric definitions;
- combining structured and unstructured knowledge;
- performing cross-source analysis;
- leaving reviewable traces;
- generating trustworthy reports;
- admitting when something cannot be answered reliably.

These two kinds of agents should cooperate, not replace each other.

InfiniSynapse also provides Command Tools so that Code Agents such as Cursor, Claude Code, Codex, and WinClaw can call Data Agent capabilities.

The wording here matters: InfiniSynapse's interface to the Code Agent ecosystem is a single binary Command Tool that you download and place in `PATH`. It is not a Python package installed with `pip install`, and it is not a persistent MCP service that users have to run themselves.

A more reasonable division of labor looks like this:

| Scenario | Better tool |
|---|---|
| Writing code, refactoring, fixing bugs, generating pages | Code Agent |
| Small CSVs, one-off EDA, temporary charts | Code Agent is enough |
| Multi-turn follow-up, business definitions, cross-source analysis, report accumulation | Data Agent |
| Enterprise databases, permissions, audit, private deployment | Data Agent |
| Joint analysis of structured data and unstructured business knowledge | Data Agent |
| Serious decision-making, regulatory reporting, financial risk control, business analysis | Data Agent |

Once general agents mature, specialized systems always emerge.

Code Agents are the specialized system for software engineering.

Data Agents are the specialized system for enterprise data analysis.

---

## Conclusion: First Find What to Trust, Then Calculate a Trustworthy Answer

The hard part for a Code Agent is:

> Changing code correctly inside a well-defined engineering system.

The hard part for a Data Agent is:

> Inside a messy, dynamic, semantically dense enterprise data system, first finding what should be trusted, then calculating a trustworthy answer.

That is why Data Agents are not a subset of Code Agents.

They are not "Code Agents that can write SQL."

They need their own infrastructure:

- InfiniAgent handles planning, small-step exploration, and self-correction;
- InfiniSQL provides an agent-friendly data analysis language, allowing tool-call results to accumulate into a virtual data warehouse;
- InfiniRAG binds business knowledge, metric definitions, personal preferences, historical analyses, and unstructured documents to data sources and execution chains.

Together, these three components are not just a "chat box that can query databases." They form a real Data Agent for enterprise data environments.

The Code Agent era has already proved one thing: when AI has the right working interface, it can transform software development.

The Data Agent era will prove the same thing:

Only when AI has a language designed for data analysis, a knowledge system that understands business semantics, and an auditable execution chain can it truly transform enterprise data analysis.

---

## References and Further Reading

- Databricks Blog, [Pushing the Frontier for Data Agents with Genie](https://www.databricks.com/blog/pushing-frontier-data-agents-genie), 2026-05-08.
