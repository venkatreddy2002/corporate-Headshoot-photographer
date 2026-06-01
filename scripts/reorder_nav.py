import os
import re

def reorder_navbar(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the desktop nav section
    nav_pattern = re.compile(r'(<nav class="hidden nav-mobile:flex items-center gap-3 lg:gap-4">)(.*?)(</nav>)', re.DOTALL)
    match = nav_pattern.search(content)
    if not match:
        return False

    prefix = match.group(1)
    nav_inner = match.group(2)
    suffix = match.group(3)

    # Extract items
    # Items can be <div class="relative">...</div> or <a ...>...</a>
    # We need to be careful with nesting.
    
    # Let's find the specific elements by their classes
    home_item = re.search(r'<div class="relative">.*?nav-home.*?</div>\s*</div>', nav_inner, re.DOTALL)
    if not home_item:
        # Fallback if structure is slightly different
        home_item = re.search(r'<div class="relative">.*?nav-home.*?</div>', nav_inner, re.DOTALL)
    
    about_item = re.search(r'<a[^>]*class="[^"]*nav-about[^"]*"[^>]*>.*?</a>', nav_inner, re.DOTALL)
    services_item = re.search(r'<a[^>]*class="[^"]*nav-services[^"]*"[^>]*>.*?</a>', nav_inner, re.DOTALL)
    blog_item = re.search(r'<a[^>]*class="[^"]*nav-blog[^"]*"[^>]*>.*?</a>', nav_inner, re.DOTALL)
    gallery_item = re.search(r'<a[^>]*class="[^"]*nav-gallery[^"]*"[^>]*>.*?</a>', nav_inner, re.DOTALL)
    contact_item = re.search(r'<a[^>]*class="[^"]*nav-contact[^"]*"[^>]*>.*?</a>', nav_inner, re.DOTALL)
    
    dashboard_item = re.search(r'<div class="relative">.*?nav-dashboard.*?</div>\s*</div>', nav_inner, re.DOTALL)
    if not dashboard_item:
        dashboard_item = re.search(r'<div class="relative">.*?nav-dashboard.*?</div>', nav_inner, re.DOTALL)

    if not all([home_item, about_item, services_item, blog_item, gallery_item, contact_item, dashboard_item]):
        print(f"Skipping {file_path}: Could not find all nav items.")
        return False

    # Get the exact strings
    home_str = home_item.group(0).strip()
    about_str = about_item.group(0).strip()
    services_str = services_item.group(0).strip()
    blog_str = blog_item.group(0).strip()
    gallery_str = gallery_item.group(0).strip()
    contact_str = contact_item.group(0).strip()
    dashboard_str = dashboard_item.group(0).strip()

    # Build new inner content with proper spacing
    new_inner = f"\n\t\t{home_str}\n\t\t{about_str}\n\t\t{services_str}\n\t\t{blog_str}\n\t\t{gallery_str}\n\t\t{contact_str}\n\t\t{dashboard_str}\n\t"

    new_nav = prefix + new_inner + suffix
    new_content = content[:match.start()] + new_nav + content[match.end():]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

pages_dir = r"c:\Users\sivak\Downloads\Photographer\photographer\pages"
files = [os.path.join(pages_dir, f) for f in os.listdir(pages_dir) if f.endswith('.html')]

success_count = 0
for f in files:
    if reorder_navbar(f):
        success_count += 1

print(f"Successfully reordered navbar in {success_count} files.")
