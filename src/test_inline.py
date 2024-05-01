import unittest
from inline import *
from textnode import *

class TestParsing(unittest.TestCase):
    def test_split_nodes(self):
        node1= TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is *a text* node", text_type_text)
        node3 = TextNode("This is `a text` node", text_type_text)
        node4 = TextNode("This is **a text** node", text_type_text)
        node5 = TextNode("*This* is *a text* node", text_type_text)
        node6 = TextNode("This is `a text node", text_type_text)
        self.assertEqual(split_nodes_delimiter([node1, node2], '*', text_type_italic),
                                                                [TextNode("This is a text node", text_type_bold),
                                                                 TextNode("This is ", text_type_text),
                                                                 TextNode("a text", text_type_italic),
                                                                 TextNode(" node", text_type_text)])
        self.assertEqual(split_nodes_delimiter([node3], '`', text_type_code),
                                                       [TextNode("This is ", text_type_text),
                                                       TextNode("a text", text_type_code),
                                                       TextNode(" node", text_type_text)])
        self.assertEqual(split_nodes_delimiter([node4], '**', text_type_italic),
                                                       [TextNode("This is ", text_type_text),
                                                       TextNode("a text", text_type_italic),
                                                       TextNode(" node", text_type_text)])
        self.assertEqual(split_nodes_delimiter([node5], '*', text_type_bold),
                                                       [TextNode("This", text_type_bold),
                                                       TextNode(" is ", text_type_text),
                                                       TextNode("a text", text_type_bold),
                                                       TextNode(" node", text_type_text)])
        
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        res = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")] 
        self.assertEqual(extract_markdown_images(text), res)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        res = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(text), res)

    def test_split_nodes_image(self):
        node = TextNode(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
        text_type_text)
        node2 = TextNode('hoher', text_type_bold)
        res = [
        TextNode("This is text with an ", text_type_text),
        TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        TextNode(" and another ", text_type_text),
        TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        TextNode('hoher', text_type_bold)]
        self.assertEqual(split_nodes_image([node, node2]), res)

    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
        text_type_text)
        node2 = TextNode('hoher', text_type_bold)
        res = [
        TextNode("This is text with an ", text_type_text),
        TextNode("image", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        TextNode(" and another ", text_type_text),
        TextNode("second image", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        TextNode('hoher', text_type_bold)]
        self.assertEqual(split_nodes_link([node, node2]), res)

    def test_text_to_textnodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)'
        res = [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ]
        self.assertEqual(text_to_textnodes(text), res)
        text2 = '`This is` **text** with an **italic** *word* an ![image2](https://storage.googleapis.com/hoher/zjjcJKZ.png) and a [link6](https://hoher.ru)'
        res2 = [
                TextNode("This is", text_type_code),
                TextNode(" ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_bold),
                TextNode(" ", text_type_text),
                TextNode("word", text_type_italic),
                TextNode(" an ", text_type_text),
                TextNode("image2", text_type_image, "https://storage.googleapis.com/hoher/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link6", text_type_link, "https://hoher.ru"),
            ]
        self.assertEqual(text_to_textnodes(text2), res2)

if __name__ == "__main__":
    unittest.main()
