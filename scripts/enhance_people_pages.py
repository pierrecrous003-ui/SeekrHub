from pathlib import Path
import random

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PEOPLE_ROOT = BASE_DIR / "people"
TEMPLATE_DIR = BASE_DIR / "templates" / "people"

BASE_TEMPLATE = TEMPLATE_DIR / "base.html"
BLOCKS_FILE = TEMPLATE_DIR / "blocks.html"

SITE_BASE_URL = "https://seekrhub.pro"

ENHANCEMENT_MARKER = "<!-- SEEKRHUB_PEOPLE_ENHANCED_V1 -->"

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
    "MARKET": extract_block("MARKET CONTEXT"),
    "INSIGHT": extract_block("INSIGHT LINK"),
    "CTA": extract_block("CTA"),
    "DISCLAIMER": extract_block("DISCLAIMER"),
}

ARCHETYPES = [
    ["INTRO", "INDUSTRIES", "INSIGHT", "CTA", "DISCLAIMER"],
    ["INTRO", "SKILLS", "TOOLS", "INSIGHT", "CTA", "DISCLAIMER"],
    ["INTRO", "RESPONSIBILITIES", "INDUSTRIES", "INSIGHT", "CTA", "DISCLAIMER"],
]

# =====================================================
# ROLE-TYPE ENHANCEMENT BLOCKS (CEILING KILLER)
# =====================================================

ROLE_TYPE_BLOCKS = {
    "managerial": """
<section>
    <h2>How This Role Typically Functions</h2>
    <p>
        This role typically involves coordinating people, processes, and resources
        to ensure organisational objectives are met. Individuals in this position
        are often responsible for oversight, decision-making, and aligning teams
        with strategic or operational priorities.
    </p>
</section>
""",

    "specialist": """
<section>
    <h2>How This Role Typically Functions</h2>
    <p>
        This role typically focuses on applying specialised skills or expertise to
        specific tasks or functions within an organisation. Individuals in this
        position often work alongside managers and cross-functional teams to deliver
        practical or technical outcomes.
    </p>
</section>
""",

    "advisory": """
<section>
    <h2>How This Role Typically Functions</h2>
    <p>
        This role typically exists to provide guidance, analysis, or professional
        judgement in support of organisational decisions. Individuals in this
        position often engage with stakeholders across departments and contribute
        to planning, compliance, or strategic initiatives.
    </p>
</section>
""",

    "operational": """
<section>
    <h2>How This Role Typically Functions</h2>
    <p>
        This role typically supports day-to-day organisational operations by managing
        processes, information, or coordination activities. Individuals in this
        position help ensure continuity, efficiency, and effective communication
        across teams.
    </p>
</section>
""",

    "commercial": """
<section>
    <h2>How This Role Typically Functions</h2>
    <p>
        This role typically focuses on driving organisational growth through customer
        engagement, relationship management, or market-facing activities. Individuals
        in this position often work closely with internal teams to align offerings
        with market demand.
    </p>
</section>
""",
}

# =====================================================
# ROLE → ROLE TYPE MAPPING
# =====================================================

ROLE_TYPE_MAP = {
    # Managerial
    "it-manager": "managerial",
    "operations-manager": "managerial",
    "project-manager": "managerial",
    "release-manager": "managerial",

    # Specialist / Practitioner
    "ux-designer": "specialist",
    "business-intelligence-analyst": "specialist",
    "data-analyst": "specialist",
    "electrician": "specialist",

    # Advisory
    "consultant": "advisory",
    "hr-partner": "advisory",
    "legal-advisor": "advisory",

    # Operational / Support
    "administrator": "operational",
    "office-coordinator": "operational",

    # Commercial
    "digital-marketing-specialist": "commercial",
    "sales-manager": "commercial",
    "business-development-manager": "commercial",
}

DEFAULT_ROLE_TYPE = "specialist"

# =====================================================
# ENHANCER
# =====================================================

def enhance_people_pages(limit_roles=None):
    enhanced = 0
    skipped = 0

    for role_dir in PEOPLE_ROOT.iterdir():
        if not role_dir.is_dir():
            continue

        role_slug = role_dir.name
        role_title = role_slug.replace("-", " ").title()

        if limit_roles and role_slug not in limit_roles:
            continue

        role_type = ROLE_TYPE_MAP.get(role_slug, DEFAULT_ROLE_TYPE)
        quality_block = ROLE_TYPE_BLOCKS[role_type].strip()

        for country_dir in role_dir.iterdir():
            if not country_dir.is_dir():
                continue

            country_slug = country_dir.name
            country_name = country_slug.replace("-", " ").title()

            page_file = country_dir / "index.html"
            if not page_file.exists():
                continue

            existing_html = page_file.read_text(encoding="utf-8")

            if ENHANCEMENT_MARKER in existing_html:
                skipped += 1
                continue

            archetype = random.choice(ARCHETYPES)
            middle = archetype[1:-3]
            random.shuffle(middle)

            ordered_blocks = (
                [archetype[0]] +
                ["__QUALITY__"] +
                middle +
                archetype[-3:]
            )

            sections = []
            for block in ordered_blocks:
                if block == "__QUALITY__":
                    sections.append(quality_block)
                else:
                    sections.append(BLOCKS[block])

            content_html = "\n\n".join(sections)

            title = f"{role_title}s in {country_name}"

            rendered = (
                base_html
                .replace("{{PAGE_TITLE}}", title)
                .replace("{{H1_TITLE}}", title)
                .replace(
                    "{{META_DESCRIPTION}}",
                    f"Learn what {role_title}s do in {country_name}, including typical responsibilities and work environments."
                )
                .replace(
                    "{{CANONICAL_URL}}",
                    f"{SITE_BASE_URL}/people/{role_slug}/{country_slug}/"
                )
                .replace("{{CONTENT_BLOCKS}}", content_html)
                .replace("{{ROLE_TITLE}}", role_title)
                .replace("{{ROLE_SLUG}}", role_slug)
                .replace("{{COUNTRY_NAME}}", country_name)
                .replace("{{COUNTRY_SLUG}}", country_slug)
            )

            rendered = ENHANCEMENT_MARKER + "\n" + rendered
            page_file.write_text(rendered, encoding="utf-8")
            enhanced += 1

    print(f"✔ PEOPLE pages enhanced: {enhanced}")
    print(f"↷ PEOPLE pages skipped (already enhanced): {skipped}")

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    enhance_people_pages(limit_roles=None)
