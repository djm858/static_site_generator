from textnode import TextType, TextNode

def main():
    textnode = TextNode("dummy text", TextType.LINK, "https://www.boot.dev")
    print(textnode.__repr__())

main()
