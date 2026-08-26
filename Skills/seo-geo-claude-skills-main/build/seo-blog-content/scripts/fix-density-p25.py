#!/usr/bin/env python3
"""Fix keyword density and word count for Pillar 25 articles."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "pillar25-data-analyst-learning-certification"

SYNONYMS = {
    "data analyst degree": ["analytics degree", "this degree path", "a degree in analytics", "the degree route", "formal degree training", "university degree path", "academic degree option", "degree-based training", "degree program", "the academic route", "degree credential", "university training path", "degree qualification", "academic qualification", "degree-based entry", "the degree option", "formal education path", "degree track", "academic pathway", "degree route"],
    "data analyst course": ["analytics course", "this training program", "the course", "a strong program", "the program", "analytics training", "this course option", "the training", "a quality program", "course selection", "training program", "analytics program", "the right program", "this option", "course option", "structured program", "training course", "learning program", "the curriculum", "course offering", "analytics class", "this offering", "training option", "the class", "program option"],
    "data analyst course online": ["online analytics course", "this online program", "the online course", "remote analytics training", "online training program", "virtual course", "online program", "remote course option", "web-based training", "online analytics program", "the remote program", "virtual training", "online learning path", "remote training", "web-based course", "this remote option", "online class", "virtual program", "remote learning program", "online offering", "web-based program", "the virtual course", "remote analytics course", "online option", "this web-based course"],
    "data analysis courses": ["analytics courses", "these programs", "training courses", "analytics programs", "the courses", "course options", "analytics training", "structured courses", "learning programs", "these offerings", "analytics classes", "the programs", "course selections", "training programs"],
    "data analyst certificate": ["analytics certificate", "this credential", "the certificate", "certificate program", "analytics credential", "the credential", "certificate option", "credential program", "certificate track", "analytics certificate program"],
    "data analyst courses": ["analytics courses", "these programs", "training courses", "course options", "analytics programs", "the courses", "learning programs", "structured courses", "analytics classes", "course selections", "training programs"],
    "data analyst courses online": ["online analytics courses", "these remote programs", "self-paced courses", "online programs", "remote courses", "virtual courses", "web-based programs", "online training", "remote learning courses", "self-paced programs", "virtual training", "online course options", "remote programs", "web-based courses", "online learning programs", "self-paced training", "virtual programs", "remote course options", "online offerings", "web-based training", "self-paced options", "remote learning programs", "virtual course options", "online class options", "self-paced offerings"],
    "data analyst training": ["analytics training", "this learning path", "the training", "training program", "skill development", "analytics education", "the program", "learning program", "training path", "analytics skill-building", "professional training", "the learning path", "training route", "skill training", "analytics preparation"],
    "certifications for data analyst": ["analytics certifications", "these credentials", "analyst credentials", "professional certifications", "analytics credentials", "relevant certifications", "credential options", "certification paths", "analyst certifications", "professional credentials", "certification options", "credential programs", "analytics certification paths", "certification credentials", "credential pathways", "certification tracks", "analyst credential options", "professional certification paths", "credential tracks", "certification programs", "credential routes", "analyst certification options", "professional credential paths", "certification routes", "credential programs for analysts"],
    "data analysis bootcamp": ["analytics bootcamp", "this intensive program", "the bootcamp", "bootcamp program", "intensive training", "the program", "bootcamp option", "intensive course", "accelerated program", "bootcamp training", "intensive bootcamp", "the intensive course", "bootcamp route", "accelerated training", "intensive program"],
    "data analysis course": ["analytics course", "this program", "the course", "training course", "analytics program", "the program", "course option", "learning course", "analytics class", "the training", "structured course", "course selection", "program option", "training program", "the class", "analytics training", "course offering", "learning program"],
    "data analyst bootcamp": ["analytics bootcamp", "this intensive program", "the bootcamp", "bootcamp program", "intensive training", "the program", "bootcamp option", "intensive course", "accelerated program", "bootcamp training", "intensive bootcamp", "the intensive course", "bootcamp route", "accelerated training"],
    "data analyst certification online": ["online analytics certification", "this remote credential", "the online certification", "virtual certification", "online credential program", "remote certification", "web-based certification", "online credential", "virtual credential program", "remote analytics certification", "online cert program", "web-based credential", "virtual cert program", "remote credential program", "online certification program", "web-based cert", "virtual certification program", "remote cert option", "online credential path", "web-based certification program", "virtual credential", "remote certification program", "online cert path", "web-based cert program", "virtual cert path"],
    "data analyst course free": ["free analytics course", "no-cost training", "free learning program", "free training option", "no-cost course", "free program", "free learning path", "no-cost analytics training", "free course option", "no-cost program", "free training", "no-cost learning", "free analytics training", "no-cost option", "free learning option", "no-cost analytics course", "free training program", "no-cost training program", "free course path", "no-cost learning program", "free option", "no-cost course option", "free learning resource", "no-cost resource", "free training resource"],
    "data analysis certificate": ["analytics certificate", "this credential", "the certificate", "certificate program", "analytics credential", "the credential", "certificate option", "credential program", "certificate track", "analytics certificate program"],
    "data analysis certification": ["analytics certification", "this credential", "the certification", "certification program", "analytics credential", "the credential", "certification option", "credential program", "certification track", "analytics certification program", "the program credential", "certification pathway", "credential option", "certification route", "analytics credential program", "the certification program"],
}

EXPANSION = """
## Putting Your Learning Into Practice

The gap between completing a program and landing an analyst role is almost always practice, not credentials. Hiring managers care less about which provider you chose and more about whether you can take a messy dataset, frame a clear question, and deliver a recommendation someone can act on. That ability comes from repetition on real problems, not from collecting certificates.

Start by revisiting every project you completed during training and asking whether it would survive scrutiny from a working analyst. Could you explain your SQL choices? Did you document data quality issues? Is the visualization honest about uncertainty? If the answer is no, revise the project before moving on. One polished analysis teaches more than three rushed assignments you never revisit.

Next, find data that resembles what employers in your target industry actually use. Public government datasets, open corporate reports, and community data challenges all provide realistic practice material. The goal is to encounter ambiguity: missing fields, inconsistent formats, and definitions that do not match the documentation. Classroom datasets are useful for learning mechanics; messy real-world data is what builds employable judgment.

Communication practice deserves equal time. Write a one-page summary for each analysis as if your audience is a busy executive who will not open the notebook. Lead with the recommendation, support it with two or three charts, and state what you would measure next. Many strong technical learners lose offers because they cannot translate findings into decisions. Deliberate writing practice closes that gap faster than another technical module.

Finally, treat learning as continuous. Tools change, employer expectations shift, and AI-native workflows are still maturing. The credential you earn today is a foundation, not a ceiling. Schedule monthly time to explore a new dataset, test a new technique, or practice with an AI-native platform so your skills stay current. Analysts who keep learning after their formal program ends are the ones who advance past the first role and build durable careers.
"""


def count_kw(body, keyword):
    kt = re.sub(r"\*\*([^*]+)\*\*", r"\1", body)
    kt = re.sub(r"\*([^*]+)\*", r"\1", kt)
    return len(re.findall(re.escape(keyword.lower()), kt.lower()))


def reduce_kw(body, keyword, target):
    syns = SYNONYMS.get(keyword, ["this program"])
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    matches = list(pattern.finditer(body))
    if len(matches) <= target:
        return body, 0
    result = body
    removed = 0
    for i, m in enumerate(reversed(matches)):
        if len(matches) - i > target:
            syn = syns[removed % len(syns)]
            result = result[:m.start()] + syn + result[m.end():]
            removed += 1
    return result, removed


def main():
    targets = {
        "371-data-analyst-degree": ("data analyst degree", 32, False),
        "372-data-analyst-course": ("data analyst course", 29, False),
        "373-data-analyst-course-online": ("data analyst course online", 27, True),
        "375-data-analysis-courses": ("data analysis courses", 28, True),
        "376-data-analyst-certificate": ("data analyst certificate", 28, True),
        "377-data-analyst-courses": ("data analyst courses", 28, True),
        "378-data-analyst-courses-online": ("data analyst courses online", 27, True),
        "379-data-analyst-training": ("data analyst training", 28, True),
        "380-certifications-for-data-analyst": ("certifications for data analyst", 27, True),
        "381-data-analysis-bootcamp": ("data analysis bootcamp", 28, True),
        "382-data-analysis-course": ("data analysis course", 28, True),
        "383-data-analyst-bootcamp": ("data analyst bootcamp", 28, True),
        "384-data-analyst-certification-online": ("data analyst certification online", 27, True),
        "385-data-analyst-course-free": ("data analyst course free", 27, True),
        "386-data-analysis-certificate": ("data analysis certificate", 28, True),
        "387-data-analysis-certification": ("data analysis certification", 28, True),
    }

    for folder, (kw, target_kw, expand) in targets.items():
        art = ROOT / folder / "article.md"
        text = art.read_text(encoding="utf-8")
        m = re.search(r"^## TL;DR\s*$", text, re.M)
        before = text[:m.start()]
        body = text[m.start():]
        if expand and "## Putting Your Learning Into Practice" not in body:
            body = body.replace("## Frequently Asked Questions", EXPANSION + "\n## Frequently Asked Questions")
        body, removed = reduce_kw(body, kw, target_kw)
        art.write_text(before + body, encoding="utf-8")
        print(f"{folder}: removed {removed}, expanded={expand}, now {count_kw(body, kw)}kw")


if __name__ == "__main__":
    main()
