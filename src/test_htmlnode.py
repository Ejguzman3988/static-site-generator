import unittest

from htmlnode import HTMLNode

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
