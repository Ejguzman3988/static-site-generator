from typing import Self
import unittest

from blocktype import (
    CODE,
    HEADING,
    ORDERED_LIST,
    PARAGRAPH,
    QUOTE,
    UNORDERED_LIST,
    block_to_block_type,
)


def test_helper(self, answer, paragraph, non_paragraph):
    for test_case in paragraph:
        msg = f"{test_case} failed"
        self.assertEqual(block_to_block_type(test_case), PARAGRAPH, msg=msg)
    for test_case in non_paragraph:
        msg = f"{test_case} failed"
        self.assertEqual(block_to_block_type(test_case), answer, msg=msg)


class TestBlockNode(unittest.TestCase):

    def test_block_node_oredred_list(self):
        paragraph = [
            """ """,
            """11. a""",
            """111. a\n112. b""",
            """1. a\n112. b""",
            """1. a\n2. """,
            """1. a\n 2. b""",
            """1. a\n 3. b""",
        ]
        non_paragraph = [
            """1. a""",
            """1. 2\n2. 45 """,
            """1. 2\n2. 45\n3. test\n4. a\n5. v\n6. a\n7. b\n8. a\n9. b\n10. test """,
        ]
        test_helper(self, ORDERED_LIST, paragraph, non_paragraph)

    def test_block_node_unoredred_list(self):
        paragraph = ["""-""", """--""", """-1""", """- b\n-"""]
        non_paragraph = ["""- """, """- 2""", """- 1\n- 1""", """- 1\n- """]
        test_helper(self, UNORDERED_LIST, paragraph, non_paragraph)

    def test_block_node_quote(self):
        paragraph = ["""a>""", """a> """, """> a\n> test\nnope"""]
        non_paragraph = ["""> a""", """> a\n> test""" """> a\n> test"""]
        test_helper(self, QUOTE, paragraph, non_paragraph)

    def test_block_node_code(self):
        paragraph = [
            """aH""",
            """`""",
            """``""",
            """```""",
            """```a""",
            """```a`""",
            """```a``""",
            """```aa``""",
            """``````""",
        ]
        non_paragraph = [
            """```aa```""",
            """```
            ```""",
        ]

        test_helper(self, CODE, paragraph, non_paragraph)

    def test_block_node_heading(self):
        paragraph = ["""a#""", """#""", """##""", """## """, """####### 1"""]

        non_paragraph = ["""# 1""", """## 1""", """### 1"""]

        test_helper(self, HEADING, paragraph, non_paragraph)


if __name__ == "__main__":
    unittest.main()
