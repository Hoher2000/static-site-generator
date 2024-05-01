from textnode import *
from htmlnode import *
from inline import *


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    return [i.strip() for i in markdown.split('\n\n') if i.strip() != '']


def block_to_block_type(block):
    heading = [f"{'#' * i} " for i in range(1, 7)]
    if any([block.startswith(i) for i in heading]): return block_type_heading
    if block.startswith("'''") and block.endswith("'''"): return block_type_code
    multiline_block = block.splitlines()
    if all([line.startswith('>') for line in multiline_block]): return block_type_quote
    if all([line.startswith('*') or line.startswith('-') for line in multiline_block]): return block_type_unordered_list
    for i, j in enumerate(multiline_block, 1):
        if not j.startswith(f'{i}.'): break
    else: return block_type_ordered_list
    return block_type_paragraph

def markdown_to_html_node(markdown):

    def line_to_html_nodes(line):
        return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(line)]
    
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_quote:
            block = '\n'.join(line[1:].strip() for line in block.splitlines())
            children = line_to_html_nodes(block)
            block_nodes.append(ParentNode('blockquote', children, props=None))
        elif block_type == block_type_unordered_list:
            block = [line[1:].strip() for line in block.splitlines()]
            children = []
            for ul in block:
                children.append(ParentNode('li', line_to_html_nodes(ul), props=None))
            block_nodes.append(ParentNode('ul', children, props=None))
        elif block_type == block_type_ordered_list:
            block = [line.lstrip('1234567890. ') for line in block.splitlines()]
            children = []
            for ul in block:
                children.append(ParentNode('li', line_to_html_nodes(ul), props=None))
            block_nodes.append(ParentNode('ol', children, props=None))
        elif block_type == block_type_code:
            block = block[3:-3].strip()
            code_node = ParentNode('code', line_to_html_nodes(block), props=None)
            block_nodes.append(ParentNode('pre', [code_node], props=None))
        elif block_type == block_type_heading:
            counter, block = block.split(maxsplit=1)
            children = line_to_html_nodes(block)
            block_nodes.append(ParentNode(f'h{len(counter)}', children, props=None))
        else:
            children = line_to_html_nodes(block)
            block_nodes.append(ParentNode('p', children, props=None))
    return ParentNode("div", children=block_nodes)     

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines: 
        if line.startswith('#') and line[:2].count('#') == 1:
            h1 = line[1:].strip()      
            break
    else:  
        raise Exception('Invalid markdown: h1 header is not found')
    return h1