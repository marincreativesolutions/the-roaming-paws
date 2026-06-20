import os, re

base = r'E:\Antigravity\kdp-book-generator-amazon\website\the-roaming-paws'
pages = ['index.html', 'about.html', 'books.html', 'contact.html', 'shop.html', 'thankyou.html']

for page in pages:
    path = os.path.join(base, page)
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'href=["\']([^"\']*\.html[^"\']*)["\']', content)
    if matches:
        print(f'--- {page} ---')
        for m in sorted(set(matches)):
            print(f'  {m}')
