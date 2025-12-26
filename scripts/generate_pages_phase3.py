from pathlib import Path

# =========================
# CONFIG
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "people-role-country.html"
OUTPUT_ROOT = BASE_DIR / "people"

SITE_BASE_URL = "https://seekrhub.pro"

# =========================
# PHASE 3 ROLES (NEW ONLY)
# =========================

ROLES = [
    {"slug": "frontend-developer", "title": "Frontend Developer"},
    {"slug": "backend-developer", "title": "Backend Developer"},
    {"slug": "full-stack-developer", "title": "Full Stack Developer"},
    {"slug": "machine-learning-engineer", "title": "Machine Learning Engineer"},
    {"slug": "data-scientist", "title": "Data Scientist"},
    {"slug": "ai-engineer", "title": "AI Engineer"},
    {"slug": "site-reliability-engineer", "title": "Site Reliability Engineer"},
    {"slug": "platform-engineer", "title": "Platform Engineer"},
    {"slug": "enterprise-architect", "title": "Enterprise Architect"},
    {"slug": "scrum-master", "title": "Scrum Master"},
    {"slug": "technical-product-manager", "title": "Technical Product Manager"},
    {"slug": "growth-marketing-manager", "title": "Growth Marketing Manager"},
    {"slug": "seo-specialist", "title": "SEO Specialist"},
    {"slug": "salesforce-developer", "title": "Salesforce Developer"},
    {"slug": "data-engineer", "title": "Data Engineer"},
    {"slug": "business-intelligence-analyst", "title": "Business Intelligence Analyst"},
]

# =========================
# COUNTRIES (PHASE 1 + 2 COMBINED)
# =========================

COUNTRIES = [
    {"slug": "united-states", "name": "United States"},
    {"slug": "canada", "name": "Canada"},
    {"slug": "united-kingdom", "name": "United Kingdom"},
    {"slug": "germany", "name": "Germany"},
    {"slug": "france", "name": "France"},
    {"slug": "italy", "name": "Italy"},
    {"slug": "japan", "name": "Japan"},
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

    print("✔ Phase 3 pages generated (new roles, all existing countries)")

if __name__ == "__main__":
    generate_pages()
