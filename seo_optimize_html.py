import os
import glob
from bs4 import BeautifulSoup

HTML_DIR = "/Users/alexanderkwamin/.gemini/antigravity/scratch/leichtbau-werkstatt"
BASE_URL = "https://www.leichtbauwerkstatt.com"

pages_info = {
    "index.html": {"title": "Leichtbau Werkstatt - Redefining the Analog Driving Experience", "desc": "Leichtbau Werkstatt is dedicated to redefining the analog driving experience. Specializing in bespoke engine assembly, race prep, fabrication, and high-performance parts. Vintage soul, modern precision."},
    "assembly.html": {"title": "Engine & Gearbox Assembly - Leichtbau Werkstatt", "desc": "Expert engine and gearbox assembly services. Precision engineering for unmatched reliability and performance."},
    "collection-gallery.html": {"title": "Collection & Gallery - Leichtbau Werkstatt", "desc": "Explore our collection and gallery of custom builds, race cars, and high-performance engineering projects."},
    "contact.html": {"title": "Contact Us - Leichtbau Werkstatt", "desc": "Get in touch with Leichtbau Werkstatt for inquiries about custom builds, engine assembly, race prep, and more."},
    "events.html": {"title": "Events & Track Days - Leichtbau Werkstatt", "desc": "Join Leichtbau Werkstatt at our upcoming events, track days, and motorsport gathering experiences."},
    "fabrication.html": {"title": "Custom Fabrication & Motorsport - Leichtbau Werkstatt", "desc": "Bespoke fabrication services for motorsport applications. From roll cages to custom exhaust systems, built with precision."},
    "parts.html": {"title": "High-Performance Parts - Leichtbau Werkstatt", "desc": "Premium high-performance parts tailored for the ultimate analog driving experience."},
    "race-prep.html": {"title": "Race Prep & Maintenance - Leichtbau Werkstatt", "desc": "Professional race prep and routine maintenance to ensure your vehicle performs at its peak on and off the track."},
    "404.html": {"title": "Page Not Found - Leichtbau Werkstatt", "desc": "The page you are looking for does not exist."},
    "coming-soon.html": {"title": "Coming Soon - Leichtbau Werkstatt", "desc": "Exciting new updates are coming soon to Leichtbau Werkstatt."},
    "event-register.html": {"title": "Register for Event - Leichtbau Werkstatt", "desc": "Register for upcoming track days and events hosted by Leichtbau Werkstatt."},
    "event-success.html": {"title": "Registration Successful - Leichtbau Werkstatt", "desc": "Your event registration was successful."},
    "success-state.html": {"title": "Success - Leichtbau Werkstatt", "desc": "Form submission successful."}
}

def optimize_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    head = soup.head
    if not head:
        print(f"Skipping {filename} (No <head> found)")
        return

    info = pages_info.get(filename, {"title": f"{filename} - Leichtbau Werkstatt", "desc": "Redefining the analog driving experience. Vintage soul, modern precision."})
    
    # 1. Title Tag
    title_tag = head.find('title')
    if title_tag:
        title_tag.string = info["title"]
    else:
        new_title = soup.new_tag('title')
        new_title.string = info["title"]
        head.append(new_title)

    # Helper function to set or replace meta tag
    def set_meta(attrs, content=None):
        # find existing
        search_attrs = attrs.copy()
        if content is not None:
            if 'property' in search_attrs:
                tag = head.find('meta', property=search_attrs['property'])
            elif 'name' in search_attrs:
                tag = head.find('meta', attrs={'name': search_attrs['name']})
            else:
                tag = head.find('meta', attrs=search_attrs)

            if tag:
                tag['content'] = content
            else:
                new_meta = soup.new_tag('meta')
                for k, v in attrs.items():
                    new_meta[k] = v
                new_meta['content'] = content
                head.append(new_meta)

    # 2. Meta Description
    set_meta({'name': 'description'}, info["desc"])

    # 3. Open Graph Tags
    canonical_path = "/" if filename == "index.html" else f"/{filename.replace('.html', '')}"
    full_url = BASE_URL + canonical_path
    
    set_meta({'property': 'og:title'}, info["title"])
    set_meta({'property': 'og:description'}, info["desc"])
    set_meta({'property': 'og:url'}, full_url)
    set_meta({'property': 'og:type'}, "website")
    
    # Ensure og:image is set (checking if missing, if absent, set a generic one)
    og_img = head.find('meta', property='og:image')
    if not og_img:
        set_meta({'property': 'og:image'}, f"{BASE_URL}/assets/og-preview.jpg")

    # 4. Twitter Cards
    set_meta({'name': 'twitter:card'}, "summary_large_image")
    set_meta({'name': 'twitter:title'}, info["title"])
    set_meta({'name': 'twitter:description'}, info["desc"])
    
    tw_img = head.find('meta', attrs={'name': 'twitter:image'})
    if not tw_img:
        set_meta({'name': 'twitter:image'}, f"{BASE_URL}/assets/og-preview.jpg")

    # 5. Canonical link
    canonical_tag = head.find('link', rel='canonical')
    if canonical_tag:
        canonical_tag['href'] = full_url
    else:
        new_canonical = soup.new_tag('link', rel='canonical', href=full_url)
        head.append(new_canonical)

    # 6. Ensure alt attributes on img tags
    for img in soup.find_all('img'):
        if not img.get('alt'):
            # try to make a reasonable alt from the src or title
            alt_text = "Leichtbau Werkstatt image"
            if img.get('src'):
                fname = os.path.basename(img['src']).split('.')[0]
                alt_text = fname.replace('-', ' ').replace('_', ' ').title() + " - Leichtbau Werkstatt"
            img['alt'] = alt_text

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Optimized {filename}")

if __name__ == "__main__":
    for filepath in glob.glob(os.path.join(HTML_DIR, '*.html')):
        filename = os.path.basename(filepath)
        optimize_file(filepath, filename)
