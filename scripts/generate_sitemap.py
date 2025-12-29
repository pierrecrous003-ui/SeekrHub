from pathlib import Path
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
PEOPLE_DIR = BASE_DIR / "people"
SITEMAP_PATH = BASE_DIR / "sitemap.xml"

SITE_BASE_URL = "https://seekrhub.pro"

NOW = datetime.utcnow().strftime("%Y-%m-%d")

# =====================================================
# URL ENTRY BUILDER
# =====================================================

def build_url_entry(loc: str, priority: str) -> str:
    return f"""
    <url>
        <loc>{loc}</loc>
        <lastmod>{NOW}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>{priority}</priority>
    </url>
    """.strip()

# =====================================================
# MAIN SITEMAP GENERATOR
# =====================================================

def generate_sitemap():
    urls = []

    # Homepage
    urls.append(build_url_entry(
        f"{SITE_BASE_URL}/",
        "1.0"
    ))

    # PEOPLE + INSIGHT PAGES
    for index_file in PEOPLE_DIR.rglob("index.html"):
        rel_path = index_file.relative_to(BASE_DIR)
        url_path = "/" + rel_path.as_posix().replace("index.html", "")

        # Determine priority
        if "/insights/" in url_path:
            priority = "0.4"
        else:
            priority = "0.6"

        urls.append(build_url_entry(
            f"{SITE_BASE_URL}{url_path}",
            priority
        ))

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""

    SITEMAP_PATH.write_text(sitemap, encoding="utf-8")
    print(f"✔ sitemap.xml generated at {SITEMAP_PATH}")

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    generate_sitemap()
