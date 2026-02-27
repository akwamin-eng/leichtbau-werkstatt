import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BASE_URL = "https://www.leichtbauwerkstatt.com"
HTML_DIR = "/Users/alexanderkwamin/.gemini/antigravity/scratch/leichtbau-werkstatt"

pages = {
    "index.html": {"title": "Leichtbau Werkstatt - Redefining the Analog Driving Experience", "priority": "1.0"},
    "assembly.html": {"title": "Engine & Gearbox Assembly - Leichtbau Werkstatt", "priority": "0.8"},
    "collection-gallery.html": {"title": "Collection & Gallery - Leichtbau Werkstatt", "priority": "0.8"},
    "contact.html": {"title": "Contact Us - Leichtbau Werkstatt", "priority": "0.7"},
    "events.html": {"title": "Events & Track Days - Leichtbau Werkstatt", "priority": "0.7"},
    "fabrication.html": {"title": "Custom Fabrication & Motorsport - Leichtbau Werkstatt", "priority": "0.8"},
    "parts.html": {"title": "High-Performance Parts - Leichtbau Werkstatt", "priority": "0.8"},
    "race-prep.html": {"title": "Race Prep & Maintenance - Leichtbau Werkstatt", "priority": "0.8"},
}

def generate_sitemap(pages):
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for filename, info in pages.items():
        url = BASE_URL + ("/" if filename == "index.html" else f"/{filename.replace('.html', '')}")
        sitemap_content += '  <url>\n'
        sitemap_content += f'    <loc>{url}</loc>\n'
        sitemap_content += '    <changefreq>weekly</changefreq>\n'
        sitemap_content += f'    <priority>{info["priority"]}</priority>\n'
        sitemap_content += '  </url>\n'
        
    sitemap_content += '</urlset>'
    
    with open(os.path.join(HTML_DIR, "sitemap.xml"), "w") as f:
        f.write(sitemap_content)
    print("Generated sitemap.xml")

def generate_robots():
    robots_content = "User-agent: *\nAllow: /\n\n"
    robots_content += f"Sitemap: {BASE_URL}/sitemap.xml\n"
    
    with open(os.path.join(HTML_DIR, "robots.txt"), "w") as f:
        f.write(robots_content)
    print("Generated robots.txt")

if __name__ == "__main__":
    generate_sitemap(pages)
    generate_robots()
