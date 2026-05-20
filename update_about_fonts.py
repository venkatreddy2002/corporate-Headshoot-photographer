import os
import re

file_path = r"c:\Users\sivak\Downloads\Photographer\photographer\pages\about.html"
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace 1: Subheader
    content = content.replace(
        '<p class="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">',
        '<p class="text-slate-600 dark:text-slate-400 text-lg md:text-xl max-w-2xl mx-auto">'
    )

    # Replace 2: Marcus Thorne Name
    content = content.replace(
        '<h3 class="text-3xl font-bold text-slate-900 dark:text-white mb-4">',
        '<h3 class="text-4xl font-bold text-slate-900 dark:text-white mb-4">'
    )

    # Replace 3: Title
    content = content.replace(
        '<p class="text-primary font-semibold mb-4">',
        '<p class="text-primary text-xl font-semibold mb-4">'
    )

    # Replace 4: Description
    content = content.replace(
        '<p class="text-slate-600 dark:text-slate-400 leading-relaxed mb-6">',
        '<p class="text-slate-600 dark:text-slate-400 text-lg leading-relaxed mb-6">'
    )

    # Replace 5: Experience
    content = content.replace(
        '<div class="flex gap-6 text-sm text-slate-500 dark:text-slate-400">',
        '<div class="flex gap-6 text-base text-slate-500 dark:text-slate-400">'
    )

    # Replace 6: Cards H4
    content = content.replace(
        '<h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">',
        '<h4 class="text-xl font-bold text-slate-900 dark:text-white mb-2">'
    )

    # Replace 7: Cards P inside team highlights
    parts = content.split('<!-- TEAM HIGHLIGHTS -->')
    if len(parts) > 1:
        parts[1] = parts[1].replace('<p class="text-sm text-slate-600 dark:text-slate-400">', '<p class="text-base text-slate-600 dark:text-slate-400">')
        content = '<!-- TEAM HIGHLIGHTS -->'.join(parts)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated font sizes in about.html")
except Exception as e:
    print(f"Error: {e}")
