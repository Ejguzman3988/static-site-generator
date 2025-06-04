import os
import shutil

from markdown import extract_title, markdown_to_html_node


def generate_page(
    from_path="content/index.md",
    template_path="template.html",
    dest_path="public/index.html",
):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path, "r").read()
    template = open(template_path, "r").read()

    md_to_html = markdown_to_html_node(md).to_html()
    page_title = extract_title(md)
    template.replace("{{ Title }}", page_title)
    template.replace("{{ Content }}", md_to_html)

    dirs = dest_path.split("/")

    writting_path = []
    for dir in dirs:
        writting_path.append(dir)
        current_dir = "/".join(writting_path)
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)

    open(dest_path, "w").write(template_path)

    # template = open(template_path, "r").read()
    # html = template.replace("{{content}}", md)
    # open(dest_path, "w").write(html


def copy_public(copy_path="/public", origin_path="/static"):
    cwd = os.getcwd()
    if not os.path.exists(cwd + copy_path):
        os.makedirs(cwd + copy_path)
    if len(os.listdir(cwd + copy_path)) > 0:
        shutil.rmtree(cwd + copy_path)

    copied_files = []

    def traverse_file_and_folders(origin_path, path, copied_files):
        new_path = origin_path + "/" + path
        if os.path.isdir(new_path):
            for another_path in os.listdir(new_path):
                traverse_file_and_folders(new_path, another_path, copied_files)

        if os.path.isfile(new_path):
            copied_files.append(new_path)

    traverse_file_and_folders(cwd, origin_path[1:], copied_files)

    for file in copied_files:
        file_path = "/".join(file.split("/")[:-1])

        if not os.path.exists(file_path.replace(origin_path + "/", copy_path + "/")):
            os.makedirs(file_path.replace(origin_path + "/", copy_path + "/"))

        print(f"Copy: {file} => {file.replace(origin_path+ "/", copy_path+ "/")}")
        shutil.copy(file, file.replace(origin_path + "/", copy_path + "/"))
