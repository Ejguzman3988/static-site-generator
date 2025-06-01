import unittest

from helper import (
    BASE_ALT,
    BASE_SRC,
    BASE_TXT,
    BASE_URL,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    create_url,
    text_to_textnodes,
)
from textnode import TextNode, TextType

# class HTMLNode(
#     tag: Unknown | None = None,
#     value: Unknown | None = None,
#     children: Unknown | None = None,
#     props: Unknown | None = None
# )


class TestHelpers(unittest.TestCase):
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

    def test_extract_markdown_images_simple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        list_images = extract_markdown_images(text)
        self.assertListEqual(
            list_images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links_simple(self):
        matches = extract_markdown_links(
            "This is text with an link [to an image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            matches, [("to an image", "https://i.imgur.com/zjjcJKZ.png")]
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        list_links = extract_markdown_links(text)
        self.assertListEqual(
            list_links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_create_url(self):
        with self.assertRaises(TypeError):
            create_url("link")

        with self.assertRaises(ValueError):
            create_url(TextType.CODE)

        self.assertEqual(create_url(), f"[{BASE_TXT}]({BASE_URL})")
        self.assertEqual(create_url(TextType.IMAGE), f"![{BASE_ALT}]({BASE_SRC})")
        self.assertEqual(create_url(TextType.LINK), f"[{BASE_TXT}]({BASE_URL})")
        self.assertEqual(create_url(TextType.IMAGE, "dog"), f"![dog]({BASE_SRC})")
        self.assertEqual(
            create_url(TextType.IMAGE, url="https://i.imgur.com/7vmoGw5.jpeg"),
            f"![{BASE_ALT}](https://i.imgur.com/7vmoGw5.jpeg)",
        )
        self.assertEqual(
            create_url(
                TextType.IMAGE,
                "Another smiling dog",
                "https://i.imgur.com/7vmoGw5.jpeg",
            ),
            "![Another smiling dog](https://i.imgur.com/7vmoGw5.jpeg)",
        )
        self.assertEqual(
            create_url(TextType.LINK, "Google", "https://www.google.com"),
            "[Google](https://www.google.com)",
        )
        self.assertEqual(
            create_url(TextType.LINK, "GitHub", "https://github.com"),
            "[GitHub](https://github.com)",
        )
        self.assertEqual(
            create_url(TextType.LINK, url="https://example.com"),
            f"[{BASE_TXT}](https://example.com)",
        )
        self.assertEqual(create_url(TextType.LINK, url="Docs"), f"[{BASE_TXT}](Docs)")

    def test_split_nodes_image(self):
        prepend_text = "This text is PREPENDED"
        appended_text = "This text is APPENDED."

        self.assertListEqual(
            split_nodes_image([TextNode(prepend_text, TextType.TEXT)]),
            [TextNode(prepend_text, TextType.TEXT)],
        )

        self.assertListEqual(
            split_nodes_image(
                [
                    TextNode(prepend_text, TextType.TEXT),
                    TextNode(appended_text, TextType.TEXT),
                ]
            ),
            [
                TextNode(prepend_text, TextType.TEXT),
                TextNode(appended_text, TextType.TEXT),
            ],
        )

        self.assertListEqual(
            split_nodes_image([TextNode(create_url(TextType.IMAGE), TextType.TEXT)]),
            [TextNode(BASE_ALT, TextType.IMAGE, BASE_SRC)],
        )

        self.assertListEqual(
            split_nodes_image(
                [TextNode(prepend_text + create_url(TextType.IMAGE), TextType.TEXT)]
            ),
            [
                TextNode(prepend_text, TextType.TEXT),
                TextNode(BASE_ALT, TextType.IMAGE, BASE_SRC),
            ],
        )

        self.assertListEqual(
            split_nodes_image(
                [
                    TextNode(
                        prepend_text + create_url(TextType.IMAGE) + appended_text,
                        TextType.TEXT,
                    )
                ]
            ),
            [
                TextNode(prepend_text, TextType.TEXT),
                TextNode(BASE_ALT, TextType.IMAGE, BASE_SRC),
                TextNode(appended_text, TextType.TEXT),
            ],
        )

        self.assertListEqual(
            split_nodes_image(
                [
                    TextNode(
                        prepend_text + create_url(TextType.IMAGE) + appended_text,
                        TextType.TEXT,
                    ),
                    TextNode(prepend_text, TextType.TEXT),
                    TextNode(create_url(TextType.IMAGE), TextType.TEXT),
                ]
            ),
            [
                TextNode(prepend_text, TextType.TEXT),
                TextNode(BASE_ALT, TextType.IMAGE, BASE_SRC),
                TextNode(appended_text, TextType.TEXT),
                TextNode(prepend_text, TextType.TEXT),
                TextNode(BASE_ALT, TextType.IMAGE, BASE_SRC),
            ],
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

        prepend_text = "This text is PREPENDED"
        appended_text = "This text is APPENDED."

        self.assertListEqual(
            split_nodes_link([TextNode(prepend_text, TextType.TEXT)]),
            [TextNode(prepend_text, TextType.TEXT)],
        )

        self.assertListEqual(
            split_nodes_link(
                [
                    TextNode(prepend_text, TextType.TEXT),
                    TextNode(appended_text, TextType.TEXT),
                ]
            ),
            [
                TextNode(prepend_text, TextType.TEXT),
                TextNode(appended_text, TextType.TEXT),
            ],
        )

        self.assertListEqual(
            split_nodes_link([TextNode(create_url(), TextType.TEXT)]),
            [TextNode(BASE_TXT, TextType.LINK, BASE_URL)],
        )

        self.assertListEqual(
            split_nodes_link([TextNode(prepend_text + create_url(), TextType.TEXT)]),
            [
                TextNode(prepend_text, TextType.TEXT),
                TextNode(BASE_TXT, TextType.LINK, BASE_URL),
            ],
        )

        self.assertListEqual(
            split_nodes_link(
                [
                    TextNode(
                        prepend_text + create_url() + appended_text,
                        TextType.TEXT,
                    )
                ]
            ),
            [
                TextNode(prepend_text, TextType.TEXT),
                TextNode(BASE_TXT, TextType.LINK, BASE_URL),
                TextNode(appended_text, TextType.TEXT),
            ],
        )

        self.assertListEqual(
            split_nodes_link(
                [
                    TextNode(
                        prepend_text + create_url() + appended_text,
                        TextType.TEXT,
                    ),
                    TextNode(prepend_text, TextType.TEXT),
                    TextNode(create_url(), TextType.TEXT),
                ]
            ),
            [
                TextNode(prepend_text, TextType.TEXT),
                TextNode(BASE_TXT, TextType.LINK, BASE_URL),
                TextNode(appended_text, TextType.TEXT),
                TextNode(prepend_text, TextType.TEXT),
                TextNode(BASE_TXT, TextType.LINK, BASE_URL),
            ],
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )
