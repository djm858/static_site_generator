import re
from textnode import TextType, TextNode

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"matching closing delimiter ({delimiter}) not found")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                type = TextType.TEXT
            else:
                type = text_type
            new_nodes.append(TextNode(split_text[i], type))
    return new_nodes

def split_nodes_imagelink(old_nodes, type, split_string):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        match type:
            case TextType.IMAGE:
                tuples = extract_markdown_images(old_node.text)
            case TextType.LINK:
                tuples = extract_markdown_links(old_node.text)
            case _:
                raise Exception("not valid type for split_nodes_imagelink")
        if len(tuples) == 0:
            new_nodes.append(old_node)
            continue
        remaining_text = re.split(split_string, old_node.text)
        for i in range(len(remaining_text)):
            if remaining_text[i] != "":
                new_nodes.append(TextNode(remaining_text[i], old_node.text_type))
            if i < len(remaining_text) - 1:
                tuple = tuples[i]
                new_nodes.append(TextNode(tuple[0], type, tuple[1]))
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_imagelink(old_nodes, TextType.IMAGE, r"!\[[^\[\]]*\]\([^\(\)]*\)")

def split_nodes_link(old_nodes):
    return split_nodes_imagelink(old_nodes, TextType.LINK, r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)")

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
