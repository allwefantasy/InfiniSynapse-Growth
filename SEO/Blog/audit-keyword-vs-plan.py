#!/usr/bin/env python3
"""Reconcile each article's Target keyword against the planning doc's chosen keyword.

Plan: SEO/100页主题集群规划-v1-替换后主关键词版.md
  - "### NNN. <original topic>"  = original topic (heading)
  - first table data row, col 1  = 替换后主关键词 (library/SEMrush-validated)  -> the REQUIRED keyword
  - col 2 = Volume

Output: SEO/Blog/keyword-reconcile.csv (编号 / 原始主题 / 规划关键词 / 规划Volume /
        实际关键词 / 是否一致 / 差异类型 / 建议)
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # SEO/
BLOG = Path(__file__).parent
PLAN = ROOT / "100页主题集群规划-v1-替换后主关键词版.md"
OUT = BLOG / "keyword-reconcile.csv"


def parse_plan() -> dict[str, dict]:
    out: dict[str, dict] = {}
    cur = None
    topic = ""
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        m = re.match(r"###\s+(\d{3})\.\s*(.+)", line)
        if m:
            cur, topic = m.group(1), m.group(2).strip()
            continue
        if not cur or not line.startswith("| "):
            continue
        if "Volume" in line or ":---" in line or "关键词 " in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if cells and cur not in out:
            out[cur] = {"topic": topic, "keyword": cells[0],
                        "volume": cells[1] if len(cells) > 1 else ""}
    return out


def read_actual() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for pillar in sorted(BLOG.glob("pillar[1-8]-*")):
        if " copy" in pillar.name:
            continue
        for md in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            aid = md.parent.name[:3]
            t = md.read_text(encoding="utf-8")
            m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", t)
            out[aid] = {"keyword": m.group(1).strip() if m else "<缺失>",
                        "folder": md.parent.name}
    return out


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().replace("-", " ")).strip()


def diff_type(plan_kw: str, actual_kw: str) -> str:
    p, a = norm(plan_kw), norm(actual_kw)
    if p == a:
        return "一致"
    if set(p.split()) == set(a.split()):
        return "语序/措辞差异（语义相近）"
    if a == norm(actual_kw) and a != p and len(set(p.split()) & set(a.split())) >= 1:
        return "部分重叠（需复核）"
    return "完全不同（疑退回原始主题）"


def main() -> None:
    plan = parse_plan()
    actual = read_actual()
    rows = []
    for aid in sorted(plan):
        p = plan[aid]
        a = actual.get(aid, {"keyword": "<缺失>"})
        dt = diff_type(p["keyword"], a["keyword"])
        consistent = dt == "一致"
        if consistent:
            suggestion = "无需处理"
        elif "语序" in dt:
            suggestion = "可保留（语义一致）或按规划微调"
        elif "部分重叠" in dt:
            suggestion = "人工复核：是否改回规划词"
        else:
            suggestion = "建议改回规划词（实际词可能不在SEMrush）"
        rows.append({
            "编号": aid,
            "原始主题": p["topic"],
            "规划关键词(替换后)": p["keyword"],
            "规划搜索量": p["volume"],
            "实际Target关键词": a["keyword"],
            "是否一致": "是" if consistent else "否",
            "差异类型": dt,
            "建议": suggestion,
            "slug": a.get("folder", "").split("-", 1)[-1] if a.get("folder") else "",
        })

    fields = ["编号", "原始主题", "规划关键词(替换后)", "规划搜索量", "实际Target关键词",
              "是否一致", "差异类型", "建议", "slug"]
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    from collections import Counter
    c = Counter(r["差异类型"] for r in rows)
    print(f"Wrote {len(rows)} rows -> {OUT}\n")
    for k, v in c.most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
