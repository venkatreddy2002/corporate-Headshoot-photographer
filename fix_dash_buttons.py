import os
import re

files = [
    'c:/Users/sivak/Downloads/Photographer/photographer/pages/dashboard.html',
    'c:/Users/sivak/Downloads/Photographer/photographer/pages/user-dashboard.html'
]

# Common conflicting classes to remove
classes_to_remove = [
    'bg-primary', 'bg-amber-500', 'bg-slate-100', 'bg-slate-800', 'dark:bg-slate-800',
    'text-white', 'text-slate-600', 'text-slate-300', 'dark:text-slate-300',
    'hover:bg-primary/90', 'hover:bg-amber-600', 'hover:bg-slate-200', 'dark:hover:bg-accent-dark',
    'py-2.5', 'py-2', 'px-4', 'rounded-xl', 'rounded-lg'
]

def repl_btn(m):
    class_attr = m.group(1)
    text = m.group(2)
    
    # Determine target class based on text
    target_class = ''
    if 'View Details' in text or 'Accept' in text:
        target_class = 'btn-primary'
    elif 'Project Timeline' in text or 'View Moodboard' in text or 'View Brief' in text:
        target_class = 'btn-secondary'
    elif 'Review Gallery' in text:
        target_class = 'btn-accent'
    
    if not target_class:
        return m.group(0) # don't touch if it's not a card button we know
        
    # Clean up existing conflicting classes
    new_class_attr = class_attr
    for cls in classes_to_remove:
        # use regex to replace whole word boundary
        new_class_attr = re.sub(r'\b' + re.escape(cls) + r'\b', '', new_class_attr)
        
    # Add the new target class
    new_class_attr = re.sub(r'\s+', ' ', new_class_attr).strip()
    new_class_attr += ' ' + target_class
    
    return f'<button class="{new_class_attr}">{text}</button>'

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match <button class="...">...</button>
    new_content = re.sub(r'<button\s+class="([^"]+)"\s*>([^<]+)</button>', repl_btn, content)
    
    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {file_path}')
