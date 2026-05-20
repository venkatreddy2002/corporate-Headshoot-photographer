import re, os

pages_dir = 'pages'
for fname in sorted(os.listdir(pages_dir)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(pages_dir, fname)
    with open(fpath, encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if '<section' in line and ('md:px' in line or 'lg:px' in line):
            print(f"{fname}:{i}: {line.strip()[:120]}")
