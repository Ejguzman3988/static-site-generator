import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    global sample_prop
    global child_node
    global child_node_no_tag
    global child_node_props
    global parent_node
    global parent_node_props

    sample_prop = {"href": "https://www.google.com"}
    child_node = LeafNode("span", "child")
    child_node_no_tag = LeafNode(
        "span",
        "child",
    )
    child_node_props = LeafNode("a", "child", sample_prop)
    parent_node = ParentNode("div", [child_node])
    parent_node_props = ParentNode("a", [child_node], sample_prop)

    def test_to_html_with_children(self):
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
