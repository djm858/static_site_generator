from files import copy_files
from html import generate_pages_recursive

def main():
    copy_files('./static', './public')
    generate_pages_recursive('content', 'template.html', 'public')

main()
