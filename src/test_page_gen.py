import unittest

from copy_static_files import generate_page
from markdown import extract_title, markdown_to_blocks, markdown_to_html_node


class TestGenPage(unittest.TestCase):
    def test_print_message(self):
        page = generate_page()
        self.assertEqual(page, None)
