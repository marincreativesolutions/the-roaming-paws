import os, re

BASE = r'E:\Antigravity\kdp-book-generator-amazon\website\the-roaming-paws'

for root, dirs, files in os.walk(BASE):
    # Skip .git and backup files
    dirs[:] = [d for d in dirs if d != '.git']
    for fname in files:
        if not fname.endswith('.html') or fname.endswith('.bak'):
            continue
        path = os.path.join(root, fname)
        rel = os.path.relpath(path, BASE)
        with open(path, encoding='utf-8') as f:
            content = f.read()
        matches = re.findall(r'href=["\']([^"\']*\.html[^"\']*)["\']', content)
        if matches:
            print(f'--- {rel} ---')
            for m in sorted(set(matches)):
                print(f'  {m}')
