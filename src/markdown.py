from blocktype import (
    CODE,
    HEADING,
    ORDERED_LIST,
    PARAGRAPH,
    QUOTE,
    UNORDERED_LIST,
    block_to_block_type,
    block_to_str,
)
from helper import text_node_to_html_node, text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    first_block = blocks[0]
    block_type = block_to_block_type(first_block)
    if block_type != HEADING or first_block[:2] != "# ":
        raise Exception("No H1 Header")
    return first_block[2:]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []
    html = ParentNode("div", children)

    for block in blocks:
        block_type = block_to_block_type(block)
        line = block_to_str(block)

        if block_type == PARAGRAPH:
            inner_children = []
            children.append(ParentNode("p", inner_children))
            text_nodes = text_to_textnodes(line)
            for node in text_nodes:
                inner_children.append(text_node_to_html_node(node))
        elif block_type == HEADING:
            inner_children = []
            children.append(block_heading_to_html(line))
        elif block_type == CODE:
            inner_children = []
            children.append(ParentNode("pre", [LeafNode("code", block[4:-3])]))
        elif block_type == UNORDERED_LIST:
            inner_children = []
            children.append(ParentNode("ul", inner_children))
            lines = block.split("\n")
            for line in lines:
                li_child = []
                text_nodes = text_to_textnodes(line[2:])
                for node in text_nodes:
                    li_child.append(text_node_to_html_node(node))
                inner_children.append(ParentNode("li", li_child))
        elif block_type == ORDERED_LIST:
            inner_children = []
            children.append(ParentNode("ol", inner_children))
            lines = block.split("\n")
            for line in lines:
                dot_index = line.find(".")
                li_child = []
                text_nodes = text_to_textnodes(line[dot_index + 2 :])
                for node in text_nodes:
                    li_child.append(text_node_to_html_node(node))
                inner_children.append(
                    ParentNode(
                        "li",
                        li_child,
                    )
                )
        elif block_type == QUOTE:
            inner_children = []
            text_nodes = text_node_to_html_node(
                TextNode(block.replace("> ", "").replace("\n", " "), TextType.TEXT)
            )
            children.append(ParentNode("blockquote", [text_nodes]))

    return html


def block_heading_to_html(line):
    count = 0
    for i in range(6):
        if line.startswith("#" * (i + 1)):
            count += 1

    text_node = TextNode(line[count + 1 :], TextType.TEXT)
    child_text_nodes = text_node_to_html_node(text_node)
    return ParentNode("h" + str(count), [child_text_nodes])


def markdown_to_blocks(markdown):
    return list(
        filter(lambda x: x != "", map(lambda x: x.strip(), markdown.split("\n\n")))
    )
