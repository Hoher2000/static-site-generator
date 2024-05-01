class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        if self.props is None: return ''
        string_item = (f' {key}="{value}"' for key, value in self.props.items())
        return ''.join(string_item)   
    
    def __repr__(self) -> str:
        return f'HTMLNode\ntag: {self.tag}\nvalue: {self.value}\nchidren: {self.children}\nprops: {self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self) -> str:
        return f'LeafNode\ntag: {self.tag}\nvalue: {self.value}\nprops: {self.props}'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)  

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")   
        if not self.children:
            raise ValueError("Invalid parent HTML: no children")
        child_to_html = ''.join([child.to_html() for child in self.children])
        return f'<{self.tag}{self.props_to_html()}>{child_to_html}</{self.tag}>'

    def __repr__(self) -> str:
        return f'ParentNode (tag: {self.tag}\nchildren: {self.children}\nprops: {self.props}'   