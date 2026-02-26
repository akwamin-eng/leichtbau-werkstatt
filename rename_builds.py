import glob
import re

files = glob.glob('*.html')
for file in files:
    with open(file, 'r') as f:
        content = f.read()
        
    # Replace id="builds" in index.html
    content = content.replace('id="builds"', 'id="services"')
    content = content.replace('href="#builds"', 'href="#services"')
    content = content.replace('href="index.html#builds"', 'href="index.html#services"')
    
    # Navigation link text >Builds< to >Services<
    content = re.sub(r'>\s*Builds\s*<', '>Services<', content)
    
    with open(file, 'w') as f:
        f.write(content)

print("Renamed Builds to Services across HTML files.")
