import os
import glob
import re

html_files = glob.glob('pages/*.html')

# We want to hide the hamburger menu on desktop more robustly
# Current: class="nav-mobile:hidden h-9 w-9 ..."
# New: class="nav-mobile:!hidden hidden h-9 w-9 ..."
# This ensures it's hidden by default and !hidden on desktop (which is redundant but forces it)
# Actually, the standard tailwind is 'hidden lg:block' or similar.
# Since we use 'nav-mobile', we should use 'hidden nav-mobile:!hidden' or similar logic.
# Wait, if we want it ONLY on mobile, it should be 'flex nav-mobile:hidden'.

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Target the mobile menu trigger button
    # Add 'hidden' to the start of the class list and ensure 'nav-mobile:hidden' is present or replaced
    new_content = re.sub(r'id="mobile-menu-trigger"\s*class="nav-mobile:hidden', 'id="mobile-menu-trigger" class="hidden nav-mobile:!hidden', content)
    
    # Also handle the drawer trigger if it has slightly different classes
    new_content = re.sub(r'class="nav-mobile:hidden\s+h-9\s+w-9', 'class="hidden nav-mobile:!hidden h-9 w-9', new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated mobile menu visibility in {file_path}")

print("Done.")
