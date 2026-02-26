import glob
import re

html_files = glob.glob('*.html')

cursor_base = re.compile(r'#cursor\s*\{[^}]*?mix-blend-mode:[^}]*?\}', re.DOTALL)
cursor_hover = re.compile(r'#cursor\.hovered\s*\{[^}]*?\}', re.DOTALL)

new_base = """#cursor {
            position: fixed; top: 0; left: 0; width: 12px; height: 12px;
            background-color: #FF4D00; border-radius: 50%; pointer-events: none;
            z-index: 10000; transform: translate(-50%, -50%);
            transition: width 0.2s, height 0.2s, background-color 0.2s;
            box-shadow: 0 0 10px rgba(255, 77, 0, 0.6);
        }"""
new_hover = """#cursor.hovered {
            width: 60px; height: 60px;
            background-color: rgba(255, 77, 0, 0.15); border: 1px solid rgba(255, 77, 0, 0.5);
            box-shadow: 0 0 20px rgba(255, 77, 0, 0.3);
        }"""

for file in html_files:
    if file == 'index.html':
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if this file has the old cursor style to replace
    if 'mix-blend-mode: difference;' in html and '#cursor {' in html:
        html = cursor_base.sub(new_base, html)
        html = cursor_hover.sub(new_hover, html)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Fixed cursor in {file}")

