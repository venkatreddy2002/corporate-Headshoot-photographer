import os
import re

def update_nav_buttons(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update Book Now
        # Targeting the desktop version inside the lg:flex container
        # We look for the one with h-9 and px-6 (current state)
        book_now_pattern = re.compile(r'(<a href="book-services.html"\s+class=")[^"]*h-9 px-6[^"]*(">\s*Book Now\s*</a>)')
        new_book_now = r'\1h-9 px-4 flex items-center justify-center border border-primary text-primary bg-transparent font-bold uppercase rounded-lg shadow-sm hover:bg-primary/5 transition-all\2'
        
        # Update Login
        # Targeting the desktop version
        login_pattern = re.compile(r'(<a href="login.html"\s+class=")[^"]*h-9 px-4[^"]*(">\s*Login\s*</a>)')
        new_login = r'\1h-9 px-4 flex items-center justify-center bg-primary text-white text-xs font-bold uppercase rounded-lg shadow-md shadow-primary/20 hover:brightness-110 transition-all\2'

        new_content = book_now_pattern.sub(new_book_now, content)
        new_content = login_pattern.sub(new_login, new_content)

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
        if update_nav_buttons(os.path.join(pages_dir, f)):
            success_count += 1

print(f"Updated nav buttons in {success_count} files.")
