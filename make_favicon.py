from PIL import Image, ImageDraw

# Load original logo
img = Image.open('assets/logo-color.png')

# Crop the mark
# The mark is everything roughly above y=300
box = (600, 30, 990, 280)
mark = img.crop(box)

# Create 512x512 canvas with transparent background
size = 512
fav = Image.new('RGBA', (size, size), (255, 255, 255, 0))

# Create a circular mask and draw the orange circle
draw = ImageDraw.Draw(fav)
orange = (255, 77, 0, 255) # #FF4D00
draw.ellipse((0, 0, size, size), fill=orange)

# The mark is white, let's resize it to fit well within the circle
# Find actual bounding box of cropped image just to be tight
mark_bbox = mark.getbbox()
mark = mark.crop(mark_bbox)

mw, mh = mark.size
# Scale to fit inside 380x380
target_w = 360
ratio = target_w / mw
target_h = int(mh * ratio)

if target_h > 360:
    target_h = 360
    ratio = target_h / mh
    target_w = int(mw * ratio)

mark = mark.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Paste centered
paste_x = (size - target_w) // 2
paste_y = (size - target_h) // 2
fav.alpha_composite(mark, (paste_x, paste_y))

fav.save('assets/favicon.png')
# Also save an ico
fav.save('favicon.ico', format='ICO')
print("Successfully created assets/favicon.png and favicon.ico")
