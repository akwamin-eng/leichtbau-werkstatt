import glob

html_files = glob.glob('*.html')

anti_inspect_script = """
    <!-- Anti-Inspection & Asset Protection -->
    <script>
        document.addEventListener('contextmenu', event => event.preventDefault());
        document.onkeydown = function (e) {
            // Disable F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
            if (
                event.keyCode == 123 ||
                (e.ctrlKey && e.shiftKey && e.keyCode == 73) ||
                (e.ctrlKey && e.shiftKey && e.keyCode == 74) ||
                (e.ctrlKey && e.keyCode == 85) ||
                (e.metaKey && e.altKey && e.keyCode == 73) || // Mac Cmd+Option+I
                (e.metaKey && e.altKey && e.keyCode == 74) || // Mac Cmd+Option+J
                (e.metaKey && e.keyCode == 85) // Mac Cmd+U
            ) {
                return false;
            }
        };
    </script>
</body>"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if we already injected it
    if '<!-- Anti-Inspection' not in html:
        html = html.replace('</body>', anti_inspect_script)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Hardened {file}")

