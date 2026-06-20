"""Generate web-optimized preview images for the Yosemite book preview modal."""
from PIL import Image
import os

SRC = r'E:\Antigravity\kdp-book-generator-amazon\v2\book1_illustrations'
DST = r'E:\Antigravity\kdp-book-generator-amazon\website\the-roaming-paws\images\preview\yosemite'
os.makedirs(DST, exist_ok=True)

files = [
    ('cover_new_author.png',       'preview_01_cover.jpg'),
    ('spread_00_hometown.png',     'preview_02_hometown.jpg'),
    ('spread_01_car.png',          'preview_03_car.jpg'),
    ('spread_02_tunnel.png',       'preview_04_tunnel.jpg'),
    ('spread_03_night_comfort.png','preview_05_night.jpg'),
]

for src_name, dst_name in files:
    src = os.path.join(SRC, src_name)
    dst = os.path.join(DST, dst_name)
    img = Image.open(src).convert('RGB')
    # Resize so longest side = 1000px, keep aspect ratio
    img.thumbnail((1000, 1000), Image.LANCZOS)
    img.save(dst, 'JPEG', quality=85, optimize=True)
    kb = round(os.path.getsize(dst) / 1024, 1)
    print(f'{dst_name}: {img.width}x{img.height}px — {kb} KB')

print(f'\nAll 5 preview images saved to: {DST}')
