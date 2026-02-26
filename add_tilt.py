import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add tilt library to head
if 'vanilla-tilt' not in html:
    html = html.replace('</head>', '    <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.1/vanilla-tilt.min.js"></script>\n</head>')

# Add data-tilt attributes to the service cards, and a glare effect
def add_tilt(match):
    original = match.group(0)
    # Check if we already added it
    if 'data-tilt' in original:
        return original
    
    # We add the tilt attributes to the <a> tag
    new_tag = original.replace('class="', 'data-tilt data-tilt-max="5" data-tilt-speed="400" data-tilt-glare data-tilt-max-glare="0.2" class="')
    return new_tag

# Target the three specific cards on the homepage (Fabrication, Race Prep, Assembly)
html = re.sub(r'<a href="fabrication\.html" class="flex flex-col[^>]*>', add_tilt, html)
html = re.sub(r'<a href="race-prep\.html" class="flex flex-col[^>]*>', add_tilt, html)
html = re.sub(r'<a href="assembly\.html" class="flex flex-col[^>]*>', add_tilt, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied 3D tilt hover effects to service cards.")
