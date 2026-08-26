#!/usr/bin/env python3
"""Ensure Target keyword appears in H1, article description, and meta-tags."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BLOG = Path(__file__).parent
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar2-data-agent-vs-alternatives",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

DESC_MAX = 165


def extract_keyword(text: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).strip() if m else ""


def extract_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_article_desc(text: str) -> str:
    m = re.search(r"\*\*Meta Description\*\*:\s*(.+)$", text, re.M)
    if not m:
        return ""
    desc = m.group(1).strip()
    return re.sub(r"\s*\(\d+\s*chars\)\s*$", "", desc, flags=re.I)


def kw_title_case(kw: str) -> str:
    small = {"for", "to", "in", "on", "with", "and", "or", "a", "an", "the", "of", "vs"}
    parts = kw.split()
    out = []
    for i, p in enumerate(parts):
        low = p.lower()
        if i > 0 and low in small:
            out.append(low)
        elif low == "nl2sql":
            out.append("NL2SQL")
        elif low == "ai":
            out.append("AI")
        elif low == "sql":
            out.append("SQL")
        elif low == "csv":
            out.append("CSV")
        elif low == "cto":
            out.append("CTO")
        elif low == "saas":
            out.append("SaaS")
        elif "-" in p:
            out.append("-".join(x.capitalize() if x.lower() not in small else x.lower() for x in p.split("-")))
        else:
            out.append(p.capitalize())
    return " ".join(out)


def split_year(h1: str) -> tuple[str, str]:
    m = re.search(r"\s*(\(20\d{2}\))\s*$", h1)
    if m:
        return h1[: m.start()].strip(), f" {m.group(1)}"
    return h1.strip(), ""


def recover_desc_from_preview(folder: Path) -> str:
    preview = folder / "preview.html"
    if not preview.is_file():
        return ""
    mt = preview.read_text(encoding="utf-8")
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', mt, re.I)
    return m.group(1).strip() if m else ""


def recover_h1_from_preview(folder: Path) -> str:
    preview = folder / "preview.html"
    if not preview.is_file():
        return ""
    mt = preview.read_text(encoding="utf-8")
    m = re.search(r"<title>([^<]+)</title>", mt, re.I)
    return m.group(1).strip() if m else ""


def looks_truncated(text: str) -> bool:
    if not text:
        return False
    if text.endswith("(") or text.endswith(" —"):
        return True
    if " — " in text:
        frag = text.rsplit(" — ", 1)[1]
        if len(frag) < 20 and kw_fragment(frag):
            return True
    if len(text) >= DESC_MAX - 3 and not text.rstrip().endswith((".", "!", "?", "…")):
        tail = text.split()[-1] if text.split() else ""
        if len(tail) <= 4:
            return True
    return False


def kw_fragment(s: str) -> bool:
    return bool(re.match(r"^[A-Za-z]{1,12}$", s.strip()))


def strip_redundant_suffix(h1: str, kw: str) -> str:
    if " — " not in h1:
        return h1
    left, right = h1.rsplit(" — ", 1)
    left = left.strip()
    right_l = right.lower()
    kw_l = kw.lower()
    if kw_l in left.lower():
        return left
    if right_l in kw_l or kw_l.startswith(right_l) or right_l.startswith(kw_l[: max(8, len(right_l))]):
        if kw_l in left.lower():
            return left
    if kw_fragment(right):
        return left
    return h1


def clean_broken_h1(h1: str, kw: str, folder: Path) -> str:
    h1 = strip_redundant_suffix(h1, kw)
    if looks_truncated(h1) or "[/" in h1 or "](/blog/" in h1:
        recovered = recover_h1_from_preview(folder)
        if recovered and not looks_truncated(recovered):
            h1 = recovered
    if " — " in h1:
        left, right = h1.rsplit(" — ", 1)
        if kw_fragment(right):
            h1 = left.strip()
    if h1.endswith("("):
        h1 = h1.rstrip(" (").strip()
    if "[/" in h1:
        h1 = h1.split("[/", 1)[0].strip()
    return strip_redundant_suffix(h1, kw)


def clean_broken_desc(desc: str, folder: Path) -> str:
    if looks_truncated(desc):
        recovered = recover_desc_from_preview(folder)
        if recovered:
            return recovered
    return desc


def shorten_base(base: str) -> str:
    short = re.sub(r"^How to ", "", base, flags=re.I)
    short = re.sub(r"^Connect ", "", short, flags=re.I)
    short = re.sub(r"^Analyze ", "", short, flags=re.I)
    return short.strip()


def weave_title(h1: str, kw: str, folder: Path) -> str:
    h1 = clean_broken_h1(h1, kw, folder)
    if kw.lower() in h1.lower():
        return h1

    kwt = kw_title_case(kw)
    base, year = split_year(h1)
    subtitle = ""
    if ":" in base:
        head, subtitle = base.split(":", 1)
        subtitle = subtitle.strip()
        base = head.strip()

    tokens = kw.lower().split()
    if all(t in base.lower() for t in tokens):
        if subtitle:
            return f"{kwt}{year}: {subtitle}"
        return f"{kwt}{year}"

    for extra in ("tools", "tool"):
        trial = re.sub(rf"\b{extra}\b", "", base, count=1, flags=re.I)
        trial = re.sub(r"\s{2,}", " ", trial).strip()
        if kw.lower() in trial.lower():
            return trial + year

    short = shorten_base(base)
    candidates = [
        f"{kwt}{year}: {subtitle}" if subtitle else "",
        f"{kwt}: {short}{year}",
        f"{kwt}{year}: {short}",
        f"{kwt}{year}",
    ]
    for c in candidates:
        if c and kw.lower() in c.lower():
            return strip_redundant_suffix(c, kw)

    return f"{kwt}{year}"


def smart_trim(text: str, max_len: int, kw: str) -> str:
    if len(text) <= max_len:
        return text
    trimmed = text[:max_len]
    if kw.lower() not in trimmed.lower():
        return text
    if " " in trimmed:
        trimmed = trimmed.rsplit(" ", 1)[0]
        if trimmed and trimmed[-1] in ",;:":
            trimmed = trimmed[:-1] + "."
    return trimmed


def weave_description(desc: str, kw: str, h1: str, folder: Path) -> str:
    desc = clean_broken_desc(desc, folder)
    if not desc:
        desc = recover_desc_from_preview(folder)

    if desc and kw.lower() in desc.lower():
        if looks_truncated(desc):
            recovered = recover_desc_from_preview(folder)
            if recovered:
                desc = recovered
            elif not desc.rstrip().endswith((".", "!", "?")):
                desc = desc.rstrip() + "."
        return smart_trim(desc, DESC_MAX, kw)

    if desc:
        for old, new in (
            (" tools for ", " for "),
            (" tool for ", " for "),
            ("Compare the best ", "The best "),
        ):
            trial = desc.replace(old, new)
            if kw.lower() in trial.lower():
                return smart_trim(trial, DESC_MAX, kw)

    kwt = kw_title_case(kw)
    if not desc:
        if "connect" in h1.lower() or "analyze" in h1.lower():
            desc = (
                f"{kwt} guide with setup checklist, security controls, example SQL, "
                "and FAQ for 2026 teams."
            )
        else:
            desc = (
                f"{kwt} in 2026: practical workflow patterns, governance controls, "
                "and FAQ for data teams."
            )
        return smart_trim(desc, DESC_MAX, kw)

    prefix = f"{kwt}: "
    if kw.lower() in desc.lower():
        woven = desc
    else:
        woven = f"{prefix}{desc}"
    if kw.lower() not in woven.lower():
        woven = f"Guide to {kwt} for 2026 teams. {desc}"
    if len(woven) > DESC_MAX:
        body_budget = DESC_MAX - len(prefix)
        if body_budget > 40 and not woven.startswith(prefix):
            body = woven[:DESC_MAX].rsplit(" ", 1)[0]
            woven = body if body.endswith((".", "!", "?")) else body + "."
        elif body_budget > 40:
            body = desc[:body_budget].rsplit(" ", 1)[0]
            woven = prefix + body
            if not woven.endswith((".", "!", "?")):
                woven += "."
    return smart_trim(woven, DESC_MAX, kw)


def set_h1(text: str, new_h1: str) -> str:
    return re.sub(r"^# .+$", f"# {new_h1}", text, count=1, flags=re.M)


def set_article_desc(text: str, desc: str) -> str:
    if re.search(r"\*\*Meta Description\*\*:", text):
        return re.sub(
            r"\*\*Meta Description\*\*:\s*.+$",
            f"**Meta Description**: {desc}",
            text,
            count=1,
            flags=re.M,
        )
    slug_m = re.search(r"(\*\*Slug\*\*:\s*.+$)", text, re.M)
    if slug_m:
        return text[: slug_m.start()] + f"**Meta Description**: {desc}\n\n" + text[slug_m.start() :]
    return text


def sync_meta_tags(meta_path: Path, title: str, desc: str) -> bool:
    if not meta_path.is_file():
        return False
    mt = meta_path.read_text(encoding="utf-8")
    original = mt
    mt = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", mt, count=1, flags=re.I)
    mt = re.sub(
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        mt,
        count=1,
        flags=re.I,
    )
    mt = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\g<1>{title}\2",
        mt,
        count=1,
        flags=re.I,
    )
    mt = re.sub(
        r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")',
        rf"\g<1>{title}\2",
        mt,
        count=1,
        flags=re.I,
    )
    mt = re.sub(
        r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        mt,
        count=1,
        flags=re.I,
    )
    mt = re.sub(
        r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        mt,
        count=1,
        flags=re.I,
    )
    if mt != original:
        meta_path.write_text(mt, encoding="utf-8")
        return True
    return False


def sync_schema(schema_path: Path, title: str, desc: str) -> bool:
    if not schema_path.is_file():
        return False
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    changed = False
    for block in data:
        if block.get("@type") == "BlogPosting":
            if block.get("headline") != title:
                block["headline"] = title
                changed = True
            if block.get("description") != desc:
                block["description"] = desc
                changed = True
    if changed:
        schema_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def process(article_path: Path) -> bool:
    folder = article_path.parent
    text = article_path.read_text(encoding="utf-8")
    kw = extract_keyword(text)
    if not kw:
        return False
    h1 = extract_h1(text)
    desc = extract_article_desc(text)
    new_h1 = strip_redundant_suffix(weave_title(h1, kw, folder), kw)
    new_desc = weave_description(desc, kw, new_h1, folder)
    new_text = text
    if new_h1 != h1:
        new_text = set_h1(new_text, new_h1)
    if new_desc != desc or not extract_article_desc(new_text):
        new_text = set_article_desc(new_text, new_desc)

    changed = new_text != text
    if changed:
        article_path.write_text(new_text, encoding="utf-8")

    meta_changed = sync_meta_tags(folder / "meta-tags.html", new_h1, new_desc)
    schema_changed = sync_schema(folder / "schema.json", new_h1, new_desc)
    return changed or meta_changed or schema_changed


def main() -> int:
    targets: list[Path] = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            p = Path(arg)
            if p.is_dir():
                targets.extend(sorted(p.glob("[0-9][0-9][0-9]-*/article.md")))
            elif p.is_file():
                targets.append(p)
    else:
        for pillar in PILLARS:
            if pillar.is_dir():
                targets.extend(sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")))

    changed = 0
    for art in targets:
        if process(art):
            changed += 1
            print(f"fixed: {art.parent.name}")
    print(f"\nUpdated {changed} articles/bundles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
