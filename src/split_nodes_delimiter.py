from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter == "**" and delimiter in node.text:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("unmatched delimiter")
            split_node = node.text.split(delimiter)
            for i, text in enumerate(split_node):
                if text == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
            return new_nodes
        if delimiter == "_" and delimiter in node.text:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("unmatched delimiter")
            split_node = node.text.split(delimiter)
            for i, text in enumerate(split_node):
                if text == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
            return new_nodes
        if delimiter == "`" and delimiter in node.text:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("unmatched delimiter")
            split_node = node.text.split(delimiter)
            for i, text in enumerate(split_node):
                if text == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
            return new_nodes
        else:
            raise Exception("no matched delimiter found")