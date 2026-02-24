import sys
from files import copy_files
from html import generate_pages_recursive

def main(argv):
    if len(argv) > 1:
        basepath = argv[1]
    else:
        basepath = '/'
    copy_files('./static', './docs')
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

if __name__ == "__main__":
    main(sys.argv)
