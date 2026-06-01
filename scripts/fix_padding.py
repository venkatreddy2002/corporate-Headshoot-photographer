import os

def replace_in_files(directory, old_str, new_str):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if old_str in content:
                        new_content = content.replace(old_str, new_str)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                        print(f"Updated {filepath}")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    replace_in_files('.', 'lg:px-[100px]', 'lg:px-10')
