import os
import glob
import re

html_files = glob.glob('pages/*.html')

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update nav-mobile to 1024px to match 'lg' and user requirement
    new_content = re.sub(r"'nav-mobile':\s*'915px'", "'nav-mobile': '1024px'", content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated nav-mobile breakpoint in {file_path}")

print("Done.")
