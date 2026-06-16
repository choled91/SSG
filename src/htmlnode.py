from Block_type import markdown_to_blocks, block_to_block_type, BlockType
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result +=f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is required")
        if self.tag is None:
            return self.value
        if self.props:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        if self.props:
            return f"LeafNode({self.tag}, {self.value}, {self.props})"
        else:
            return f"LeafNode({self.tag}, {self.value})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required")
        if self.children is None:
            raise ValueError("Children is required")
        else:
            children_html = ""
            for child in self.children:
                children_html +=child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type is BlockType.PARAGRAPH:
            block_node = ParentNode("p", text_to_children(block.replace("\n", " ")))
            block_nodes.append(block_node)
        if block_type is BlockType.HEADING:
            n = 0
            for char in block:
                if char == "#":
                    n +=1
                else:
                    break
            block_node = ParentNode(f"h{n}", text_to_children(block[n + 1:]))
            block_nodes.append(block_node)
        if block_type is BlockType.QUOTE:
            block_node = ParentNode("blockquote", text_to_children(block.removeprefix("> ")))
            block_nodes.append(block_node)
        if block_type is BlockType.UNORDERED_LIST:
            block_list = []
            for i in block.split("\n"):
                block_list.append(ParentNode("li", text_to_children(i.removeprefix("- "))))
            block_node = ParentNode("ul", block_list)
            block_nodes.append(block_node)
        if block_type is BlockType.ORDERED_LIST:
            block_list = []
            for i, line in enumerate(block.split("\n"), start=1):
                block_list.append(ParentNode("li", text_to_children(line.removeprefix(f"{i}. "))))
            block_node = ParentNode("ol", block_list)
            block_nodes.append(block_node)
        if block_type is BlockType.CODE:
            block_text = "\n".join(block.split("\n")[1:-1])
            text_node = TextNode(block_text + "\n", TextType.CODE)
            block_node = ParentNode("pre", [text_node_to_html_node(text_node)])
            block_nodes.append(block_node)
    block_parent = ParentNode("div", block_nodes)
    return block_parent