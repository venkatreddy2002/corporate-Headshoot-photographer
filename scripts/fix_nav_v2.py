import os
import re

def fix_navbar(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the desktop nav block
        nav_start_tag = '<nav class="hidden nav-mobile:flex items-center gap-3 lg:gap-4">'
        nav_end_tag = '</nav>'
        
        start_idx = content.find(nav_start_tag)
        if start_idx == -1: return False
        
        end_idx = content.find(nav_end_tag, start_idx)
        if end_idx == -1: return False
        
        nav_html = content[start_idx : end_idx + len(nav_end_tag)]

        def get_dropdown(class_name):
            # Dropdowns are <div class="relative"> ... class_name ... </div> </div>
            pattern = rf'<div class="relative">[^<]*<a[^>]*{class_name}.*?</div>\s*</div>'
            m = re.search(pattern, nav_html, re.DOTALL)
            return m.group(0).strip() if m else None

        def get_link(class_name):
            pattern = rf'<a[^>]*{class_name}.*?</a>'
            m = re.search(pattern, nav_html, re.DOTALL)
            return m.group(0).strip() if m else None

        home = get_dropdown('nav-home')
        about = get_link('nav-about')
        services = get_link('nav-services')
        blog = get_link('nav-blog')
        gallery = get_link('nav-gallery')
        contact = get_link('nav-contact')
        dashboard = get_dropdown('nav-dashboard')

        if not all([home, about, services, blog, gallery, contact, dashboard]):
            print(f"Skipping {file_path}: missing items ({'home' if not home else ''} {'about' if not about else ''} {'services' if not services else ''} {'blog' if not blog else ''} {'gallery' if not gallery else ''} {'contact' if not contact else ''} {'dashboard' if not dashboard else ''})")
            return False

        # Construct the new nav inner content
        new_inner = f"\n\t\t{home}\n\t\t{about}\n\t\t{services}\n\t\t{blog}\n\t\t{gallery}\n\t\t{contact}\n\t\t{dashboard}\n\t"
        new_nav = nav_start_tag + new_inner + nav_end_tag
        
        new_content = content[:start_idx] + new_nav + content[end_idx + len(nav_end_tag):]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

pages_dir = r"c:\Users\sivak\Downloads\Photographer\photographer\pages"
success_count = 0
for f in os.listdir(pages_dir):
    if f.endswith('.html'):
        if fix_navbar(os.path.join(pages_dir, f)):
            success_count += 1

print(f"Successfully fixed navbar in {success_count} files.")
