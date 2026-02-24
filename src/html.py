import re
import os
from pathlib import Path
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    matches = re.findall(r'^#\s+(.*)', markdown, flags=re.MULTILINE)
    if len(matches) == 0:
        raise Exception('markdown file does not contain header')
    return matches[0]

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    try:
        with open(from_path, 'r') as file:
            markdown = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

    try:
        with open(template_path, 'r') as file:
            template = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
