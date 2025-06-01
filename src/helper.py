import re
from leafnode import LeafNode
from textnode import TextNode, TextType

BASE_TXT = "google"
BASE_URL = "https://www.google.com"
BASE_ALT = "A Smiling Dog"
BASE_SRC = "https://i.imgur.com/hdiQzJa.png"


def create_url(text_type=TextType.LINK, text=BASE_TXT, url=BASE_URL):
    if not isinstance(text_type, TextType):
        raise TypeError(
            f"`text_type` must be an instance of TextType, got {type(text_type).__name__}"
        )

    if text_type not in [TextType.LINK, TextType.IMAGE]:
        raise ValueError(
            f"Function: create_url does not suppoert type: {text_type} \r\n Type must be either TextType.LINK or TextType.IMAGE"
        )

    bracket = "![" if text_type == TextType.IMAGE else "["
    if text_type == TextType.IMAGE and text == BASE_TXT:
        text = BASE_ALT

    if text_type == TextType.IMAGE and url == BASE_URL:
        url = BASE_SRC

    return f"{bracket}{text}]({url})"


def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )

        case _:
            raise Exception("Text type does not exist")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) <= 1:
                new_nodes.append(node)
            elif len(split_node) == 2:
                raise Exception("That is invalid markdown")
            else:
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                new_nodes.append(TextNode(split_node[1], text_type))
                new_nodes.append(TextNode(split_node[2], TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    # To be able to change this over the operations
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            list_image_tuple = extract_markdown_links(node.text)
            if len(list_image_tuple) == 0:
                new_nodes.append(node)
                continue

            temp_str = node.text
            for [alt, src] in list_image_tuple:
                sub_strs = temp_str.split(f"![{alt}]({src})", 1)
                if len(sub_strs) <= 1:
                    continue
                front = sub_strs[0]
                back = sub_strs[1]
                if front != "":
                    new_nodes.append(TextNode(front, TextType.TEXT))

                new_nodes.append(TextNode(alt, TextType.IMAGE, src))
                temp_str = back

            if temp_str != "":
                new_nodes.append(TextNode(temp_str, TextType.TEXT))
            # list of tuples with images

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    # To be able to change this over the operations
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            list_image_tuple = extract_markdown_links(node.text)
            if len(list_image_tuple) == 0:
                new_nodes.append(node)
                continue

            temp_str = node.text

            for [txt, url] in list_image_tuple:
                sub_strs = temp_str.split(f"[{txt}]({url})", 1)
                if len(sub_strs) <= 1:
                    continue

                front = sub_strs[0]
                back = sub_strs[1]
                if front != "":
                    new_nodes.append(TextNode(front, TextType.TEXT))

                new_nodes.append(TextNode(txt, TextType.LINK, url))

                temp_str = back

            if temp_str != "":
                new_nodes.append(TextNode(temp_str, TextType.TEXT))
            # list of tuples with images

    return new_nodes


def text_to_textnodes(text):
    original_nodes = [TextNode(text, TextType.TEXT)]

    bold_split = split_nodes_delimiter(original_nodes, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_image(code_split)
    link_split = split_nodes_link(image_split)

    return link_split
