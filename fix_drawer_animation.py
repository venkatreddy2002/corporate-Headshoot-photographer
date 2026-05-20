import os
import glob

html_files = glob.glob('pages/*.html') + ['index.html']

for file in html_files:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file has the drawer
    if 'id="mobile-drawer"' in content:
        # For overlay
        content = content.replace('id="drawer-overlay"\n    class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] opacity-0 invisible transition-all duration-300"',
                                  'id="drawer-overlay"\n    class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] opacity-0 invisible transition-all duration-300 nav-mobile:hidden"')
        
        # If it's on a single line
        content = content.replace('id="drawer-overlay" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] opacity-0 invisible transition-all duration-300"',
                                  'id="drawer-overlay" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] opacity-0 invisible transition-all duration-300 nav-mobile:hidden"')

        # For drawer
        # There are variations. The key is to add nav-mobile:hidden to the drawer class list if it doesn't exist
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'id="mobile-drawer"' in line or 'id="drawer-overlay"' in line:
                # Need to add nav-mobile:hidden to the class list of the next line or this line
                pass
                
with open('fix_drawer_animation.py', 'w') as f: pass # clear it out
