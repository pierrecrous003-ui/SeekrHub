from pathlib import Path

# =========================
# CONFIG
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "people-role-country.html"
OUTPUT_ROOT = BASE_DIR / "people"

SITE_BASE_URL = "https://seekrhub.pro"

# =========================
# PHASE 4 ROLES (NEW ONLY)
# =========================

ROLES = [
    {"slug": "systems-administrator", "title": "Systems Administrator"},
    {"slug": "infrastructure-engineer", "title": "Infrastructure Engineer"},
    {"slug": "it-operations-manager", "title": "IT Operations Manager"},
    {"slug": "network-operations-engineer", "title": "Network Operations Engineer"},
    {"slug": "noc-engineer", "title": "NOC Engineer"},
    {"slug": "endpoint-administrator", "title": "Endpoint Administrator"},

    {"slug": "analytics-engineer", "title": "Analytics Engineer"},
    {"slug": "data-platform-engineer", "title": "Data Platform Engineer"},
    {"slug": "mlops-engineer", "title": "MLOps Engineer"},
    {"slug": "applied-scientist", "title": "Applied Scientist"},
    {"slug": "decision-scientist", "title": "Decision Scientist"},

    {"slug": "information-security-manager", "title": "Information Security Manager"},
    {"slug": "iam-engineer", "title": "IAM Engineer"},
    {"slug": "grc-analyst", "title": "GRC Analyst"},

    {"slug": "program-manager", "title": "Program Manager"},
    {"slug": "delivery-manager", "title": "Delivery Manager"},
    {"slug": "agile-coach", "title": "Agile Coach"},
    {"slug": "release-manager", "title": "Release Manager"},

    {"slug": "revenue-operations-manager", "title": "Revenue Operations Manager"},
    {"slug": "customer-success-manager", "title": "Customer Success Manager"},
    {"slug": "crm-manager", "title": "CRM Manager"},
    {"slug": "marketing-operations-manager", "title": "Marketing Operations Manager"},

    {"slug": "enterprise-applications-manager", "title": "Enterprise Applications Manager"},
    {"slug": "digital-transformation-manager", "title": "Digital Transformation Manager"},
    {"slug": "it-service-delivery-manager", "title": "IT Service Delivery Manager"},
]

# =========================
# COUNTRIES (PHASE 1 + 2)
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
            generated_count += 1

    print(f"✔ Phase 4 pages generated: {generated_count} pages")

if __name__ == "__main__":
    generate_pages()
