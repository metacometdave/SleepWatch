#!/usr/bin/env python3
"""
Create a simple black lightning bolt icon for the menu bar.
Generates a 22x22 PNG with transparency.
"""
from PIL import Image, ImageDraw

# Create a 22x22 image with transparent background
size = 22
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw a simple lightning bolt shape
# Lightning bolt coordinates (simplified geometric shape)
lightning = [
    (11, 2),   # Top point
    (13, 10),  # Right upper
    (9, 10),   # Inner upper
    (11, 20),  # Bottom point
    (9, 12),   # Left lower
    (13, 12),  # Inner lower
    (11, 2)    # Back to top
]

# Draw filled polygon in black
draw.polygon(lightning, fill=(0, 0, 0, 255))

# Save as PNG
img.save('/Users/dhunt/code/Sleepwatch/icon.png')
print("Icon created: icon.png")
