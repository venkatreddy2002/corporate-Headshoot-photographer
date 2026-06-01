import os
import re

def refactor_html_files():
    pages_dir = 'pages'
    root_dir = '.'
    
    # 1. Refactor root 404.html
    root_404 = os.path.join(root_dir, '404.html')
    if os.path.exists(root_404):
        with open(root_404, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace script src
        content = content.replace('assets/js/tailwind-config.js', 'configs/tailwind-config.js')
        
        with open(root_404, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Refactored root 404.html")

    # 2. Refactor pages/
    inline_script_pattern = re.compile(r'<script\s+id="tailwind-config">.*?</script>', re.DOTALL)
    
    for filename in os.listdir(pages_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(pages_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Replace inline tailwind configs
            if inline_script_pattern.search(content):
                content = inline_script_pattern.sub('<script src="../configs/tailwind-config.js"></script>', content)
                print(f"Removed inline tailwind config in {filename}")
                
            # Replace regular scripts
            content = content.replace('../assets/js/tailwind-config.js', '../configs/tailwind-config.js')
            content = content.replace('assets/js/tailwind-config.js', '../configs/tailwind-config.js')
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {filename}")

if __name__ == '__main__':
    refactor_html_files()
