import re

def sync_drawer():
    # Read source from index.html
    with open(r'c:\Users\sivak\Downloads\Photographer\photographer\pages\index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # Extract drawer using regex (from <!-- Mobile Drawer Overlay --> to <!-- End Mobile Drawer -->)
    drawer_pattern = re.compile(r'(<!-- Mobile Drawer Overlay -->\s*<div id="drawer-overlay".*?</div>\s*<!-- Mobile Drawer -->\s*<div id="mobile-drawer".*?</div><!-- End Mobile Drawer -->)', re.DOTALL)
    
    match = drawer_pattern.search(index_html)
    if not match:
        print("Could not find drawer in index.html")
        return
        
    drawer_content = match.group(1)
    
    # Read target
    with open(r'c:\Users\sivak\Downloads\Photographer\photographer\pages\portfolio.html', 'r', encoding='utf-8') as f:
        target_html = f.read()
        
    # Find drawer in target (from <!-- Mobile Drawer Overlay --> up to just before <main class="pt-20">)
    # The portfolio drawer might end differently, let's use a simpler pattern
    target_pattern = re.compile(r'<!-- Mobile Drawer Overlay -->.*?</div>\s*</header>', re.DOTALL)
    # Wait, the portfolio HTML has:
    # <!-- Mobile Drawer Overlay -->
    # ...
    #     </div>
    # 
    #     <main class="pt-20">
    
    target_pattern = re.compile(r'(<!-- Mobile Drawer Overlay -->.*?)\s*<main class="pt-20">', re.DOTALL)
    
    def replace_drawer(match):
        return drawer_content + '\n\n    <main class="pt-20">'
        
    new_target_html = target_pattern.sub(replace_drawer, target_html)
    
    with open(r'c:\Users\sivak\Downloads\Photographer\photographer\pages\portfolio.html', 'w', encoding='utf-8') as f:
        f.write(new_target_html)
        
    print("Drawer synced successfully to portfolio.html")

sync_drawer()
