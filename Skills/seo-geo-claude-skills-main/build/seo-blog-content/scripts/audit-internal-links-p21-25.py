#!/usr/bin/env python3
"""Audit internal links for Pillars 21-25 (Library Model)."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = {
    "pillar21-data-analysis-fundamentals": {
        "hub": "300-data-analysis-complete-guide",
        "hub_slug": "data-analysis-complete-guide",
    },
    "pillar22-advanced-data-analysis-methods": {
        "hub": "317-python-data-analysis-guide",
        "hub_slug": "python-data-analysis-guide",
    },
    "pillar23-data-analysis-tools-software": {
        "hub": "334-data-analysis-tools-guide",
        "hub_slug": "data-analysis-tools-guide",
    },
    "pillar24-data-analyst-career-jobs": {
        "hub": "352-data-analyst-guide",
        "hub_slug": "data-analyst-guide",
    },
    "pillar25-data-analyst-learning-certification": {
        "hub": "370-data-analyst-certification-guide",
        "hub_slug": "data-analyst-certification-guide",
    },
}

# Planned sibling links from architecture doc (folder numbers)
PLANNED_SIBLINGS: dict[str, list[str]] = {
    "301-what-is-data-analysis": ["302", "311"],
    "302-data-analysis-definition": ["301", "303"],
    "303-data-analysis-meaning": ["302", "304"],
    "304-analysis-of-data": ["312", "316"],
    "305-what-analysis-of-data": ["304", "306"],
    "306-data-analysis-what-is": ["301", "305"],
    "307-what-is-the-analysis-of-data": ["308", "313"],
    "308-whats-a-data-analysis": ["301", "303"],
    "309-what-is-meant-by-data-analysis": ["302", "316"],
    "310-exploratory-data-analysis": ["312", "313"],
    "311-data-analysis-process": ["310", "313"],
    "312-data-analysis-methods": ["313", "314"],
    "313-data-analysis-techniques": ["312", "315"],
    "314-types-of-data-analysis": ["312", "313"],
    "315-data-analysis-example": ["316", "310"],
    "316-data-analysis-examples": ["315", "314"],
    "318-python-for-data-analysis": ["319", "320"],
    "319-data-analysis-with-python": ["318", "320"],
    "320-sql-data-analysis": ["321", "317"],
    "321-data-analysis-using-sql": ["320", "317"],
    "322-r-data-analysis": ["318", "320"],
    "323-qualitative-data-analysis": ["324", "325"],
    "324-qualitative-research-data-analysis": ["323", "325"],
    "325-qualitative-studies-data-analysis": ["323", "326"],
    "326-data-analysis-of-qualitative-data": ["324", "323"],
    "327-survey-data-analysis": ["323", "331"],
    "328-secondary-data-analysis": ["327", "333"],
    "329-spatial-data-analysis": ["330", "327"],
    "330-topological-data-analysis": ["329", "331"],
    "331-bayesian-data-analysis": ["332", "333"],
    "332-predictive-data-analysis": ["331", "333"],
    "333-financial-data-analysis": ["332", "328"],
    "335-data-analysis-software": ["336", "340"],
    "336-data-analysis-tool": ["335", "337"],
    "337-tools-for-data-analysis": ["336", "338"],
    "338-software-for-data-analysis": ["335", "337"],
    "339-data-analysis-platform": ["340", "334"],
    "340-data-analysis-platforms": ["339", "335"],
    "341-analytical-tools-for-data-analysis": ["337", "342"],
    "342-programs-for-data-analysis": ["341", "338"],
    "343-tableau-public-data-analysis": ["344", "345"],
    "344-tableau-data-analysis-tool": ["343", "345"],
    "345-data-analysis-tools-tableau": ["343", "344"],
    "346-excel-data-analysis-tool": ["347", "350"],
    "347-microsoft-office-excel-data-analysis": ["346", "348"],
    "348-excel-data-analysis": ["349", "351"],
    "349-excel-data-analysis-toolpak": ["348", "347"],
    "350-microsoft-excel-data-analysis": ["346", "348"],
    "351-excel-for-data-analysis": ["348", "334"],
    "353-data-analyst-jobs": ["354", "359"],
    "354-data-analyst-salary": ["368", "367"],
    "355-what-does-a-data-analyst-do": ["356", "358"],
    "356-what-do-data-analysts-do": ["355", "358"],
    "357-how-to-become-a-data-analyst": ["369", "358"],
    "358-what-is-a-data-analyst": ["355", "352"],
    "359-data-analyst-job-description": ["353", "369"],
    "360-entry-level-data-analyst-jobs": ["361", "357"],
    "361-remote-data-analyst-jobs": ["360", "353"],
    "362-data-analyst-internship": ["360", "363"],
    "363-junior-data-analyst-jobs": ["360", "362"],
    "364-data-analyst-vs-data-scientist": ["358", "369"],
    "365-data-analyst-resume": ["366", "359"],
    "366-data-analyst-interview-questions": ["365", "369"],
    "367-senior-data-analyst-salary": ["354", "368"],
    "368-data-analyst-pay": ["354", "367"],
    "369-data-analyst-skills": ["357", "364"],
    "371-data-analyst-degree": ["372", "379"],
    "372-data-analyst-course": ["373", "380"],
    "373-data-analyst-course-online": ["372", "385"],
    "374-certified-data-analysis": ["370", "383"],
    "375-data-analysis-courses": ["372", "382"],
    "376-data-analyst-certificate": ["370", "384"],
    "377-data-analyst-courses": ["372", "373"],
    "378-data-analyst-courses-online": ["373", "377"],
    "379-data-analyst-training": ["371", "381"],
    "380-certifications-for-data-analyst": ["370", "376"],
    "381-data-analysis-bootcamp": ["384", "379"],
    "382-data-analysis-course": ["375", "372"],
    "383-data-analyst-bootcamp": ["381", "384"],
    "384-data-analyst-certification-online": ["370", "376"],
    "385-data-analyst-course-free": ["373", "372"],
    "386-data-analysis-certificate": ["376", "387"],
    "387-data-analysis-certification": ["386", "374"],
}

BANNED = re.compile(
    r"## Related Reading|Within this topic cluster|## Conclusion \+ Related Reading",
    re.I,
)


def slug_from_article(path: Path) -> str:
    sidecar = path.parent / "article-meta.json"
    if sidecar.is_file():
        import json

        raw = json.loads(sidecar.read_text(encoding="utf-8")).get("slug", "")
        if raw:
            return raw.replace("/blog/", "").strip("/")
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\*\*Slug\*\*:\s*`?/blog/([a-z0-9-]+)`?", text)
    if m:
        return m.group(1)
    m = re.match(r"\d{3}-(.+)", path.parent.name)
    return m.group(1) if m else path.parent.name


def internal_slugs(text: str) -> set[str]:
    slugs = set()
    for _, slug in re.findall(
        r"\[([^\]]+)\]\((?:https?://[^/]+)?(?:/[a-z]{2})?/blog/([^)/\s]+)", text
    ):
        slugs.add(slug.strip("/").split("/")[-1])
    return slugs


def folder_num(folder: str) -> str:
    return folder[:3]


def audit_pillar(pdir: Path, meta: dict) -> list[dict]:
    hub_folder = meta["hub"]
    hub_slug = meta["hub_slug"]
    articles = sorted(pdir.glob("[0-9][0-9][0-9]-*/article.md"))
    folder_to_slug = {a.parent.name: slug_from_article(a) for a in articles}
    clusters = [f for f in folder_to_slug if f != hub_folder]
    results = []

    for art in articles:
        folder = art.parent.name
        text = art.read_text(encoding="utf-8")
        slugs = internal_slugs(text)
        fails = []
        is_hub = folder == hub_folder

        if BANNED.search(text):
            fails.append("banned Related Reading / cluster dump block")

        if is_hub:
            if "Cluster guides in this pillar" not in text and "Cluster Guides in This Pillar" not in text:
                fails.append("hub missing 'Cluster guides in this pillar' section")
            missing_table = [folder_to_slug[c] for c in clusters if folder_to_slug[c] not in slugs]
            if missing_table:
                fails.append(f"hub table/prose missing {len(missing_table)} cluster links: {missing_table[:5]}{'...' if len(missing_table)>5 else ''}")
        else:
            if hub_slug not in slugs:
                fails.append(f"missing hub link: /blog/{hub_slug}")
            sibling_slugs = {folder_to_slug[f] for f in clusters if f != folder}
            linked_siblings = slugs & sibling_slugs
            if len(linked_siblings) < 2:
                fails.append(f"cluster needs >=2 sibling links (has {len(linked_siblings)})")
            # check planned siblings
            planned = PLANNED_SIBLINGS.get(folder, [])
            if planned:
                planned_folders = [f"{n}-" for n in planned]
                planned_slugs = []
                for pf, ps in folder_to_slug.items():
                    if any(pf.startswith(p) for p in [f"{n}-" for n in planned]):
                        # match by folder number prefix
                        pass
                for num in planned:
                    match = [folder_to_slug[f] for f in folder_to_slug if f.startswith(f"{num}-")]
                    if match:
                        planned_slugs.append(match[0])
                missing_planned = [s for s in planned_slugs if s not in slugs]
                if missing_planned:
                    fails.append(f"missing planned siblings: {missing_planned}")

        results.append({
            "folder": folder,
            "role": "hub" if is_hub else "cluster",
            "slug": folder_to_slug[folder],
            "internal_count": len(slugs),
            "pass": len(fails) == 0,
            "fails": fails,
        })
    return results


def main():
    total = passed = 0
    pillar_summary = []
    for pname, meta in PILLARS.items():
        pdir = BLOG / pname
        rows = audit_pillar(pdir, meta)
        p_pass = sum(1 for r in rows if r["pass"])
        p_total = len(rows)
        total += p_total
        passed += p_pass
        pillar_summary.append((pname, p_pass, p_total))
        print(f"\n{'='*60}\n{pname}  ({p_pass}/{p_total} pass)\n{'='*60}")
        for r in rows:
            mark = "✓" if r["pass"] else "✗"
            print(f"  {mark} [{r['role']:7}] {r['folder']:<42} {r['internal_count']:2} links")
            for f in r["fails"]:
                print(f"       · {f}")

    print(f"\n{'='*60}")
    print("PILLAR SUMMARY")
    print(f"{'='*60}")
    for pname, pp, pt in pillar_summary:
        print(f"  {pname:<45} {pp:2}/{pt} pass")
    print(f"\nTOTAL: {passed}/{total} articles pass internal link audit")


if __name__ == "__main__":
    main()
