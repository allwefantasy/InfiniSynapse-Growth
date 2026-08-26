#!/usr/bin/env python3
"""Fix H1/title-desc keywords, duplicate sentences, and P25 practice sections."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
H1_FIXES: dict[str, str] = {
    "306-data-analysis-what-is": "Data Analysis What Is: In One Minute",
    "308-whats-a-data-analysis": "Whats a Data Analysis: A Casual Starter Guide",
    "317-python-data-analysis-guide": "Python Data Analysis: The Complete 2026 Guide",
    "320-sql-data-analysis": "SQL Data Analysis: Patterns and Queries (2026)",
    "326-data-analysis-of-qualitative-data": "Data Analysis of Qualitative Data: Step by Step (2026)",
    "343-tableau-public-data-analysis": "Tableau Public Data Analysis: A 2026 How-To",
    "344-tableau-data-analysis-tool": "Tableau Data Analysis Tool: Strengths and Limits (2026)",
    "345-data-analysis-tools-tableau": "Data Analysis Tools Tableau: Where It Fits in 2026",
    "346-excel-data-analysis-tool": "Microsoft Excel Data Analysis Tool in 2026",
    "347-microsoft-office-excel-data-analysis": "Microsoft Office Excel Data Analysis: 2026 Walkthrough",
    "360-entry-level-data-analyst-jobs": "Entry Level Data Analyst Jobs: How to Start in 2026",
    "361-remote-data-analyst-jobs": "Data Analyst Jobs Remote: The Complete 2026 Guide",
}

META_DESC_FIXES: dict[str, str] = {
    "306-data-analysis-what-is": (
        "Data analysis what is it? The fastest clear answer for 2026: a one-minute "
        "explanation, the essentials, a quick example, and how AI now performs it."
    ),
    "320-sql-data-analysis": (
        "SQL data analysis in 2026: the core query patterns that matter, from "
        "aggregation to window functions, and how AI turns plain English into SQL."
    ),
    "326-data-analysis-of-qualitative-data": (
        "Data analysis of qualitative data for 2026: transcription, coding, theme "
        "development, and interpretation, plus how AI accelerates the workflow."
    ),
    "344-tableau-data-analysis-tool": (
        "Tableau data analysis tool strengths and limits in 2026: what it does well, "
        "where it falls short, and how an AI-native agent complements it."
    ),
    "345-data-analysis-tools-tableau": (
        "Data analysis tools Tableau placement in 2026: where Tableau fits your stack, "
        "what to pair it with, and when to extend beyond visualization."
    ),
    "346-excel-data-analysis-tool": (
        "Microsoft excel data analysis tool capabilities in 2026: pivot tables, "
        "formulas, charts, real ceilings, and when to hand off to an AI-native agent."
    ),
    "360-entry-level-data-analyst-jobs": (
        "Entry level data analyst jobs in 2026: what they involve, how to qualify "
        "without experience, where to find them, and how to stand out."
    ),
}

# (old_fragment, new_fragment) — replace first match after TL;DR / FAQ only
DUP_FIXES: dict[str, list[tuple[str, str]]] = {
    "306-data-analysis-what-is": [
        (
            "You take raw numbers, clean them, look for patterns, and explain what they mean. The core idea fits",
            "Analysts start with raw figures, tidy inconsistent entries, spot patterns, and explain what those numbers imply. The core idea fits",
        ),
    ],
    "309-what-is-meant-by-data-analysis": [
        (
            "It turns sales, customer, and operational data into insights that improve choices, replacing guesswork with evidence. Its value is measured by the quality and outcomes",
            "Sales, customer, and operations records become decision-ready insights that replace guesswork with evidence. Its value is measured by the quality and outcomes",
        ),
    ],
    "314-types-of-data-analysis": [
        (
            "They form an ascending ladder of sophistication and value, with each type building on the ones before it. Most everyday work is descriptive and diagnostic.",
            "Think of them as a staircase: each step adds sophistication and depends on the steps below. Day-to-day teams spend most of their time on descriptive and diagnostic work.",
        ),
    ],
    "317-python-data-analysis-guide": [
        (
            "It offers unlimited flexibility for statistics, machine learning, and reproducible pipelines, at the cost of requiring programming skill. It has become the dominant",
            "Coding gives you open-ended room for statistics, machine learning, and reproducible pipelines, but only if you can maintain Python fluency. It has become the dominant",
        ),
    ],
    "323-qualitative-data-analysis": [
        (
            "Unlike quantitative work, it interprets what data means rather than counting it, using systematic methods like coding and thematic analysis to keep the interpretation rigorous and defensible.",
            "Where quantitative work counts occurrences, this work interprets meaning through systematic coding and thematic analysis so conclusions stay rigorous and defensible.",
        ),
    ],
    "324-qualitative-research-data-analysis": [
        (
            "It sits between data collection and reporting, uses methods like thematic analysis and coding, and must meet rigor standards so the findings are credible and defensible.",
            "This stage bridges raw collection and final reporting, applying thematic analysis and coding under explicit rigor checks so findings stay credible.",
        ),
    ],
    "386-data-analysis-certificate": [
        (
            "It signals organized learning and baseline competency but does not replace demonstrated ability through a portfolio.",
            "Employers read it as proof of structured study and baseline skills, not as a substitute for portfolio work.",
        ),
    ],
}

PRACTICE_SECTIONS: dict[str, str] = {
    "373-data-analyst-course-online": """## Putting Your Learning Into Practice

Online coursework only pays off when you treat every module like a rehearsal for a real analyst shift. Block time on your calendar the way you would for a live class, keep a running notebook of SQL snippets and chart decisions, and publish at least one finished analysis per month to a public repo or portfolio site. Remote learners who document their process outperform peers who only watch videos.

Pick one messy public dataset tied to an industry you want to work in—retail transactions, transit logs, or open government tables—and run the full loop without instructor prompts. Write your own question, profile missing values, defend one visualization choice, and record a two-minute Loom walkthrough. Hiring managers skim portfolios; a narrated project proves you can explain trade-offs, not just complete exercises.

Pair technical drills with stakeholder writing. After each analysis, draft a three-bullet executive summary that leads with the recommendation. If you cannot state the decision your chart supports, the analysis is not finished. Many online graduates fail interviews because they over-index on syntax and under-practice translation.

Finally, layer AI-native practice on top of your syllabus. Try plain-language querying on a warehouse you control, compare the agent output to your hand-written SQL, and note where you would override the model. Analysts who blend coursework with self-directed, publishable work land remote roles faster than those who stop at certificates.""",
    "375-data-analysis-courses": """## Putting Your Learning Into Practice

A catalog of data analysis courses becomes useful only when you sequence them around outcomes, not logos. Map each program to a skill gap—SQL joins, cohort retention, dashboard storytelling—and finish one course completely before starting the next. Scattershot enrollment produces half-finished notebooks that never survive a hiring screen.

Turn every capstone into a portfolio chapter. Rename files clearly, add a data dictionary, and include a short limitations section that names bias or coverage gaps. Recruiters recognize templated class projects instantly; customized framing and honest caveats signal professional judgment.

Study in public when you can. Post weekly learnings, share a chart that surprised you, or contribute to a community data challenge. Courses supply structure; community feedback supplies the friction that sharpens communication. Analysts who narrate their learning curve appear more coachable than those who present only polished finals.

Budget time for tools your target employers actually use. If job posts mention Snowflake, dbt, or an AI-native stack, replicate those environments in side projects even when the course defaults to SQLite or CSV labs. Coursework is the spine—employer-shaped practice is what makes you hirable.""",
    "376-data-analyst-certificate": """## Putting Your Learning Into Practice

Certificate programs compress fundamentals; your job is to stretch them into proof. Within two weeks of finishing, rebuild one class project on a fresh dataset with no starter code. If you cannot replicate the workflow independently, revisit the modules you rushed. Certificates open doors only when the skills feel automatic.

Add a business narrative to every certificate artifact. State the stakeholder, the decision at stake, the metric definition, and what you would monitor next week. Certificates validate exposure; decision framing validates readiness for a junior desk.

Network with intent, not volume. Message three working analysts monthly with a specific question about their stack or portfolio review offer—never a generic connection request. Many certificate holders find first roles through referrals sparked by visible, thoughtful project posts.

Keep the credential current. Analytics tooling shifts quarterly; schedule a quarterly refresh where you test a new connector, rewrite an old query with window functions, or compare an AI-generated analysis to your manual version. The certificate is a milestone, not a finish line.""",
    "377-data-analyst-courses": """## Putting Your Learning Into Practice

Multiple data analyst courses tempt you to collect completions like badges. Resist. Choose a six-week sprint on SQL and visualization, then a separate sprint on statistics or experimentation. Depth in one stack beats shallow exposure across five platforms.

Build a "course-to-career" tracker: list skills each syllabus promises, mark what you can demonstrate without notes, and flag gaps for weekend labs. Interviewers probe the gaps, not the certificates on your LinkedIn header.

Practice cross-functional communication weekly. Pair each technical exercise with a mock Slack update for a product manager who will not open your notebook. Courses rarely grade clarity; employers always do.

When courses end, simulate employment rhythms: Monday stakeholder question, midweek data pull, Friday readout. Repeating that cadence on volunteer or open data teaches prioritization better than another optional module.""",
    "378-data-analyst-courses-online": """## Putting Your Learning Into Practice

Online data analyst courses reward learners who engineer accountability. Join or create a small cohort that meets weekly to review one chart and one SQL block. Solo progress stalls when life interrupts; cohorts convert intention into shipped work.

Optimize for time zones and async review if you are studying while employed. Record short screen captures explaining bugs you fixed—those clips become interview stories that static screenshots cannot match.

Treat discussion forums as practice interviews. Answer peer questions with structured replies: context, method, caveat, next step. Teaching solidifies your own gaps and signals professionalism to mentors who lurk in those threads.

Close each course with a migration project: take the final assignment, port it to the cloud warehouse or BI tool your target company lists in job posts, and document setup steps. Online flexibility is an advantage only if outputs look production-adjacent.""",
    "379-data-analyst-training": """## Putting Your Learning Into Practice

Formal data analyst training supplies scaffolding; employability comes from deliberate reps afterward. Block recurring lab time—two evenings weekly—to re-run exercises from memory. If you need the video after week three, the skill is not yet muscle memory.

Pair training with domain immersion. Read earnings summaries, operations dashboards, or nonprofit annual reports in your target industry so you recognize real metrics when datasets arrive. Training teaches methods; domain context teaches which questions matter.

Seek feedback loops training programs skip. Ask a mentor or peer to critique whether your chart axis starts at zero, whether your cohort definition is stable, and whether your conclusion matches the evidence. Training grades completion; managers grade judgment.

Document a personal ops manual: how you profile tables, how you version queries, how you store credentials safely, how you sanity-check AI-generated SQL. Analysts who arrive with habits—not just homework—onboard faster.""",
    "380-certifications-for-data-analyst": """## Putting Your Learning Into Practice

Certifications for data analysts clarify baseline skills but rarely differentiate finalists. After earning one, publish a comparative post or repo README explaining what the exam tested versus what your last job simulation required. That meta-analysis shows evaluative thinking recruiters want.

Stack certifications only when each fills a distinct gap—cloud warehouse, statistics, visualization platform. Otherwise you accumulate logos without expanding capability. Pair every new badge with a fresh portfolio piece that uses the certified tool on unclean data.

Practice exam scenarios under time pressure, then practice stakeholder scenarios under ambiguity. Certifications validate structured tasks; workdays mix both. Run mock sessions where a teammate changes the question mid-analysis.

Maintain a living study queue: note concepts you guessed on during the exam and schedule micro-labs until guesses become derivations. Certified analysts who keep sharpening weak areas outpace peers who treat passing as permanent proof.""",
    "381-data-analysis-bootcamp": """## Putting Your Learning Into Practice

Bootcamps compress months of material into weeks; retention depends on what you build the month after graduation. Before the final week ends, line up two practice datasets and calendar daily rebuild sessions. Bootcamp velocity is useful only if skills survive without instructors.

Treat career services as a multiplier, not a magic lever. Bring polished stories: a bug you diagnosed, a metric you redefined, a chart you scrapped because it misled. Coaches can refine narratives you already own; they cannot invent experience you have not practiced.

Pair bootcamp stacks with production hygiene. Learn basic git branching, environment variables for credentials, and README templates hiring teams expect. Many bootcamp portfolios look identical; operational polish separates memorable candidates.

Negotiate your first role with portfolio evidence, not syllabus lists. Send hiring managers a one-page case study with SQL appendix. Bootcamp graduates who ship ongoing public work beat those who disappear after demo day.""",
    "382-data-analysis-course": """## Putting Your Learning Into Practice

A single data analysis course can anchor your learning plan if you treat it as the first sprint in a longer build. Revisit each assignment after two weeks and refactor for readability: clearer CTE names, commented assumptions, chart titles that state the takeaway.

Extend course datasets rather than replacing them. Add a new dimension—time zone, product line, customer segment—and measure how conclusions shift. Employers trust analysts who stress-test their own results.

Publish a "lessons learned" memo after the final module: what you would do differently with more time, which visuals failed, which definitions were unstable. That honesty demonstrates maturity more than a perfect grade.

Bridge to AI-native workflows once fundamentals feel solid. Re-ask one course question in plain language against a warehouse and compare the agent plan to your manual approach. Courses teach mechanics; hybrid practice teaches speed with guardrails.""",
    "383-data-analyst-bootcamp": """## Putting Your Learning Into Practice

Data analyst bootcamps optimize for immersion—your post-camp routine should too. Keep a standing four-hour weekly lab where you rebuild a project without slides. Immersion fades quickly without spaced repetition.

Specialize one portfolio project toward the roles you want. Fintech candidates might emphasize fraud cohorts; healthcare candidates might emphasize operational throughput. Bootcamp generics are starting points; targeted depth wins screens.

Practice live explanations. Record yourself walking through SQL for five minutes without editing. Bootcamp demos are polished; job interviews are messy. Fluency under imperfection signals senior potential early.

Stay connected to cohort peers for mock interviews and dataset swaps. The bootcamp network matters when you share job leads and review each other's take-home tests. Graduates who maintain that circle find roles faster than isolated finishers.""",
    "384-data-analyst-certification-online": """## Putting Your Learning Into Practice

Online certification paths test consistency more than brilliance. Schedule exam prep like a work shift: same time, same environment, phone off. Remote candidates who treat certification as a habit outperform cram sessions that collapse under proctoring stress.

After passing, immediately apply the certified skill to a non-practice dataset—company volunteer data, municipal open data, or a Kaggle set you have never opened. Certification proves you can follow a rubric; independent application proves transfer.

Build a verification habit for AI-assisted study. If you used tutors or copilots while learning, redo key exercises unassisted and log where you still hesitate. Hiring teams increasingly probe fundamentals beneath the badge.

Pair your online credential with visible communication practice: blog posts, LinkedIn breakdowns, or conference lightning talks summarizing one exam topic in plain language. Certifications get you considered; articulate analysts get hired.""",
    "385-data-analyst-course-free": """## Putting Your Learning Into Practice

Free data analyst courses remove price barriers, not effort barriers. Invest what you save into time: treat saved tuition as a budget for portfolio hosting, cloud credits, or a second monitor—not as permission to skim.

Because free syllabi vary wildly, maintain a personal rubric scoring each module on hands-on minutes, answer key quality, and dataset realism. Drop courses that are slide-heavy; double down on those that force SQL in graded assignments.

Compensate for missing career services by volunteering analytics for a local nonprofit or open-source maintainer. Free learning plus real stakeholders beats premium video libraries with zero accountability.

Stack free resources intentionally: one SQL track, one stats primer, one visualization deep dive. Publish a capstone that cites which free modules you combined and why. Employers respect resourceful learners who ship despite budget constraints.""",
    "386-data-analysis-certificate": """## Putting Your Learning Into Practice

Earning a data analysis certificate is a checkpoint—translate it into workplace rhythms quickly. Within thirty days, shadow a public earnings call or product update and draft the three analyses you would run if you owned that metric. Certificates validate curriculum; scenario practice validates fit.

Rebuild one certificate project with stricter data governance: document sources, retention rules, and who may access exports. Teams hire analysts who think about policy early, not only charts.

Pair your credential with measurable outcomes. If a project improved a KPI, estimate the counterfactual or at least define how you would measure impact. Hiring managers discount certificates without effect sizes or clear success criteria.

Keep an upgrade queue: after the certificate, pick one advanced topic—experimentation, semantic layers, or AI-assisted SQL—and schedule micro-projects until it appears in your portfolio. Static credentials age; documented progression does not.""",
    "387-data-analysis-certification": """## Putting Your Learning Into Practice

Data analysis certification programs signal commitment; sustained practice signals readiness. Draft a ninety-day plan that alternates between reinforcing certified topics and exploring one adjacent skill your job targets list—dbt, Python pipelines, or stakeholder workshops.

Run monthly retrospectives on your study system: which labs stuck, which definitions still feel fuzzy, where AI tools saved time versus introduced risk. Certified professionals who audit their own learning adapt faster when employers change stacks.

Offer pro bono analytics sprints to small teams with real deadlines. Certification exams are bounded; client work is not. Delivering under uncertainty teaches prioritization no classroom fully mirrors.

Publish a certification maintenance log—courses completed, labs retaken, standards refreshed—so recruiters see ongoing discipline. Certifications open conversations; proof of continuous practice closes offers.""",
}


def fix_h1_and_meta(article: Path, folder: str) -> bool:
    if folder not in H1_FIXES and folder not in META_DESC_FIXES:
        return False
    text = article.read_text(encoding="utf-8")
    orig = text
    if folder in H1_FIXES:
        text = re.sub(r"^# .+$", f"# {H1_FIXES[folder]}", text, count=1, flags=re.M)
    if folder in META_DESC_FIXES:
        text = re.sub(
            r"\*\*Meta Description\*\*:\s*.+$",
            f"**Meta Description**: {META_DESC_FIXES[folder]}",
            text,
            count=1,
            flags=re.M,
        )
    if text != orig:
        article.write_text(text, encoding="utf-8")
        return True
    return False


def fix_duplicates(article: Path, folder: str) -> bool:
    pairs = DUP_FIXES.get(folder)
    if not pairs:
        return False
    text = article.read_text(encoding="utf-8")
    orig = text
    m = re.search(r"^## Frequently Asked Questions\s*$", text, re.M)
    faq_start = m.start() if m else len(text)
    for old, new in pairs:
        idx = text.find(old, faq_start)
        if idx == -1:
            idx = text.find(old)
        if idx != -1:
            text = text[:idx] + new + text[idx + len(old) :]
    if text != orig:
        article.write_text(text, encoding="utf-8")
        return True
    return False


def fix_practice_section(article: Path, folder: str) -> bool:
    section = PRACTICE_SECTIONS.get(folder)
    if not section:
        return False
    text = article.read_text(encoding="utf-8")
    pattern = re.compile(
        r"## Putting Your Learning Into Practice\s*\n.*?(?=\n## )",
        re.S,
    )
    if not pattern.search(text):
        return False
    new_text = pattern.sub(section + "\n\n", text)
    if new_text != text:
        article.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    counts = {"h1": 0, "dup": 0, "practice": 0}
    touched: list[Path] = []

    for pillar in sorted(BLOG.glob("pillar2[1-5]-*")):
        for article in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            folder = article.parent.name
            if fix_h1_and_meta(article, folder):
                counts["h1"] += 1
                touched.append(article)
            if fix_duplicates(article, folder):
                counts["dup"] += 1
                if article not in touched:
                    touched.append(article)
            if fix_practice_section(article, folder):
                counts["practice"] += 1
                if article not in touched:
                    touched.append(article)

    print(f"H1/meta fixes: {counts['h1']}")
    print(f"Duplicate sentence fixes: {counts['dup']}")
    print(f"Practice section rewrites: {counts['practice']}")

    if touched:
        gen = Path(__file__).resolve().parent / "gen-meta-schema-p21-25.py"
        subprocess.run([sys.executable, str(gen)], check=True)
        print("Regenerated meta-tags.html + schema.json for P21-25")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
