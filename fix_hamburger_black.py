import os
import re

def fix_hamburger(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update max-lg:bg-gray-200 to max-lg:bg-black
        new_content = content.replace('max-lg:bg-gray-200', 'max-lg:bg-black')

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

print(f"Updated hamburger icon background to black in {success_count} files.")
