import os
import re

pattern = r'max-lg:rounded-none max-lg:shadow-sm max-lg:p-4'

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if re.search(pattern, content):
                    print(f"Found in {filepath}")
            except Exception as e:
                pass
