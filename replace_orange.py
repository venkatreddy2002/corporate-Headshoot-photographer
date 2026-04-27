import os

files_to_update = ['pages/login.html', 'pages/register.html']

for file_path in files_to_update:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace orange specific classes with primary/blue classes
        content = content.replace('bg-[#d95c27]', 'bg-primary')
        content = content.replace('text-[#d95c27]', 'text-primary')
        content = content.replace('focus:ring-[#d95c27]', 'focus:ring-primary')
        content = content.replace('hover:text-[#d95c27]', 'hover:text-primary')
        content = content.replace('shadow-[#d95c27]/30', 'shadow-primary/30')
        content = content.replace('hover:bg-[#c25121]', 'hover:brightness-110')
        
        # Also replace #d95d2c if it exists
        content = content.replace('bg-[#d95d2c]', 'bg-primary')
        content = content.replace('text-[#d95d2c]', 'text-primary')
        content = content.replace('focus:ring-[#d95d2c]', 'focus:ring-primary')
        content = content.replace('hover:text-[#d95d2c]', 'hover:text-primary')
        content = content.replace('shadow-[#d95d2c]/30', 'shadow-primary/30')
        content = content.replace('hover:bg-[#c2512c]', 'hover:brightness-110')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")
