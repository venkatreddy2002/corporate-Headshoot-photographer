import os
import re

pages = 'pages'
for f in sorted(os.listdir(pages)):
    if not f.endswith('.html'):
        continue
    content = open(os.path.join(pages, f), encoding='utf-8').read()
    matches = re.findall(r'<section[^>]+class="([^"]+)"', content)
    for m in matches:
        classes = m.split()
        has_px = any(c in classes for c in ['px-6','px-4','px-8','px-10','px-12','px-16','px-20'])
        has_lg_px = any('lg:px' in c or 'md:px' in c for c in classes)
        if has_px and has_lg_px:
            print(f'{f}: {m[:120]}')
            break
