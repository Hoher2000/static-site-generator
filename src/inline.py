from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        if not len(split_nodes) % 2:
            raise Exception(f'Invalid Markdown syntax. Closing delimitter {delimiter} is not found in text of node "{node.text}"')
        for i in range(len(split_nodes)):
            if not i % 2:
                if split_nodes[i]:
                    new_nodes.append(TextNode(split_nodes[i], text_type_text))
            else:
                if split_nodes[i]:
                    new_nodes.append(TextNode(split_nodes[i], text_type))   
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        i = 0
        for item in re.split(r"!\[(.*?)\]\((.*?)\)", node.text):
            if item == images[i-1][1]:
                continue
            if item and item not in images[i]:
                new_nodes.append(TextNode(item, text_type_text))
                continue
            if item == images[i][0]:
                new_nodes.append(TextNode(images[i][0], text_type_image, images[i][1]))
                i += 1 if i < len(images) - 1 else 0         
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        i = 0
        for item in re.split(r"\[(.*?)\]\((.*?)\)", node.text):
            if item == links[i-1][1]:
                continue
            if item and item not in links[i]:
                new_nodes.append(TextNode(item, text_type_text))
                continue
            if item == links[i][0]:
                new_nodes.append(TextNode(links[i][0], text_type_link, links[i][1]))
                i += 1 if i < len(links) - 1 else 0          
    return new_nodes

def text_to_textnodes(text):
    split_nodes = [TextNode(text, text_type_text)]
    for i in (('**', text_type_bold), ('*', text_type_italic), ('`', text_type_code)):
        split_nodes = split_nodes_delimiter(split_nodes, *i)
    split_nodes = split_nodes_image(split_nodes)
    split_nodes = split_nodes_link(split_nodes)
    return split_nodes