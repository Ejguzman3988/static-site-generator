import sys
from copy_static_files import copy_files, generate_page_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_files("./docs", "./static")
    generate_page_recursive("./content", "./template.html", "./docs", basepath)


if __name__ == "__main__":
    main()
