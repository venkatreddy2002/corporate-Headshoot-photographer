import os
import glob
import re

html_files = glob.glob('pages/*.html')

for file_path in html_files:
    if 'dashboard' in file_path:
        continue # skip dashboards as they might not have these header buttons
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to swap the classes of the Book Sessions and Login buttons.
    # The original Book Sessions button has classes containing `bg-primary text-white`
    # The original Login button has classes containing `bg-white/50 ... border border-slate-200 ... text-slate-600`
    
    # Let's do a precise replace based on what we found in index.html
    # Book Sessions original:
    # class="hidden nav-mobile:flex items-center justify-center rounded-lg h-9 px-4 bg-primary text-white text-[10px] font-black uppercase tracking-wider transition-all hover:brightness-110 active:scale-95 shadow-md shadow-primary/20"
    # Login original:
    # class="hidden nav-mobile:flex items-center justify-center rounded-lg h-9 px-4 bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:text-primary text-[10px] font-bold uppercase tracking-wider transition-all active:scale-95"
    
    # Replace Book Sessions
    content = re.sub(
        r'(<a href="book-services\.html"[^>]*class=")([^"]+)(">\s*Book Sessions\s*</a>)',
        r'\1hidden nav-mobile:flex items-center justify-center rounded-lg h-9 px-4 bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:text-primary text-[10px] font-bold uppercase tracking-wider transition-all active:scale-95\3',
        content, flags=re.IGNORECASE | re.DOTALL
    )

    # Replace Login
    content = re.sub(
        r'(<a href="login\.html"[^>]*class=")([^"]+)(">\s*Login\s*</a>)',
        r'\1hidden nav-mobile:flex items-center justify-center rounded-lg h-9 px-4 bg-primary text-white text-[10px] font-black uppercase tracking-wider transition-all hover:brightness-110 active:scale-95 shadow-md shadow-primary/20\3',
        content, flags=re.IGNORECASE | re.DOTALL
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {file_path}")
