#!/usr/bin/env python3
"""Generate a priority-ordered deployment checklist CSV with complete URLs (100 articles).

Merges:
  - blog-deploy-order-90d-zh.csv  -> phase / week / keyword-priority / action / status (by 文章编号)
  - blog-content-catalog.csv       -> title / keyword / pillar / type / week / action (100 rows)
Full URL = https://infinisynapse.com/en/blog/{slug}
Sorted by deployment priority: live hubs → week 1..12 → Q2 queue → unscheduled.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SITE = "https://infinisynapse.com"
DEPLOY_ORDER = BLOG / "blog-deploy-order-90d-zh.csv"
CATALOG = BLOG / "frontend-package" / "blog-content-catalog.csv"
OUT = BLOG / "部署清单-完整URL.csv"


def load_order_by_id() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not DEPLOY_ORDER.is_file():
        return out
    for r in csv.DictReader(DEPLOY_ORDER.open(encoding="utf-8-sig")):
        aid = (r.get("文章编号") or "").strip().zfill(3)
        if aid:
            out[aid] = r
    return out


def week_rank(week: str, status: str) -> int:
    w = (week or "").strip()
    if "已上线" in w or "已上线" in (status or ""):
        return 0
    m = re.search(r"第(\d+)周", w)
    if m:
        return int(m.group(1))
    if "Q2" in w:
        return 90
    return 95  # unscheduled / 待发


def status_of(week: str, action: str, order_status: str) -> str:
    if order_status and order_status.strip():
        return order_status.strip()
    if "已上线" in (week or "") or "已上线" in (action or ""):
        return "已上线"
    if "Q2" in (week or "") or "Q2" in (action or ""):
        return "Q2候选（90天后）"
    if re.search(r"第\d+周", week or ""):
        return "已排期·待部署"
    return "未排期·待部署"


def main() -> None:
    order = load_order_by_id()
    rows_out: list[dict] = []

    with CATALOG.open(encoding="utf-8-sig") as f:
        for c in csv.DictReader(f):
            aid = (c.get("文章编号") or "").strip().zfill(3)
            slug = (c.get("slug") or "").strip()
            o = order.get(aid, {})
            week = (o.get("周次") or c.get("计划周次") or "").strip()
            action = (o.get("部署动作") or c.get("部署动作") or "").strip()
            ostatus = (o.get("部署状态") or "").strip()
            rows_out.append({
                "_rank": week_rank(week, ostatus),
                "_aid": aid,
                "部署状态": status_of(week, action, ostatus),
                "周次": week or "未排期",
                "阶段": (o.get("阶段") or "—").strip() or "—",
                "批次": (o.get("批次") or "—").strip() or "—",
                "关键词优先级": (o.get("关键词优先级") or "P1").strip() or "P1",
                "部署动作": action or "待发文章",
                "文章编号": aid,
                "slug": slug,
                "完整URL": f"{SITE}/en/blog/{slug}",
                "英文标题": c.get("英文标题", ""),
                "目标关键词": c.get("目标关键词", ""),
                "支柱编号": c.get("支柱编号", ""),
                "支柱名称": c.get("支柱名称", ""),
                "内容类型": c.get("内容类型", ""),
                "详情页组件": c.get("详情页组件", ""),
                "head片段": f"head/{slug}.html",
                "内容目录": c.get("内容目录", ""),
                "上线后检查项": (o.get("上线后检查项") or
                                "渲染article.md；注入head.html（canonical/描述/og/twitter/JSON-LD）；上传images；"
                                "校验单H1+canonical+描述150-160").strip(),
                "依赖先上线slug": (o.get("依赖先上线的slug") or "").strip(),
                "GSC已提交": (o.get("GSC已提交") or "").strip(),
                "上线日期": (o.get("上线日期") or "").strip(),
            })

    # priority sort: week rank, then live first within rank 0, then article id
    rows_out.sort(key=lambda r: (r["_rank"], r["_aid"]))

    fields = [
        "部署优先级", "部署状态", "周次", "阶段", "批次", "关键词优先级", "部署动作",
        "文章编号", "slug", "完整URL", "英文标题", "目标关键词",
        "支柱编号", "支柱名称", "内容类型", "详情页组件", "head片段", "内容目录",
        "上线后检查项", "依赖先上线slug", "GSC已提交", "上线日期",
    ]
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(rows_out, 1):
            r.pop("_rank"); r.pop("_aid")
            w.writerow({"部署优先级": i, **{k: r.get(k, "") for k in fields if k != "部署优先级"}})

    print(f"Wrote {len(rows_out)} rows → {OUT}")
    from collections import Counter
    print("状态分布:", dict(Counter(r["部署状态"] for r in rows_out)))


if __name__ == "__main__":
    main()
