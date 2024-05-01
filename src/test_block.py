import unittest
from block import *


class TestBlock(unittest.TestCase):
    def test_to_blocks(self):
        markdown = '''\n This is **bolded** paragraph     \n\n    \n\n     This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items\n\n\n\n\n'''
        res = [
            'This is **bolded** paragraph',
            'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line',
            '* This is a list\n* with items']
        self.assertEqual(markdown_to_blocks(markdown), res)

    def test_block_type(self):
        block1 = "'''x == 12'''"
        self.assertEqual(block_to_block_type(block1), block_type_code)
        block2 = "'''x == 12"
        self.assertNotEqual(block_to_block_type(block2), block_type_code)
        block3 = "# Heading"
        self.assertEqual(block_to_block_type(block3), block_type_heading)
        block4 = "######## Heading"
        self.assertNotEqual(block_to_block_type(block4), block_type_heading)
        block5 = "###### Heading"
        self.assertEqual(block_to_block_type(block5), block_type_heading)
        block6 = "#Heading"
        self.assertNotEqual(block_to_block_type(block6), block_type_heading)
        block7 = '>123\n>13\n>ert'
        self.assertEqual(block_to_block_type(block7), block_type_quote)
        block8 = '>123\n13\n>ert'
        self.assertNotEqual(block_to_block_type(block8), block_type_quote)
        block9 = '*123\n-13\n*ert'
        self.assertEqual(block_to_block_type(block9), block_type_unordered_list)
        block10 = '>123\n-13\n*ert'
        self.assertNotEqual(block_to_block_type(block10), block_type_unordered_list)
        block11 = '1.123\n2.13\n3ert'
        self.assertNotEqual(block_to_block_type(block11), block_type_ordered_list)
        block12 = '1.123\n2.13\n3.ert'
        self.assertEqual(block_to_block_type(block12), block_type_ordered_list)
        block13 = '1.123\n2.13\n3ert'
        self.assertEqual(block_to_block_type(block13), block_type_paragraph)
        
    def test_extract_title(self):
        md1 = '1234\n1234\n# 1234'
        md2 = '# $1234\n1234\n# 1234'
        md3 = '1234\n#  hoher\n## 1234'
        self.assertEqual(extract_title(md1), '1234')
        self.assertEqual(extract_title(md2), '$1234')
        self.assertEqual(extract_title(md3), 'hoher')

if __name__ == "__main__":
    unittest.main()