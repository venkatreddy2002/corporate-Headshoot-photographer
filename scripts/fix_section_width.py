"""
Fix: Wrap section content in dashboard-inner so body content width
matches navbar content width (max-width: 1200px centered).

Handles: lg:px-10, md:px-20 and similar patterns
"""

import os
from bs4 import BeautifulSoup

PAGES_DIR = os.path.join(os.path.dirname(__file__), 'pages')
PADDING_CLASSES_TO_REMOVE = ['px-6', 'px-4', 'px-8', 'lg:px-10', 'md:px-20', 'lg:px-20', 'xl:px-20']
TRIGGER_CLASSES = ['lg:px-10', 'md:px-20', 'lg:px-20', 'xl:px-20']

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Only process files that have relevant padding patterns
    if not any(t in content for t in TRIGGER_CLASSES):
        return False

    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find('body')
    if not body:
        return False

    changed = False
    for section in soup.find_all('section'):
        classes = section.get('class', [])
        if not any(t in classes for t in TRIGGER_CLASSES):
            continue
        # Check if content is NOT already wrapped in dashboard-inner
        first_div = section.find('div', recursive=False)
        if first_div and 'dashboard-inner' in first_div.get('class', []):
            continue  # already wrapped

        # Remove padding classes from section
        new_classes = [c for c in classes if c not in PADDING_CLASSES_TO_REMOVE]
        section['class'] = new_classes

        # Collect all children
        children = list(section.children)

        # Create inner wrapper
        wrapper = soup.new_tag('div', attrs={'class': 'dashboard-inner'})
        for child in children:
            wrapper.append(child.extract())

        section.append(wrapper)
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated: {os.path.basename(filepath)}")

    return changed

def main():
    total = 0
    for fname in sorted(os.listdir(PAGES_DIR)):
        if not fname.endswith('.html'):
            continue
        path = os.path.join(PAGES_DIR, fname)
        if fix_file(path):
            total += 1
    print(f"\nTotal files updated: {total}")

if __name__ == '__main__':
    main()
