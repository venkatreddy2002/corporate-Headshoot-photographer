import os
import re

patterns = [
    r'w-12 h-6 bg-primary',
    r'w-12 h-6 bg-slate',
    r'w-10 h-5 bg-primary',
    r'w-10 h-5 bg-slate'
]

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                for p in patterns:
                    if re.search(p, content):
                        print(f"Matched pattern '{p}' in {filepath}")
                        break
            except Exception as e:
                pass
