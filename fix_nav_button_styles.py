import os
import re

pages_dir = os.path.join(os.path.dirname(__file__), "pages")

# OLD -> NEW replacements
replacements = [
    # Book Now button: remove rounded-lg (already has border-primary which is blue)
    # Also ensure it uses border-2 border-blue-500 (explicit blue border instead of border-primary)
    (
        'h-9 px-4 flex items-center justify-center border border-primary text-primary bg-transparent font-bold uppercase rounded-lg shadow-sm hover:bg-primary/5 transition-all',
        'h-9 px-4 flex items-center justify-center border-2 border-blue-500 text-primary bg-transparent font-bold uppercase text-xs tracking-wide shadow-sm hover:bg-primary/5 transition-all'
    ),
    # Login button: remove rounded-lg
    (
        'h-9 px-4 flex items-center justify-center bg-primary text-white text-xs font-bold uppercase rounded-lg shadow-md shadow-primary/20 hover:brightness-110 transition-all',
        'h-9 px-4 flex items-center justify-center bg-primary text-white text-xs font-bold uppercase shadow-md shadow-primary/20 hover:brightness-110 transition-all'
    ),
]

html_files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]
updated = []

for filename in html_files:
    filepath = os.path.join(pages_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated.append(filename)

print(f"Updated {len(updated)} files:")
for f in updated:
    print(f"  - {f}")
