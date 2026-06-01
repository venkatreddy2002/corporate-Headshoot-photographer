import os
import glob

html_files = glob.glob('pages/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace 'transition-all duration-500' with 'transition-colors duration-500' in the header
    new_content = content.replace(
        '<header id="navbar" class="bg-transparent fixed top-0 left-0 w-full z-50 transition-all duration-500 full-width">',
        '<header id="navbar" class="bg-transparent fixed top-0 left-0 w-full z-50 transition-colors duration-500 full-width">'
    )
    
    # Also some might have just transition-all without 500, or some other variation, but let's check this exact one first.
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

