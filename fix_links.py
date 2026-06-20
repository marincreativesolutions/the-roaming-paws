"""Fix remaining .html links in books/laketahoe/index.html and books/yosemite/index.html"""
import os, re

BASE = r'E:\Antigravity\kdp-book-generator-amazon\website\the-roaming-paws'

# All link replacements needed (old -> new)
LINK_MAP = {
    # Root-relative links (from top-level pages)
    'index.html':               '/',
    'about.html':               '/about',
    'books.html':               '/books',
    'books/laketahoe.html':     '/books/laketahoe',
    'books/yosemite.html':      '/books/yosemite',
    'contact.html':             '/contact',
    'shop.html':                '/shop',
    'thankyou.html':            '/thankyou',
    # Relative links from books/ depth (books/*.html originals)
    '../index.html':            '/',
    '../about.html':            '/about',
    '../books.html':            '/books',
    '../contact.html':          '/contact',
    '../shop.html':             '/shop',
    '../thankyou.html':         '/thankyou',
    # Sibling links within books/ (laketahoe.html, yosemite.html)
    'laketahoe.html':           '/books/laketahoe',
    'yosemite.html':            '/books/yosemite',
    # In case of ../books/ relative links
    '../books/laketahoe.html':  '/books/laketahoe',
    '../books/yosemite.html':   '/books/yosemite',
}

def fix_links(content):
    for old, new in LINK_MAP.items():
        content = re.sub(
            r'(href=["\'])' + re.escape(old) + r'(["\'])',
            r'\g<1>' + new + r'\g<2>',
            content
        )
    return content

# Apply to ALL html files (catches everything)
fixed = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d != '.git']
    for fname in files:
        if not fname.endswith('.html') or fname.endswith('.bak'):
            continue
        path = os.path.join(root, fname)
        with open(path, encoding='utf-8') as f:
            original = f.read()
        updated = fix_links(original)
        if updated != original:
            with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
                f.write(updated)
            rel = os.path.relpath(path, BASE)
            fixed.append(rel)
            print(f'FIXED: {rel}')

if not fixed:
    print('Nothing needed fixing.')
else:
    print(f'\nFixed {len(fixed)} file(s).')
