import os
from htmlnode import markdown_to_html_node, HTMLNode
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path)as markdown_file:
        markdown_text = markdown_file.read()
    with open(template_path)as template_file:
        template_text = template_file.read()
    markdown_node = markdown_to_html_node(markdown_text)
    markdown_html = markdown_node.to_html()
    title = extract_title(markdown_text)
    template_text = template_text.replace("{{ Title }}", title)
    template_text = template_text.replace("{{ Content }}", markdown_html)
    template_text = template_text.replace('href="/', f'href="{basepath}')
    template_text = template_text.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content,template_path, dest_dir_path.replace(".md", ".html"), basepath)
        return
    dir_path_folders = os.listdir(dir_path_content)
    for folder in dir_path_folders:
        folder_path = os.path.join(dir_path_content, folder)
        dist_path = os.path.join(dest_dir_path, folder)
        generate_pages_recursive(folder_path, template_path, dist_path, basepath)