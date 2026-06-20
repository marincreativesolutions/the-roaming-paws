"""
Restructures the website to use clean URLs via folder/index.html pattern.
All internal .html links and image paths are updated.
Original files are preserved with a .bak extension.
"""
import os, re, shutil

BASE = r'E:\Antigravity\kdp-book-generator-amazon\website\the-roaming-paws'

# Map: old path (relative to BASE) -> new path (relative to BASE)
FILE_MAP = {
    'about.html':            'about/index.html',
    'books.html':            'books/index.html',
    'books/laketahoe.html':  'books/laketahoe/index.html',
    'books/yosemite.html':   'books/yosemite/index.html',
    'contact.html':          'contact/index.html',
    'shop.html':             'shop/index.html',
    'thankyou.html':         'thankyou/index.html',
    'index.html':            'index.html',  # stays, just update links
}

# Map: old href value -> new href value
LINK_MAP = {
    'index.html':               '/',
    'about.html':               '/about',
    'books.html':               '/books',
    'books/laketahoe.html':     '/books/laketahoe',
    'books/yosemite.html':      '/books/yosemite',
    'contact.html':             '/contact',
    'shop.html':                '/shop',
    'thankyou.html':            '/thankyou',
}

def fix_links(content):
    """Replace all .html hrefs with clean URLs."""
    for old, new in LINK_MAP.items():
        # Match href="old" or href='old'
        content = re.sub(
            r'(href=["\'])' + re.escape(old) + r'(["\'])',
            r'\g<1>' + new + r'\g<2>',
            content
        )
    return content

def fix_image_paths(content, depth):
    """Convert relative image paths to root-relative /images/..."""
    # depth=0: root level (index.html) — images/ is already correct, convert to /images/
    # depth=1: one folder deep (about/, books/, etc.)
    # depth=2: two folders deep (books/laketahoe/, books/yosemite/)
    
    # Convert src="images/..." to src="/images/..."
    content = re.sub(r'(src=["\'])images/', r'\g<1>/images/', content)
    # Convert src="../images/..." to src="/images/..."
    content = re.sub(r'(src=["\'])\.\.\/images/', r'\g<1>/images/', content)
    # Convert src="../../images/..." to src="/images/..."
    content = re.sub(r'(src=["\'])\.\.\/\.\.\/images/', r'\g<1>/images/', content)
    
    return content

def fix_asset_paths(content):
    """Convert other relative asset paths to root-relative."""
    # Any remaining relative paths that aren't external links
    return content

# Process each file
for old_rel, new_rel in FILE_MAP.items():
    old_path = os.path.join(BASE, old_rel)
    new_path = os.path.join(BASE, new_rel)

    if not os.path.exists(old_path):
        print(f'SKIP (not found): {old_rel}')
        continue

    # Read content
    with open(old_path, encoding='utf-8') as f:
        content = f.read()

    # Calculate depth
    depth = new_rel.count('/')

    # Apply fixes
    content = fix_links(content)
    content = fix_image_paths(content, depth)

    if old_rel == new_rel:
        # index.html — overwrite in place
        with open(old_path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(content)
        print(f'UPDATED in place: {old_rel}')
    else:
        # Backup original
        bak_path = old_path + '.bak'
        shutil.copy2(old_path, bak_path)

        # Create new directory if needed
        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        # Write new file
        with open(new_path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(content)

        print(f'CREATED: {new_rel}  (backup: {os.path.basename(bak_path)})')

print('\nDone! Review the new structure, then delete .bak files before pushing.')
