"""Resolve Target keyword and P21-25 article metadata from sidecar or legacy sources."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TypedDict


class ArticleMeta(TypedDict, total=False):
    slug: str
    target_keyword: str
    secondary: list[str]


def _slug_from_folder(folder: str) -> str:
    m = re.match(r"\d{3}-(.+)", folder)
    return m.group(1) if m else folder


def _from_schema(schema_path: Path) -> ArticleMeta:
    if not schema_path.is_file():
        return {}
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    for block in data:
        if block.get("@type") == "BlogPosting":
            url = block.get("url") or block.get("mainEntityOfPage") or ""
            slug_part = url.rstrip("/").split("/")[-1] if url else ""
            kw = block.get("keywords") or ""
            if isinstance(kw, list):
                kw = kw[0] if kw else ""
            about = block.get("about") or []
            secondary: list[str] = []
            if isinstance(about, list) and len(about) > 1:
                secondary = [a.get("name", "") for a in about[1:] if a.get("name")]
            return {
                "slug": f"/blog/{slug_part}" if slug_part and not slug_part.startswith("/") else slug_part,
                "target_keyword": str(kw).strip(),
                "secondary": secondary,
            }
    return {}


def from_article_md(text: str) -> ArticleMeta:
    slug_m = re.search(r"\*\*Slug\*\*:\s*`?(/blog/[a-z0-9-]+)`?", text)
    kw_m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    sec_m = re.search(r"\*\*Secondary\*\*:\s*(.+)$", text, re.M)
    secondary: list[str] = []
    if sec_m:
        secondary = [s.strip().strip("`") for s in sec_m.group(1).split(",") if s.strip()]
    return {
        "slug": slug_m.group(1) if slug_m else "",
        "target_keyword": kw_m.group(1).strip() if kw_m else "",
        "secondary": secondary,
    }


# Back-compat alias used by strip-authoring-meta-p21-25.py
_from_article_md = from_article_md


def read_meta(article_path: Path) -> ArticleMeta:
    """Load metadata: article-meta.json > legacy article.md fields > schema.json."""
    folder = article_path.parent
    sidecar = folder / "article-meta.json"
    if sidecar.is_file():
        raw = json.loads(sidecar.read_text(encoding="utf-8"))
        return {
            "slug": raw.get("slug", ""),
            "target_keyword": raw.get("target_keyword", ""),
            "secondary": raw.get("secondary", []),
        }

    text = article_path.read_text(encoding="utf-8") if article_path.is_file() else ""
    meta = from_article_md(text)
    if meta.get("target_keyword"):
        return meta

    schema_meta = _from_schema(folder / "schema.json")
    if schema_meta.get("target_keyword"):
        if not schema_meta.get("slug"):
            schema_meta["slug"] = f"/blog/{_slug_from_folder(folder.name)}"
        return schema_meta

    return {
        "slug": f"/blog/{_slug_from_folder(folder.name)}",
        "target_keyword": "",
        "secondary": [],
    }


def target_keyword(article_path: Path, text: str | None = None) -> str:
    """Keyword for audits: sidecar first, then legacy md, then schema."""
    sidecar = article_path.parent / "article-meta.json"
    if sidecar.is_file():
        kw = json.loads(sidecar.read_text(encoding="utf-8")).get("target_keyword", "").strip()
        if kw:
            return kw

    if text is None and article_path.is_file():
        text = article_path.read_text(encoding="utf-8")
    if text:
        m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
        if m:
            return m.group(1).strip()

    return read_meta(article_path).get("target_keyword", "")


def slug(article_path: Path) -> str:
    return read_meta(article_path).get("slug", "")
