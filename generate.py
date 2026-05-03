"""
KC HVAC Pros — City Page Generator
====================================
Run this script to generate all city landing pages.

Usage:
    python generate.py

Output:
    output/
        index.html          <- copy your main homepage here manually
        service-areas/
            index.html      <- auto-generated service areas hub page
        lees-summit-hvac/
            index.html
        blue-springs-hvac/
            index.html
        ... (one folder per city)

Requirements:
    pip install jinja2

Deploy:
    Push the entire output/ folder to Cloudflare Pages or Netlify.
    Point your domain at it. Done.
"""

import os
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from cities import CITIES


# -- Config --------------------------------------------------------------------

OUTPUT_DIR = Path("output")
TEMPLATE_DIR = Path("templates")
PHONE = "(816) 265-1137"
SITE_URL = "https://www.kansascityhvacpros.com"


# -- Helpers -------------------------------------------------------------------

def make_slug(city_name: str, state: str) -> str:
    """'Lee's Summit', 'MO' -> 'lees-summit-hvac'"""
    name = city_name.lower()
    name = re.sub(r"['\u2019]", "", name)
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = name.strip("-")
    return f"{name}-hvac"


def make_nearby_links(current_city: dict, all_cities: list) -> str:
    """Build pill links to all other cities."""
    links = []
    for c in all_cities:
        if c["name"] == current_city["name"]:
            continue
        slug = make_slug(c["name"], c["state"])
        label = f"{c['name']}, {c['state']}"
        links.append(f'<a class="city-pill" href="/{slug}/">{label}</a>')
    return "\n      ".join(links)


def build_service_areas_hub(all_cities: list, output_dir: Path) -> None:
    """Generate a /service-areas/ hub page listing every city."""
    hub_dir = output_dir / "service-areas"
    hub_dir.mkdir(parents=True, exist_ok=True)

    pills_html = ""
    for c in all_cities:
        slug = make_slug(c["name"], c["state"])
        pills_html += f'<a class="city-pill" href="/{slug}/">{c["name"]}, {c["state"]}</a>\n      '

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>HVAC Service Areas | KC HVAC Pros -- Kansas City Metro</title>
  <meta name="description" content="KC HVAC Pros serves the entire Kansas City metro area including Missouri and Kansas suburbs. Find licensed HVAC contractors in your city." />
  <link rel="canonical" href="{SITE_URL}/service-areas/" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{ --navy: #0d1f3c; --blue: #1a4b8c; --sky: #2d7dd2; --ice: #e8f4fd; --orange: #e85d04; --white: #fff; --gray: #f4f6f8; --text: #1a1f2e; --muted: #6b7280; --border: #dde3ea; }}
    body {{ font-family: 'Barlow', sans-serif; color: var(--text); background: var(--white); }}
    header {{ background: var(--navy); padding: 0 2rem; display: flex; align-items: center; justify-content: space-between; height: 68px; }}
    .logo {{ font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 1.6rem; color: var(--white); text-decoration: none; }}
    .logo span {{ color: var(--orange); }}
    .hero {{ background: linear-gradient(135deg, var(--navy), var(--blue)); padding: 4rem 2rem; text-align: center; }}
    .hero h1 {{ font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 2.8rem; color: var(--white); margin-bottom: 0.8rem; }}
    .hero p {{ color: rgba(255,255,255,0.8); font-size: 1.05rem; max-width: 520px; margin: 0 auto; }}
    .section {{ padding: 4rem 2rem; max-width: 1100px; margin: 0 auto; }}
    .section h2 {{ font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 1.8rem; color: var(--navy); margin-bottom: 1.5rem; }}
    .city-pills {{ display: flex; flex-wrap: wrap; gap: 0.6rem; }}
    .city-pill {{ background: var(--white); border: 1.5px solid var(--border); border-radius: 20px; padding: 0.4rem 1rem; font-size: 0.9rem; font-weight: 500; color: var(--navy); text-decoration: none; transition: all 0.2s; }}
    .city-pill:hover {{ border-color: var(--sky); background: var(--ice); color: var(--blue); }}
    footer {{ background: var(--text); padding: 2rem; text-align: center; color: rgba(255,255,255,0.45); font-size: 0.83rem; }}
    footer a {{ color: rgba(255,255,255,0.4); }}
    footer strong {{ color: rgba(255,255,255,0.7); }}
  </style>
</head>
<body>
<header>
  <a href="/" class="logo">KC <span>HVAC</span> Pros</a>
</header>
<div class="hero">
  <h1>HVAC Service Areas -- Kansas City Metro</h1>
  <p>We connect homeowners across Missouri and Kansas with vetted local HVAC contractors. Find your city below.</p>
</div>
<div class="section">
  <h2>All Service Areas ({len(all_cities)} Cities)</h2>
  <div class="city-pills">
      {pills_html}
  </div>
</div>
<footer>
  <p><strong>KC HVAC Pros</strong> &nbsp;·&nbsp; Serving the Kansas City Metro &nbsp;·&nbsp; <a href="tel:+18162651137">{PHONE}</a></p>
  <p style="margin-top:0.4rem">© 2025 KC HVAC Pros &nbsp;·&nbsp; <a href="/">Home</a></p>
</footer>
</body>
</html>"""

    (hub_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  OK  service-areas/index.html")


# -- Main ----------------------------------------------------------------------

def main():
    print(f"\nKC HVAC Pros -- City Page Generator")
    print(f"   Generating {len(CITIES)} city pages...\n")

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("city.html")

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate service areas hub
    build_service_areas_hub(CITIES, OUTPUT_DIR)

    # Generate each city page
    for city_data in CITIES:
        city  = city_data["name"]
        state = city_data["state"]
        zip_  = city_data["zip"]
        county = city_data["county"]
        slug  = make_slug(city, state)

        # Create output directory for this city
        city_dir = OUTPUT_DIR / slug
        city_dir.mkdir(parents=True, exist_ok=True)

        # Build nearby city links
        nearby_links = make_nearby_links(city_data, CITIES)

        # Render template
        rendered = template.render(
            city=city,
            state=state,
            zip=zip_,
            county=county,
            slug=slug,
            nearby_links=nearby_links,
            phone=PHONE,
            site_url=SITE_URL,
        )

        # Write file
        out_path = city_dir / "index.html"
        out_path.write_text(rendered, encoding="utf-8")
        print(f"  OK  {slug}/index.html  ({city}, {state})")

    print(f"\nDone! {len(CITIES)} city pages + 1 hub page generated.")
    print(f"   Output folder: {OUTPUT_DIR.resolve()}")
    print(f"\nNext steps:")
    print(f"   1. Copy your homepage into output/index.html")
    print(f"   2. Sign up at formspree.io, get your form ID, replace YOUR_FORM_ID in city.html")
    print(f"   3. Push output/ to Cloudflare Pages or Netlify")
    print(f"   4. Point your domain at the deployment")
    print(f"   5. Submit sitemap to Google Search Console\n")


if __name__ == "__main__":
    main()