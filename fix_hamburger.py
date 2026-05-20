import os
import re

def fix_hamburger(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the mobile-menu-trigger button and the span inside it
        # We target the span that contains "menu" text
        pattern = re.compile(r'(<button\s+id="mobile-menu-trigger"[^>]*>.*?<span\s+class="material-symbols-outlined[^"]*)(?="[^>]*>\s*menu\s*</span>)', re.DOTALL)
        
        new_content = pattern.sub(r'\1 max-lg:bg-gray-200', content)

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"Error in {file_path}: {e}")
        return False

pages_dir = r"c:\Users\sivak\Downloads\Photographer\photographer\pages"
success_count = 0
for f in os.listdir(pages_dir):
    if f.endswith('.html'):
        if fix_hamburger(os.path.join(pages_dir, f)):
            success_count += 1

print(f"Updated hamburger icon in {success_count} files.")
