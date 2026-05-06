"""
Sitemap Generator -- run after generate.py
Usage: python sitemap.py
Output: output/sitemap.xml
"""

from pathlib import Path
from datetime import date
from cities import CITIES
from generate import make_slug

SITE_URL = "https://www.kansascityhvacpros.com"
OUTPUT_DIR = Path("output")
TODAY = date.today().isoformat()

urls = [
    ("", "1.0", "weekly"),
    ("service-areas/", "0.8", "monthly"),
]

for c in CITIES:
    slug = make_slug(c["name"], c["state"])
    urls.append((f"{slug}/", "0.9", "monthly"))

xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

for path, priority, freq in urls:
    xml_lines += [
        "  <url>",
        f"    <loc>{SITE_URL}/{path}</loc>",
        f"    <lastmod>{TODAY}</lastmod>",
        f"    <changefreq>{freq}</changefreq>",
        f"    <priority>{priority}</priority>",
        "  </url>",
    ]

xml_lines.append("</urlset>")

OUTPUT_DIR.mkdir(exist_ok=True)
sitemap_path = OUTPUT_DIR / "sitemap.xml"
sitemap_path.write_text("\n".join(xml_lines), encoding="utf-8")
print(f"OK  sitemap.xml generated with {len(urls)} URLs -> {sitemap_path.resolve()}")
print(f"   Submit to: https://search.google.com/search-console")