"""Production URL constants for InfiniSynapse blog (infinisynapse.com + locale paths)."""

DOMAIN = "infinisynapse.com"
LOCALE_EN = "en"
LOCALE_ZH = "zh"

SITE = f"https://{DOMAIN}"
APP = f"https://app.{DOMAIN}"

# English blog page (canonical for EN articles)
def blog_url_en(slug: str) -> str:
    return f"{SITE}/{LOCALE_EN}/blog/{slug}"


def blog_url_zh(slug: str) -> str:
    return f"{SITE}/{LOCALE_ZH}/blog/{slug}"


def blog_path_en(slug: str) -> str:
    return f"/{LOCALE_EN}/blog/{slug}"


def asset_url(pillar: str, slug: str, filename: str = "hero.png") -> str:
    # static assets — no locale prefix
    return f"{SITE}/blog/assets/{pillar}/{slug}/{filename}"


def about_url() -> str:
    return f"{SITE}/{LOCALE_EN}/about"


def logo_url() -> str:
    return f"{SITE}/logo.png"
