from textnode import TextNode
from copy import copy
from generate_page import generate_pages_recursive

def main():
    copy("static", "public")
    generate_pages_recursive(
        "content", 
        "template.html", 
        "public")
main()