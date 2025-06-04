import sys
from copy_static_files import copy_files, generate_page_recursive


def main():
    basepath = "./"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_files(basepath, "doc", "static")
    generate_page_recursive(basepath, "content", "template.html", "public")


if __name__ == "__main__":
    main()
