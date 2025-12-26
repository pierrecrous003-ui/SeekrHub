from pathlib import Path

# =========================
# CONFIG
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "people-role-country.html"
OUTPUT_ROOT = BASE_DIR / "people"

SITE_BASE_URL = "https://seekrhub.pro"

# =========================
# PAGE DATA
# =========================

ROLES = [
    {"slug": "data-analyst", "title": "Data Analyst"},
    {"slug": "software-engineer", "title": "Software Engineer"},
    {"slug": "web-developer", "title": "Web Developer"},
    {"slug": "product-manager", "title": "Product Manager"},
    {"slug": "project-manager", "title": "Project Manager"},
    {"slug": "business-analyst", "title": "Business Analyst"},
    {"slug": "systems-analyst", "title": "Systems Analyst"},
    {"slug": "it-consultant", "title": "IT Consultant"},
    {"slug": "network-engineer", "title": "Network Engineer"},
    {"slug": "cloud-engineer", "title": "Cloud Engineer"},
    {"slug": "devops-engineer", "title": "DevOps Engineer"},
    {"slug": "cybersecurity-analyst", "title": "Cybersecurity Analyst"},
    {"slug": "ux-designer", "title": "UX Designer"},
    {"slug": "ui-designer", "title": "UI Designer"},
    {"slug": "qa-engineer", "title": "QA Engineer"},
    {"slug": "database-administrator", "title": "Database Administrator"},
    {"slug": "solutions-architect", "title": "Solutions Architect"},
    {"slug": "technical-support-specialist", "title": "Technical Support Specialist"},
    {"slug": "it-manager", "title": "IT Manager"},
    {"slug": "digital-marketing-specialist", "title": "Digital Marketing Specialist"},
]

# =========================
# PHASE 2 COUNTRIES
# =========================

COUNTRIES = [
    {"slug": "australia", "name": "Australia"},
    {"slug": "new-zealand", "name": "New Zealand"},
    {"slug": "ireland", "name": "Ireland"},
    {"slug": "singapore", "name": "Singapore"},
    {"slug": "netherlands", "name": "Netherlands"},
    {"slug": "sweden", "name": "Sweden"},
    {"slug": "norway", "name": "Norway"},
    {"slug": "denmark", "name": "Denmark"},
    {"slug": "united-arab-emirates", "name": "United Arab Emirates"},
    {"slug": "south-africa", "name": "South Africa"},
]

# =========================
# SEMANTIC VARIATION MAPS
# (unchanged – safe defaults apply)
# =========================

COUNTRY_CONTEXT = {}
ROLE_SKILLS = {}
ROLE_INDUSTRY_LINE = {}

# =========================
# INTERNAL LINK HELPERS
# =========================

def build_related_role_links(role_slug, role_title, current_country_slug):
    links = []
    for country in COUNTRIES:
        if country["slug"] != current_country_slug:
            links.append(
                f'<li><a href="/people/{role_slug}/{country["slug"]}/">'
                f'{role_title}s in {country["name"]}</a></li>'
            )
    return "".join(links[:4])

def build_related_country_links(country_slug, country_name, current_role_slug):
    links = []
    for role in ROLES:
        if role["slug"] != current_role_slug:
            links.append(
                f'<li><a href="/people/{role["slug"]}/{country_slug}/">'
                f'{role["title"]}s in {country_name}</a></li>'
            )
    return "".join(links[:4])

# =========================
# GENERATOR
# =========================

def generate_pages():
    template_html = TEMPLATE_PATH.read_text(encoding="utf-8")

    for role in ROLES:
        for country in COUNTRIES:
            role_slug = role["slug"]
            role_title = role["title"]
            country_slug = country["slug"]
            country_name = country["name"]

            output_dir = OUTPUT_ROOT / role_slug / country_slug
            output_dir.mkdir(parents=True, exist_ok=True)

            canonical_url = f"{SITE_BASE_URL}/people/{role_slug}/{country_slug}/"

            page_html = (
                template_html
                .replace("{{ROLE_TITLE}}", role_title)
                .replace("{{ROLE_SLUG}}", role_slug)
                .replace("{{COUNTRY_NAME}}", country_name)
                .replace("{{COUNTRY_SLUG}}", country_slug)
                .replace("{{CANONICAL_URL}}", canonical_url)
            )

            (output_dir / "index.html").write_text(page_html, encoding="utf-8")

    print("✔ Phase 2 pages generated (countries only)")

if __name__ == "__main__":
    generate_pages()
