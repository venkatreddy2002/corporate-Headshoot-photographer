import os
import glob
import re

html_files = [
    'pages/about.html',
    'pages/contact.html',
    'pages/services.html',
    'pages/gallery.html',
    'pages/blog.html',
    'pages/index.html',
    'pages/home2.html'
]

for file_path in html_files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} - not found")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Navbar padding
    # From: px-4 lg:px-6 py-2
    # To:   px-4 lg:px-10 py-3
    content = content.replace('px-4 lg:px-6 py-2', 'px-4 lg:px-10 py-3')

    # 2. Increase Menu Item Size (Global replace of text-[10px] inside navbar)
    # We'll target text-[10px] and change to text-xs
    content = content.replace('text-[10px]', 'text-xs')

    # 3. Fix Mobile Menu Trigger and Text Bug
    # Find the pattern of MOBILE MENU text followed by the button
    # Replace with <!-- MOBILE MENU --> and the correct class
    content = re.sub(r'MOBILE MENU\s*<button id="mobile-menu-trigger"', '<!-- MOBILE MENU -->\n            <button id="mobile-menu-trigger"', content)
    # Ensure it has 'flex lg:hidden'
    content = re.sub(r'id="mobile-menu-trigger"\s*class="[^"]+"', 'id="mobile-menu-trigger" class="flex lg:hidden h-9 w-9 bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 items-center justify-center text-slate-600 dark:text-slate-400 hover:text-primary transition-colors active:scale-90"', content)

    # 4. Enforce Desktop visibility (lg:flex instead of nav-mobile:flex)
    content = content.replace('nav-mobile:flex', 'lg:flex')
    content = content.replace('nav-mobile:hidden', 'lg:hidden')

    # 5. Ensure "Book Now"
    content = content.replace('Book Sessions', 'Book Now')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Global fixes applied to {file_path}")

print("Done.")
