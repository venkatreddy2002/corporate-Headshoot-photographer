import os
import re

pages_dir = "pages"

pattern = re.compile(r'(<button id="mobile-menu-close".*?</span>\s*</button>\s*</div>)\s*<button id="mobile-menu-close".*?</span>\s*</button>\s*</div>', re.DOTALL)

# Better pattern based on what I saw
pattern2 = re.compile(r'(<div id="mobile-drawer".*?</div>)\s*(<button id="mobile-menu-close".*?</span>\s*</button>\s*</div>)', re.DOTALL)

for filename in os.listdir(pages_dir):
    if filename.endswith(".html"):
        path = os.path.join(pages_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # This is the exact premature closing pattern
        premature_close = re.compile(r'(<button id="mobile-menu-close".*?</span>\s*</button>\s*</div>)\s*<button id="mobile-menu-close".*?</span>\s*</button>\s*</div>', re.DOTALL)
        
        # Looking at index.html content from view_file:
        # 149:             <button id="mobile-menu-close"
        # 150:                 class="text-slate-500 dark:text-slate-600 dark:text-white/60 hover:text-primary dark:hover:text-white transition-colors">
        # 151:                 <span class="material-symbols-outlined text-2xl">close</span>
        # 152:             </button>
        # 153:         </div>
        # 154:       <button id="mobile-menu-close"
        # 155:         class="text-slate-500 dark:text-slate-600 dark:text-white/60 hover:text-primary dark:hover:text-white transition-colors">
        # 156:         <span class="material-symbols-outlined text-2xl">close</span>
        # 157:       </button>
        # 158:     </div>
        
        fixed_content = re.sub(r'(<button id="mobile-menu-close".*?</span>\s*</button>\s*</div>)\s*<button id="mobile-menu-close".*?</span>\s*</button>\s*</div>', r'\1', content, flags=re.DOTALL)
        
        if fixed_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed structural issue in {filename}")
