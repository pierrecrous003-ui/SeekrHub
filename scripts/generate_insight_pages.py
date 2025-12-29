from pathlib import Path
import random

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
PEOPLE_ROOT = BASE_DIR / "people"

TEMPLATE_DIR = BASE_DIR / "templates" / "insights"
BASE_TEMPLATE = TEMPLATE_DIR / "base.html"
BLOCKS_FILE = TEMPLATE_DIR / "blocks.html"

INSIGHT_FOLDER_NAME = "insights"

SITE_ROOT_URL = "https://seekrhub.pro"  # adjust if needed

# =====================================================
# LOAD TEMPLATES
# =====================================================

base_html = BASE_TEMPLATE.read_text(encoding="utf-8")
blocks_html = BLOCKS_FILE.read_text(encoding="utf-8")

# =====================================================
# BLOCK EXTRACTION
# =====================================================

def extract_block(marker: str) -> str:
    start = blocks_html.find(f"<!-- {marker} -->")
    if start == -1:
        return ""
    end = blocks_html.find("<!--", start + 10)
    return blocks_html[start:end].strip()

BLOCKS = {
    "INTRO": extract_block("INTRO"),
    "ROLE_DEF": extract_block("ROLE DEFINITION"),
    "RESPONSIBILITIES": extract_block("RESPONSIBILITIES"),
    "SKILLS": extract_block("SKILLS"),
    "TOOLS": extract_block("TOOLS"),
    "INDUSTRIES": extract_block("INDUSTRIES"),
    "MARKET": extract_block("MARKET"),
    "DISCLAIMER": extract_block("DISCLAIMER"),
}

ARCHETYPES = [
    ["INTRO", "ROLE_DEF", "RESPONSIBILITIES", "INDUSTRIES", "DISCLAIMER"],
    ["INTRO", "SKILLS", "TOOLS", "RESPONSIBILITIES", "DISCLAIMER"],
    ["INTRO", "MARKET", "INDUSTRIES", "ROLE_DEF", "DISCLAIMER"],
]

TITLE_PATTERNS = [
    "How {role}s Typically Work in {country}",
    "Skills and Responsibilities of {role}s in {country}",
    "Where {role}s Fit Within Organisations in {country}",
]

# =====================================================
# PLACEHOLDER RENDERING
# =====================================================

def hydrate_placeholders(html: str, *, role_title, role_slug, country_name, country_slug):
    return (
        html
        .replace("{{ROLE_TITLE}}", role_title)
        .replace("{{ROLE_SLUG}}", role_slug)
        .replace("{{COUNTRY_NAME}}", country_name)
        .replace("{{COUNTRY_SLUG}}", country_slug)
    )

# =====================================================
# MAIN GENERATOR
# =====================================================

def generate_insight_pages():
    generated = 0

    for role_dir in PEOPLE_ROOT.iterdir():
        if not role_dir.is_dir():
            continue

        role_slug = role_dir.name
        role_title = role_slug.replace("-", " ").title()

        for country_dir in role_dir.iterdir():
            if not country_dir.is_dir():
                continue

            country_slug = country_dir.name
            country_name = country_slug.replace("-", " ").title()

            insight_dir = country_dir / INSIGHT_FOLDER_NAME
            insight_dir.mkdir(exist_ok=True)

            output_file = insight_dir / "index.html"

            if output_file.exists():
                continue

            # -------------------------------
            # Content assembly
            # -------------------------------

            archetype = random.choice(ARCHETYPES)
            middle = archetype[1:-1]
            random.shuffle(middle)
            ordered = [archetype[0]] + middle + [archetype[-1]]

            content_blocks = []
            for block_key in ordered:
                raw_block = BLOCKS.get(block_key, "")
                hydrated_block = hydrate_placeholders(
                    raw_block,
                    role_title=role_title,
                    role_slug=role_slug,
                    country_name=country_name,
                    country_slug=country_slug,
                )
                content_blocks.append(hydrated_block)

            content_html = "\n\n".join(content_blocks)

            # -------------------------------
            # Metadata
            # -------------------------------

            title = random.choice(TITLE_PATTERNS).format(
                role=role_title,
                country=country_name,
            )

            canonical_url = (
                f"{SITE_ROOT_URL}/people/"
                f"{role_slug}/{country_slug}/insights/"
            )

            # -------------------------------
            # Final render
            # -------------------------------

            rendered = (
                base_html
                .replace("{{PAGE_TITLE}}", title)
                .replace("{{H1_TITLE}}", title)
                .replace(
                    "{{META_DESCRIPTION}}",
                    f"An overview of how {role_title}s typically work in {country_name}."
                )
                .replace("{{CANONICAL_URL}}", canonical_url)
                .replace(
                    "{{TAGLINE_TEXT}}",
                    f"Insights into the {role_title} role in {country_name}"
                )
                .replace("{{CONTENT_BLOCKS}}", content_html)
            )

            output_file.write_text(rendered, encoding="utf-8")
            generated += 1

    print(f"✔ Insight pages generated: {generated}")

# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    generate_insight_pages()
