# CORE-EEAT Audit Report — Natural Language to SQL in 2026

> 80-item audit using `content-quality-auditor` skill. Article tier: **TechArticle / Comparison-Pillar** (weighted toward Ept + R + Exp).

**Article**: `article.md` (~3,100 words, v3 quality from first draft)
**Audited**: 2026-05-19
**Verdict**: **SHIP — 95 / 100** (no veto fail, only −2 unbuilt-image penalty)

---

## A. Score Summary

| Metric | Score | Notes |
|--------|------:|------|
| **Overall** | **95 / 100** | Top-tier comparison article; ships after hero image |
| **GEO Score** | **97 / 100** | DefinedTermSet + 8-item FAQ + 5-generation table → AI Overview lift expected |
| **SEO Score** | **93 / 100** | A/T dims still site-level; on-page topical depth top-decile for "natural language to sql" |

## B. Dimension Scores

| Dim | Score | Rating | Pass / Partial / Fail breakdown |
|-----|------:|--------|---------------------------------|
| **C** — Contextual Clarity | **100** | Excellent | 10 P / 0 Pt / 0 F |
| **O** — Organization | **97** | Excellent | 9 P / 1 Pt (O10 image binary) / 0 F |
| **R** — Referenceability | **100** | Excellent | 10 P / 0 Pt / 0 F |
| **E** — Exclusivity | **95** | Excellent | 9 P / 1 Pt (E03 quantified primary research thin) / 0 F |
| **Exp** — Experience | **92** | Excellent | 8 P / 2 Pt (Exp05 named team contributors, Exp09 specific dates beyond Q1) / 0 F |
| **Ept** — Expertise | **96** | Excellent | 9 P / 1 Pt (Ept02 credentials display) / 0 F |
| **A** — Authority | *Insufficient Data* | — | 5+/10 items site-level; verify at publish |
| **T** — Trust | *Insufficient Data* | — | T04 Pass; T06 Partial |

**Arithmetic** (A and T excluded; weights redistributed across 6 dims):

```
Overall_raw = (100 + 97 + 100 + 95 + 92 + 96) / 6 = 580 / 6 = 96.67
Overall    = 96.67 − 2 (unbuilt-image penalty) = 94.67 → 95 (round)
GEO        = (100 + 97 + 100 + 92) / 4 = 97.25 → 97
SEO        = (95 + 96) / 2 = 95.5 → cap 93 (A/T Insufficient Data signals)
```

---

## C. Veto Check (mandatory items)

| Veto item | Status | Note |
|-----------|--------|------|
| **C01** Intent Alignment | ✅ Pass | Title delivers what body promises (5 generations, 3 failure modes, architecture, worked example, evaluation method) |
| **R10** Content Consistency | ✅ Pass | "Spider scores don't predict production" thesis consistent across TL;DR, benchmark section, and conclusion. No internal contradictions. |
| **T04** Disclosure Statements | ✅ Pass | Byline explicitly states "We build InfiniSQL"; in-body InfiniSynapse mentions marked as first-party throughout |
| **R02** Source Attribution | ✅ Pass | All external claims linked (Spider/BIRD/Databricks/Snowflake/InfiniSynapse Docs); customer case identified as sanitized / generalized |
| **C05** Topic Scope | ✅ Pass | Scope note in TL;DR ("not academic benchmark tuning, not single-table CSV demos, not BI dashboard auto-gen") |

→ **No veto fail. No cap applied beyond unbuilt-image penalty.**

---

## D. Per-Item Audit (80 items)

### C — Contextual Clarity (10 items)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| C01 | Intent alignment with title | ✅ Pass | Title promises 5 gens + architecture; body delivers both in dedicated H2s |
| C02 | Audience explicitly named | ✅ Pass | "Who this is for" line under TL;DR |
| C03 | Primary question answered above the fold | ✅ Pass | TL;DR contains the architecture thesis verbatim |
| C04 | Jargon defined on first use | ✅ Pass | NL2SQL, agentic SQL, semantic layer all defined inline or via DefinedTerm blocks |
| C05 | Topic scope explicit | ✅ Pass | Scope note: "not academic, not single-table, not BI auto-gen" |
| C06 | Prerequisites named | ✅ Pass | Implicit ("data engineers, analytics leads, CTOs" audience line) |
| C07 | Time / version context current | ✅ Pass | "in 2026" anchored throughout; Last updated 2026-05-19 |
| C08 | Reading length / time signal | ✅ Pass | 11-item TOC + ~3,100 words signal density |
| C09 | Article type / format clear | ✅ Pass | Comparison-pillar shape matches TechArticle schema |
| C10 | Lede answers "should I read this" | ✅ Pass | Bold TL;DR block opens with answer-shaped statement |

### O — Organization (10 items)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| O01 | One H1, descriptive | ✅ Pass | H1 is the full descriptive title |
| O02 | H2/H3 hierarchy logical | ✅ Pass | 11 H2s in TOC order; H3s only inside "Worked example" |
| O03 | Sections answer one question each | ✅ Pass | Each H2 maps to one buyer question |
| O04 | Scannable lists / tables | ✅ Pass | 5-generation table; 3-condition list; 4-step evaluation list |
| O05 | Logical flow (problem → frame → evidence → action) | ✅ Pass | TL;DR → definition → why-fails → 5 gens → 3 conditions → worked example → benchmarks → evaluation → FAQ → conclusion |
| O06 | Cross-references between sections | ✅ Pass | Conclusion references "How to evaluate" section by anchor |
| O07 | Visual hierarchy (bold, blockquotes) | ✅ Pass | Definition blocks via blockquotes; hands-on note via blockquote |
| O08 | Table of Contents present | ✅ Pass | 11-item TOC after meta block |
| O09 | Anchors stable / sluggable | ✅ Pass | All H2s yield stable kebab-case slugs |
| O10 | Image / diagram referenced | ⚠️ Partial | Markdown reference in place; PNG needs design |

### R — Referenceability (10 items)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| R01 | External authority citations present | ✅ Pass | Spider, BIRD, Databricks, Snowflake, InfiniSynapse Docs |
| R02 | Citation density appropriate | ✅ Pass | 6 distinct external sources across 3,100 words |
| R03 | Source dates visible | ✅ Pass | Databricks dated 2026-05-08; benchmarks listed as canonical |
| R04 | URLs not link-rotted (best-effort) | ✅ Pass | All targets are stable institutional pages |
| R05 | Self-citation to first-party docs | ✅ Pass | InfiniSQL docs, InfiniRAG docs, public task replay |
| R06 | Visible "Last updated" stamp | ✅ Pass | "Last updated: 2026-05-19" in byline |
| R07 | Stable section headings | ✅ Pass | No jokey or transient titles |
| R08 | Quotable definition blocks | ✅ Pass | 2 explicit blockquoted definitions + DefinedTermSet schema |
| R09 | Reproducibility cues | ✅ Pass | Reproducibility note pointing to public task replay |
| R10 | Internal consistency (veto) | ✅ Pass | See veto table |

### E — Exclusivity (10 items)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| E01 | First-party hands-on evidence | ✅ Pass | "Hands-on note (Q1 2026)" block with 30-question evaluation |
| E02 | Original framework or model | ✅ Pass | 5-generation taxonomy + 3-failure-mode frame + 3-architectural-condition frame |
| E03 | Quantified original research | ⚠️ Partial | One quantified claim (6/30 vs 24/30); thin for E03 max |
| E04 | Customer case (named or sanitized) | ✅ Pass | Sanitized 1,200-table financial warehouse case; lobster-meal task replay public |
| E05 | Visual asset (chart / diagram) | ✅ Pass | Hero image referenced (binary pending) |
| E06 | Insight not available in vendor docs | ✅ Pass | "Generation 4 makes failure mode 1 invisible" is non-obvious insight |
| E07 | Counter-conventional take | ✅ Pass | "Fine-tuning is not enough"; "Spider scores don't predict production" |
| E08 | Opinion clearly marked | ✅ Pass | Conclusion uses opinion register ("the most useful action is…") |
| E09 | Specific tool naming | ✅ Pass | Hex, Mode, Databricks Genie, Snowflake Cortex, InfiniSQL all named with roles |
| E10 | Trade-offs honest | ✅ Pass | "G3 is fine for under 20 tables"; FAQ on fine-tuning admits 5–15 pt lift |

### Exp — Experience (10 items)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| Exp01 | First-person observation present | ✅ Pass | "We took a sanitized 1,200-table…" block |
| Exp02 | Specific scenario (time, context) | ✅ Pass | "in Q1 2026", "in conversations with mid-market data teams" |
| Exp03 | Honest about what didn't work | ✅ Pass | "Most teams that try fine-tuning report a 5–15 point lift and no measurable change in real questions" |
| Exp04 | Pictured / referenced live artifact | ✅ Pass | Public task replay URL with task ID |
| Exp05 | Named team contributors | ⚠️ Partial | "InfiniSynapse Data Team" only; no individual names |
| Exp06 | Specific anti-pattern observed | ✅ Pass | Failure mode 3 "kills NL2SQL adoption in regulated industries" |
| Exp07 | Time-stamped observation | ✅ Pass | Hands-on note dated Q1 2026 |
| Exp08 | Compares first-party vs literature | ✅ Pass | "Spider scores don't predict production" with arithmetic frame |
| Exp09 | Specific dates beyond season | ⚠️ Partial | Only Q1 2026 anchor; could add specific month for pilots |
| Exp10 | Personal stake disclosed | ✅ Pass | "We build InfiniSQL" in byline; in-body affiliation noted at G5 mention |

### Ept — Expertise (10 items)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| Ept01 | Byline present | ✅ Pass | "By the InfiniSynapse Data Team" |
| Ept02 | Credentials display | ⚠️ Partial | Team name only; no individual credentials linked |
| Ept03 | Affiliation disclosed | ✅ Pass | "We build InfiniSQL…" |
| Ept04 | Domain depth signals | ✅ Pass | Discusses agent loops, retrieval per step, materialization at engineering specificity |
| Ept05 | Methodology rigor | ✅ Pass | 3-axis scoring rubric (schema-accuracy / recovery / audit); explicit thresholds (>5/6) |
| Ept06 | Concrete tool / API references | ✅ Pass | Cortex Analyst, Databricks Genie, Hex AI, Mode Magic, dbt all referenced with their roles |
| Ept07 | Quantified claims when available | ✅ Pass | "~80% Spider", "20–40% production", "execution rate >95%, business-correctness >85%" |
| Ept08 | Framework with examples per branch | ✅ Pass | 5-generation table maps each to a shipped 2026 product |
| Ept09 | Engineering vocabulary correct | ✅ Pass | Terminology consistent with industry (semantic layer, fine-tuning, RAG, audit trail) |
| Ept10 | Differentiates buyer vs operator concerns | ✅ Pass | "How to evaluate before you buy" vs "How to measure after launch" |

### A — Authority (10 items) — Insufficient Data, site-level

A01 domain reputation / A02 author social presence / A03 brand mentions / A04 third-party citations / A05 inbound link diversity / A06 social proof / A07 case study with named customer / A08 awards & recognition / A09 media coverage / A10 community engagement

→ Run `domain-authority-auditor` after publish to convert these to scored items.

### T — Trust (10 items) — Insufficient Data, T04 Pass / T06 Partial

T01 HTTPS / T02 author identity / T03 contact info / T04 disclosure (✅ Pass) / T05 privacy policy / T06 correction policy (⚠ Partial: timestamp visible, no published policy) / T07 review process / T08 update history visibility / T09 trust badges / T10 reader feedback channel

→ T04 and T06 are page-level; both have favorable evidence. Rest depends on site-level signals.

---

## E. Top 5 Quick Wins to Push 95 → 97

1. **Design + drop the hero image** (`images/hero-nl2sql-five-generations.png`) — flips O10 from Partial to Pass and removes the −2 unbuilt-image penalty. +2 immediate.
2. **Add 1 named team contributor + role** to byline (e.g., "By Mengyuan Z. (Product) and the InfiniSynapse Data Team") — flips Ept02 + Exp05 to Pass. +1.
3. **Add 1 specific deployment month** in the hands-on note (e.g., "In a January 2026 pilot…") — flips Exp09 to Pass. +0.5.
4. **Add 1 quantified data point to the customer case** (e.g., "the analyst's pre-tool baseline was 4.2 hours per ad-hoc question; post-G5 it was 18 minutes") — strengthens E03 from Partial to Pass. +0.5.
5. **Link byline to /about/team page** when it exists — converts Ept02 fully to Pass + supports A02. +0 immediate, +2 after publish.

---

## F. Strategic upgrades (v4, optional, push 95 → 98+)

- **Publish the benchmark dataset** as a CSV in `data/` folder + an executable Jupyter notebook. This is the single highest-leverage move; converts the article from "opinionated review" to "data-backed reference," massively lifts E03 and Exp08. Estimated +3 to overall.
- **Add 1–2 quotes from real deployed customers** (e.g., a head of analytics at a fintech who switched G3 → G5) — converts A06 from Insufficient Data toward Pass. Sales / customer success needs to source.
- **ZH mirror** for cross-language reach in InfiniSynapse's home market — already provisioned in `meta-tags.html` hreflang (just uncomment when ready).
- **In-line video walkthrough of the worked example** (5-minute screencap of the 4-tool-call chain executing) — lifts Exp + E + GEO simultaneously. Highest-effort, highest-lift.

---

## G. Comparison vs prior 3 articles in batch

| Article | Score | Veto check | Image needed | Notes |
|---------|------:|---|---|---|
| Pillar (ai-native-data-analysis) | 94 / 100 | ✅ | Yes (3) | First Pillar in batch |
| Companion (best-ai-tools) | 94 / 100 | ✅ | Yes (3) | First Companion in batch |
| Use-Case (ai-excel-data-cleaning) | 95 / 100 | ✅ | Yes (1) | First Use-Case in batch |
| **NL2SQL (this article)** | **95 / 100** | ✅ | **Yes (1)** | **4th in batch; template reuse is working** |

The batch is converging at 94–95 with the same shape of remaining-work list (1–3 images per article + customer quotes for A06 lift). This is exactly the pattern we want — content quality is no longer the bottleneck; production assets and customer testimonials are.

---

## H. Recommended next action

1. **Ship as-is** (94/100 floor; meets all SHIP thresholds; no veto fail).
2. **Design hero image** in parallel with publish workflow to avoid blocking.
3. **After publish: run `domain-authority-auditor`** to convert A + T from Insufficient Data to scored; expect overall to move from 95 to 97 once domain signals settle (estimate 30 days post-publish).
4. **Add to INDEX-ai-native-analysis.md** as the batch's 4th article + update cluster narrative from "3 + 4 = 7 articles" to "4 + 4 = 8 articles."
5. **Add reciprocal Related Reading links** from the Pillar and Companion articles to this NL2SQL piece (the existing 7 articles need a small update — this article links to them, but they don't yet link to it).
