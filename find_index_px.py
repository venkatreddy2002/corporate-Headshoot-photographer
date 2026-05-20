import re

with open('pages/index.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if 'md:px' in line or 'lg:px' in line:
        print(f"Line {i}: {line.rstrip()}")
