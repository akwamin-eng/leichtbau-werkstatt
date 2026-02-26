import glob

og_tags = """    <!-- OpenGraph & Social Meta Tags -->
    <meta property="og:title" content="Leichtbau Werkstatt" />
    <meta property="og:description" content="Redefining the analog driving experience. Vintage soul, modern precision." />
    <meta property="og:image" content="https://www.leichtbauwerkstatt.com/assets/og-preview.jpg" />
    <meta property="og:url" content="https://www.leichtbauwerkstatt.com/" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Leichtbau Werkstatt" />
    <meta name="twitter:description" content="Redefining the analog driving experience. Vintage soul, modern precision." />
    <meta name="twitter:image" content="https://www.leichtbauwerkstatt.com/assets/og-preview.jpg" />
"""

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Avoid duplicating if already present
    if "og:image" not in content and "</head>" in content:
        content = content.replace("</head>", og_tags + "</head>")
        with open(file, 'w') as f:
            f.write(content)
        print(f"Injected OG tags into {file}")
    else:
        print(f"Skipped {file} (tags already exist or no head tag)")
