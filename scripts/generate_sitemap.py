from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent.parent
PEOPLE_DIR = BASE_DIR / "people"
SITEMAP_PATH = BASE_DIR / "sitemap.xml"

SITE_BASE_URL = "https://seekrhub.pro"

def generate_sitemap():
    urls = []

    # Always include homepage
    urls.append({
        "loc": f"{SITE_BASE_URL}/",
        "priority": "1.0"
    })

    # Walk /people/**/index.html
    for index_file in PEOPLE_DIR.rglob("index.html"):
        relative_path = index_file.relative_to(BASE_DIR)
        url_path = "/" + str(relative_path.parent).replace("\\", "/") + "/"

        urls.append({
            "loc": f"{SITE_BASE_URL}{url_path}",
            "priority": "0.6"
        })

    today = date.today().isoformat()

    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for url in urls:
        sitemap.extend([
            "  <url>",
            f"    <loc>{url['loc']}</loc>",
            f"    <lastmod>{today}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            f"    <priority>{url['priority']}</priority>",
            "  </url>"
        ])

    sitemap.append("</urlset>")

    SITEMAP_PATH.write_text("\n".join(sitemap), encoding="utf-8")

    print(f"✔ sitemap.xml generated with {len(urls)} URLs")


if __name__ == "__main__":
    generate_sitemap()
