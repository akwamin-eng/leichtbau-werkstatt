import glob
import re

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r') as f:
        html = f.read()
    
    # 1. Nav logo size
    html = html.replace('class="h-16 w-auto brightness-0 invert"', 'class="h-10 md:h-16 w-auto brightness-0 invert"')

    # 2. Nav background/padding for mobile visibility over text
    # The nav currently usually has "from-black/50 to-transparent" or similar.
    # Let's just make sure it has slightly better background on mobile.
    html = re.sub(
        r'class="fixed w-full z-50 px-6 py-6 flex justify-between items-center',
        'class="fixed w-full z-50 px-6 py-4 md:py-6 flex justify-between items-center bg-black/90 md:bg-transparent backdrop-blur-md md:backdrop-blur-none',
        html
    )

    # 3. Theme Toggle placement (Contrast)
    html = html.replace(
        'class="fixed bottom-12 right-12 z-40',
        'class="fixed bottom-4 right-4 md:bottom-12 md:right-12 z-40'
    )
    
    # 4. Scroll progress bar placement
    html = html.replace(
        'class="fixed bottom-8 left-8 z-40 hidden md:flex',
        'class="fixed bottom-4 left-4 md:bottom-8 md:left-8 z-40 hidden md:flex'
    )

    # index.html specific fixes
    if file == 'index.html':
        # "PERFORMANCE & PERFECTION" heading scale
        html = html.replace('class="text-6xl md:text-9xl', 'class="text-5xl md:text-9xl')
        html = html.replace('translate-y-4 md:translate-x-20', 'translate-y-2 md:translate-x-20')
        
        # "Commission list"
        html = html.replace(
            '<span class="text-neon-orange serif-display italic normal-case">Commission</span>',
            '<span class="text-neon-orange serif-display italic normal-case text-4xl md:text-inherit -ml-1">Commission</span>'
        )
        # "Ethos span" align spacing
        html = html.replace(
            'Raw.<br /><span\n                            class="serif-display italic font-normal text-4xl md:text-6xl text-neon-orange">Analog.</span><br />Unfiltered.',
            'Raw.<br /><span\n                            class="serif-display italic font-normal text-4xl md:text-6xl text-neon-orange -ml-2">Analog.</span><br />Unfiltered.'
        )

    with open(file, 'w') as f:
        f.write(html)

print("Checked CSS responsiveness on mobile.")
