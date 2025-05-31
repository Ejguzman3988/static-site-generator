import unittest

from helper import split_nodes_delimiter, text_node_to_html_node
from htmlnode import HTMLNode
from textnode import TextNode, TextType

# class HTMLNode(
#     tag: Unknown | None = None,
#     value: Unknown | None = None,
#     children: Unknown | None = None,
#     props: Unknown | None = None
# )


class TestHtmlNode(unittest.TestCase):
    def test_props_single_to_html(self):
        node = HTMLNode(
            "p",
            "test text",
            HTMLNode("p", "inner text"),
            {"href": "https://www.boot.dev"},
        )

        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_props_multi_to_html(self):
        node = HTMLNode(
            "p",
            "test text",
            HTMLNode("p", "inner text"),
            {"href": "https://www.boot.dev", "target": "_blank"},
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://www.boot.dev" target="_blank"'
        )

    def test_to_html(self):
        node = HTMLNode()

        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_delimiter(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_delimiter_adv(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        node_adv = TextNode("This is a text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node_adv], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a `code block` word", TextType.TEXT),
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("code block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    # def test_repr(self):
    #     node = HTMLNode(
    #         "p",
    #         "test text",
    #         HTMLNode("p", "inner text"),
    #         {"href": "https://www.boot.dev"},
    #     )
    #     self.assertEqual(
    #         node,
    #         "HTMLNode(\r\n  p, \r\n  test text, \r\n  HTMLNode(\r\n    p, \r\n    inner text, \r\n    None, \r\n    None\r\n  ), \r\n  {'href': 'https://www.boot.dev'})",
    #     )


if __name__ == "__main__":
    unittest.main()
