import os
import glob
import re

html_files = glob.glob('pages/*.html')

# 1. Update style.css
css_file = 'assets/css/style.css'
with open(css_file, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace border-radius: 10px !important; with border-radius: 0 !important;
css_content = re.sub(r'border-radius:\s*10px\s*!important;', r'border-radius: 0 !important;', css_content)
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(css_content)
print("Updated style.css")

# 2. Update HTML files
# We want to remove any rounded classes from <button> tags and <a> tags that look like buttons.
# A class is like: rounded, rounded-sm, rounded-md, rounded-lg, rounded-xl, rounded-full, rounded-[something], sm:rounded...
# Pattern to match a rounded class (including breakpoints like md:rounded-lg)
rounded_class_pattern = r'\b(?:sm:|md:|lg:|xl:|2xl:)?rounded(?:-(?:sm|md|lg|xl|2xl|3xl|full|none|\[.*?\]))?\b'

def remove_rounded(match):
    tag_start = match.group(1) # e.g. <button class="
    classes = match.group(2)   # e.g. bg-blue-500 rounded-lg px-4
    tag_end = match.group(3)   # e.g. ">

    # Check if the <a> tag is actually a button (has px-, py-, bg-, btn-)
    # We always process <button> tags.
    is_a_tag = tag_start.lower().startswith('<a')
    if is_a_tag:
        is_button_like = bool(re.search(r'\b(btn-|bg-primary|px-|py-|bg-)\b', classes))
        if not is_button_like:
            return match.group(0) # Do not modify this <a> tag

    # Remove all rounded classes
    new_classes = re.sub(rounded_class_pattern, '', classes)
    
    # Clean up multiple spaces that might have been left
    new_classes = re.sub(r'\s+', ' ', new_classes).strip()
    
    return f"{tag_start}{new_classes}{tag_end}"

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find elements with a class attribute: <button ... class="..." ...> or <a ... class="..." ...>
    # It finds the opening tag up to the class="", the contents of the class="", and the rest of the tag up to ">"
    
    # We need to be careful with regex parsing HTML. Let's find class attributes within <button> or <a>
    # This pattern matches <button ... class=" ... " ... > and <a ... class=" ... " ... >
    # group 1: <button ... class=" (or <a ... class=")
    # group 2: the classes
    # group 3: " ... >
    pattern = r'(<(?:button|a)\b[^>]*?class=")([^"]*)("[^>]*>)'
    
    new_content = re.sub(pattern, remove_rounded, content, flags=re.IGNORECASE)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

