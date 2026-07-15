import os
from PIL import Image, ImageDraw, ImageFont

def make_gradient_image(width, height, start_color, end_color):
    """Creates a horizontal linear gradient image."""
    base = Image.new("RGBA", (width, height), start_color)
    top = Image.new("RGBA", (width, height), end_color)
    mask = Image.new("L", (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (x / width)))
    mask.putdata(mask_data)
    return Image.composite(top, base, mask)

def generate_logo():
    # Logo: 200x200 gradient square with rounded-like circle and initials "SCAI"
    os.makedirs("assets", exist_ok=True)
    logo_path = os.path.join("assets", "logo.png")
    
    img = make_gradient_image(200, 200, (99, 102, 241, 255), (236, 72, 153, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw circle border
    draw.ellipse([20, 20, 180, 180], outline=(255, 255, 255, 120), width=8)
    
    # Write Text
    # Use default font since custom fonts might not be present on system
    text = "SCAI"
    # To be safe, draw large text using a vector fallback or simple text
    draw.text((100, 100), text, fill=(255, 255, 255, 255), anchor="mm", font_size=40)
    img.save(logo_path)
    print(f"Generated {logo_path}")

def generate_banner():
    # Banner: 1200x300 horizontal gradient
    banner_path = os.path.join("assets", "banner.png")
    
    img = make_gradient_image(1200, 300, (15, 23, 42, 255), (76, 29, 149, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw simple design shapes
    draw.polygon([(800, 0), (1200, 0), (1200, 300), (950, 300)], fill=(99, 102, 241, 40))
    draw.polygon([(900, 0), (1200, 0), (1200, 300), (1050, 300)], fill=(236, 72, 153, 40))
    
    text = "Smart Campus AI"
    draw.text((600, 150), text, fill=(255, 255, 255, 255), anchor="mm", font_size=60)
    
    subtext = "AI-Driven Education & Operations Command"
    draw.text((600, 200), subtext, fill=(248, 250, 252, 180), anchor="mm", font_size=24)
    
    img.save(banner_path)
    print(f"Generated {banner_path}")

def generate_avatar():
    # Avatar: 150x150 circular profile shape
    avatar_path = os.path.join("assets", "avatar.png")
    
    img = Image.new("RGBA", (150, 150), (30, 41, 59, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw grey circular background for avatar
    draw.ellipse([10, 10, 140, 140], fill=(71, 85, 105, 255))
    
    # Draw head
    draw.ellipse([55, 35, 95, 75], fill=(241, 245, 249, 255))
    # Draw body
    draw.chord([30, 85, 120, 160], 180, 360, fill=(241, 245, 249, 255))
    
    img.save(avatar_path)
    print(f"Generated {avatar_path}")

if __name__ == "__main__":
    generate_logo()
    generate_banner()
    generate_avatar()
