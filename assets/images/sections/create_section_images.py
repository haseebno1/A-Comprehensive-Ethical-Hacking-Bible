#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

# Directory paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = CURRENT_DIR

# Create section badge images with cyberpunk style
def create_section_badge(text, filename, color=(255, 0, 0), size=(400, 100)):
    # Create base image with transparent background
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw cyberpunk-style background
    for i in range(0, size[0], 4):
        draw.line([(i, 0), (i, size[1])], fill=(color[0]//4, color[1]//4, color[2]//4, 50), width=1)
    
    for i in range(0, size[1], 4):
        draw.line([(0, i), (size[0], i)], fill=(color[0]//4, color[1]//4, color[2]//4, 50), width=1)
    
    # Draw border
    border_width = 3
    draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], outline=color, width=border_width)
    
    # Add diagonal lines in corners
    corner_size = 20
    draw.line([(0, 0), (corner_size, corner_size)], fill=color, width=2)
    draw.line([(size[0], 0), (size[0]-corner_size, corner_size)], fill=color, width=2)
    draw.line([(0, size[1]), (corner_size, size[1]-corner_size)], fill=color, width=2)
    draw.line([(size[0], size[1]), (size[0]-corner_size, size[1]-corner_size)], fill=color, width=2)
    
    # Add text
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    
    # Get text size
    text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (200, 40)
    
    # Position text in center
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Draw text shadow
    shadow_offset = 2
    draw.text((position[0] + shadow_offset, position[1] + shadow_offset), text, fill=(0, 0, 0, 180), font=font)
    
    # Draw main text
    draw.text(position, text, fill=color, font=font)
    
    # Add some noise/glitch effect
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if i % 20 == 0 or j % 40 == 0:
                if pixels[i, j][3] > 0:  # If not fully transparent
                    r, g, b, a = pixels[i, j]
                    pixels[i, j] = (min(r + 50, 255), g, b, a)
    
    # Save the image
    img.save(os.path.join(OUTPUT_DIR, filename))
    print(f"Created {filename}")

# Create section images
sections = [
    ("LEARNING PATHS", "learning_paths.png", (255, 0, 0)),
    ("SCRIPTS & TOOLS", "scripts_tools.png", (255, 50, 50)),
    ("OSINT TECHNIQUES", "osint.png", (255, 100, 0)),
    ("DEFENSIVE SECURITY", "defensive.png", (0, 200, 100)),
    ("BUG BOUNTY", "bug_bounty.png", (255, 200, 0)),
    ("CERTIFICATIONS", "certifications.png", (0, 100, 255))
]

# Create all section badges
for section_text, filename, color in sections:
    create_section_badge(section_text, filename, color)

print("All section images created successfully!")
