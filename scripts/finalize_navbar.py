import os
import glob
import re

html_files = glob.glob('pages/*.html')

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Hamburger Menu Visibility: Hide on desktop (lg: 1024px)
    # Target id="mobile-menu-trigger"
    # Ensure it has 'lg:hidden' and 'hidden' (for mobile if needed, but usually it's flex on mobile)
    # We want it HIDDEN on desktop screens (>=1024px)
    # Standard: 'flex lg:hidden'
    new_content = re.sub(r'id="mobile-menu-trigger"\s*class="[^"]+"', 'id="mobile-menu-trigger" class="flex lg:hidden h-9 w-9 bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 items-center justify-center text-slate-600 dark:text-slate-400 hover:text-primary transition-colors active:scale-90"', content)

    # 2. Update Main Navigation visibility: Show on desktop (lg: 1024px)
    # Target <nav class="hidden nav-mobile:flex ...">
    new_content = re.sub(r'<nav class="hidden\s+nav-mobile:flex', '<nav class="hidden lg:flex', new_content)

    # 3. Update Book Now and Login buttons visibility
    new_content = re.sub(r'class="hidden\s+nav-mobile:flex\s+items-center\s+justify-center\s+h-9', 'class="hidden lg:flex items-center justify-center h-9', new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Finalized Navbar visibility in {file_path}")

print("Done.")
