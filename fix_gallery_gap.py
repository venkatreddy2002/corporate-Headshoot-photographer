import os
import glob
import re

gallery_files = glob.glob('pages/gallery*.html')

old_css = r'''\.gallery-grid \{
\s*display: grid;
\s*grid-template-columns: repeat\(auto-fill, minmax\(140px, 1fr\)\);
\s*gap: 1rem;
\s*\}

\s*@media \(min-width: 768px\) \{
\s*\.gallery-grid \{
\s*grid-template-columns: repeat\(auto-fill, minmax\(300px, 1fr\)\);
\s*gap: 1\.5rem;
\s*\}
\s*\}'''

new_css = '''.gallery-grid {
            column-count: 2;
            column-gap: 1rem;
        }

        .gallery-grid > div {
            break-inside: avoid;
            margin-bottom: 1rem;
            display: inline-block;
            width: 100%;
        }

        @media (min-width: 768px) {
            .gallery-grid {
                column-count: 3;
                column-gap: 1.5rem;
            }
            .gallery-grid > div {
                margin-bottom: 1.5rem;
            }
        }'''

for file_path in gallery_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's check if the old css is present
    if re.search(old_css, content):
        new_content = re.sub(old_css, new_css, content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated CSS in {file_path}")
    else:
        # Fallback if whitespace differs
        # Just replace the block more loosely
        # Find .gallery-grid up to closing brace of media query
        loose_pattern = r'\.gallery-grid\s*\{[^}]+\}\s*@media\s*\([^)]+\)\s*\{\s*\.gallery-grid\s*\{[^}]+\}\s*\}'
        if re.search(loose_pattern, content):
            new_content = re.sub(loose_pattern, new_css, content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated CSS in {file_path} (loose match)")
        else:
            print(f"Could not find .gallery-grid CSS in {file_path}")
