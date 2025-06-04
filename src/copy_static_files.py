import os
import shutil

from markdown import extract_title, markdown_to_html_node


def generate_page_recursive(basepath, dir_path_content, template_path, des_dir_path):
    if os.path.isdir(dir_path_content):
        for path in os.listdir(dir_path_content):
            if os.path.isdir(os.path.join(dir_path_content, path)):
                generate_page_recursive(
                    basepath,
                    os.path.join(dir_path_content, path),
                    template_path,
                    os.path.join(des_dir_path, path),
                )
            else:
                generate_page(
                    basepath,
                    os.path.join(dir_path_content, path),
                    template_path,
                    os.path.join(des_dir_path, f"{path.split('.')[0]}.html"),
                )


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_path = os.path.join(basepath, from_path)
    template_path = os.path.join(basepath, template_path)
    dest_path = os.path.join(basepath, dest_path)

    md = open(from_path, "r").read()
    template = open(template_path, "r").read()

    md_to_html = markdown_to_html_node(md).to_html()
    page_title = extract_title(md)
    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", md_to_html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dirs = dest_path.split("/")

    writting_path = []
    for dir in dirs[:-1]:
        writting_path.append(dir)
        current_dir = "/".join(writting_path)
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)

    open(dest_path, "w").write(template)


def copy_files(basepath, copy_path="public", origin_path="static"):
    copy_path = os.path.join(basepath, copy_path)
    origin_path = os.path.join(basepath, origin_path)
    if not os.path.exists(copy_path):
        os.makedirs(copy_path)

    if len(os.listdir(copy_path)) > 0:
        shutil.rmtree(copy_path)

    copied_files = []

    def traverse_file_and_folders(origin_path, path, copied_files):
        new_path = os.path.join(origin_path, path)
        if os.path.isdir(new_path):
            for another_path in os.listdir(new_path):
                traverse_file_and_folders(new_path, another_path, copied_files)

        if os.path.isfile(new_path):
            copied_files.append(new_path)

    traverse_file_and_folders("./", origin_path, copied_files)

    for file in copied_files:
        file_path = "/".join(file.split("/")[:-1])

        if not os.path.exists(file_path.replace(origin_path + "/", copy_path + "/")):
            os.makedirs(file_path.replace(origin_path + "/", copy_path + "/"))

        print(f"Copy: {file} => {file.replace(origin_path+ "/", copy_path+ "/")}")
        shutil.copy(file, file.replace(origin_path + "/", copy_path + "/"))
