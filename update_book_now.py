import os
import glob
import re

html_files = glob.glob('pages/*.html')

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Change "Book Sessions" to "Book Now" in the navbar and other places if it's the specific button
    # The navbar button is usually >Book Sessions< or similar
    # We can just replace '>Book Sessions<' with '>Book Now<' or replacing 'Book Sessions' generally
    # Let's target the exact text node or just do a global replace for "Book Sessions" inside the <a> tag
    new_content = re.sub(r'(<a[^>]*href="book-services.html"[^>]*>)\s*Book Sessions\s*(</a>)', r'\1\n                Book Now\n            \2', content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated Book Sessions to Book Now in {file_path}")

print("Done updating HTML files.")
