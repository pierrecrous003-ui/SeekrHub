from pathlib import Path

# =========================
# CONFIG
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_PATH = BASE_DIR / "templates" / "people-role-country.html"
OUTPUT_ROOT = BASE_DIR / "people"

SITE_BASE_URL = "https://seekrhub.pro"

# =========================
# PAGE DATA (20 ROLES)
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
# PAGE DATA (G7 COUNTRIES)
# =========================

COUNTRIES = [
    {"slug": "united-states", "name": "United States"},
    {"slug": "canada", "name": "Canada"},
    {"slug": "united-kingdom", "name": "United Kingdom"},
    {"slug": "germany", "name": "Germany"},
    {"slug": "france", "name": "France"},
    {"slug": "italy", "name": "Italy"},
    {"slug": "japan", "name": "Japan"},
]

# =========================
# GENERATOR
# =========================

def generate_pages():
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")

    template_html = TEMPLATE_PATH.read_text(encoding="utf-8")

    generated_count = 0

    for role in ROLES:
        for country in COUNTRIES:
            role_slug = role["slug"]
            role_title = role["title"]
            country_slug = country["slug"]
            country_name = country["name"]

            # Output path: /people/{role}/{country}/index.html
            output_dir = OUTPUT_ROOT / role_slug / country_slug
            output_dir.mkdir(parents=True, exist_ok=True)

            canonical_url = f"{SITE_BASE_URL}/people/{role_slug}/{country_slug}/"

            page_html = (
                template_html
                .replace("{{ROLE_SLUG}}", role_slug)
                .replace("{{ROLE_TITLE}}", role_title)
                .replace("{{COUNTRY_SLUG}}", country_slug)
                .replace("{{COUNTRY_NAME}}", country_name)
                .replace("{{CANONICAL_URL}}", canonical_url)
            )

            output_file = output_dir / "index.html"
            output_file.write_text(page_html, encoding="utf-8")

            generated_count += 1
            print(f"✔ Generated: {output_file.relative_to(BASE_DIR)}")

    print(f"\nDone. Generated {generated_count} pages.")


if __name__ == "__main__":
    generate_pages()
