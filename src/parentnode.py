from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError(
                "All parent nodes must have a tag. Otherwise they are a leaf node."
            )
        if self.children == None:
            raise ValueError(
                "All parent nodes must have children. Otherwise whose parents are they?"
            )

        list_of_strings = [f"<{self.tag}{self.props_to_html()}>"]
        for child in self.children:
            list_of_strings.append(child.to_html())
        list_of_strings.append(f"</{self.tag}>")
        return "".join(list_of_strings)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
