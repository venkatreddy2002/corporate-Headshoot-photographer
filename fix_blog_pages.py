import re
import os

pages_dir = r"c:\Users\sivak\Downloads\Photographer\photographer\pages"

# --- Files and their specific fixes ---

# BLOG.HTML fixes
blog_html = os.path.join(pages_dir, "blog.html")
with open(blog_html, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the extra nested <main> with pt-24 md:pt-[10%]
content = content.replace(
    '<main class="w-full flex flex-col min-h-screen pt-24 md:pt-[10%]">',
    '<main class="w-full flex flex-col">'
)
# 2. Remove sticky from sub-navigation
content = content.replace(
    '<section class="sticky top-[56px] lg:top-[72px] z-[40] border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-[#030712]/95 backdrop-blur-md transition-colors duration-300 w-full mb-8 pt-0 pl-0 mt-0">',
    '<section class="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-[#030712] transition-colors duration-300 w-full mb-6">'
)
# 3. Tighten padding on inner wrappers
content = content.replace(
    '<div class="max-w-7xl mx-auto px-6 lg:px-20">',
    '<div class="max-w-7xl mx-auto px-4 lg:px-8">'
)
content = content.replace(
    '<div class="max-w-7xl mx-auto px-6 lg:px-20 pb-12 flex-1 w-full">',
    '<div class="max-w-7xl mx-auto px-4 lg:px-8 pb-10 flex-1 w-full">'
)
# 4. Main outer wrapper - remove w-full py-0
content = content.replace(
    '<div class="w-full py-0">',
    '<div class="w-full">'
)
# 5. Reduce hero height to be less overwhelming
content = content.replace(
    '<div class="relative h-[60vh] md:h-[70vh] overflow-hidden group">',
    '<div class="relative h-[45vh] md:h-[50vh] overflow-hidden group">'
)
# 6. Add top padding to main to account for fixed navbar
content = content.replace(
    '<main class="flex-grow">',
    '<main class="flex-grow pt-14">'
)

with open(blog_html, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed: blog.html")


# --- SUB-PAGES: blog-car-care, blog-ceramic, blog-events, blog-restoration, blog-404 ---
sub_pages = [
    "blog-car-care.html",
    "blog-ceramic.html",
    "blog-events.html",
    "blog-restoration.html",
    "blog-404.html",
]

for filename in sub_pages:
    path = os.path.join(pages_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix huge top padding on main
    content = content.replace(
        '<main class="w-full flex flex-col min-h-screen pt-24 md:pt-[10%]">',
        '<main class="w-full flex flex-col pt-14">'
    )

    # 2. Remove sticky from sub-navigation (exact pattern from blog-car-care)
    content = re.sub(
        r'<section class="sticky top-\[56px\] lg:top-\[72px\] z-\[40\] border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-\[#030712\]/95 backdrop-blur-md transition-colors duration-300 w-full mb-8">',
        '<section class="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-[#030712] transition-colors duration-300 w-full mb-6">',
        content
    )

    # 3. Tighten inner padding
    content = content.replace(
        '<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">',
        '<div class="max-w-5xl mx-auto px-4 lg:px-6">'
    )
    content = content.replace(
        '<div class="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8 flex-1 w-full">',
        '<div class="max-w-5xl mx-auto px-4 lg:px-6 py-6 flex-1 w-full">'
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed: {filename}")


# --- BLOG-SINGLE.HTML ---
single_path = os.path.join(pages_dir, "blog-single.html")
with open(single_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add top padding to main for navbar offset and tighten side padding
content = content.replace(
    '<main class="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">',
    '<main class="max-w-5xl mx-auto px-4 lg:px-6 pt-16 pb-8">'
)

with open(single_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed: blog-single.html")

print("\nAll blog pages updated successfully!")
