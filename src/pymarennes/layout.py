from __future__ import annotations
from typing import Optional, Literal

from . import geometry as G
from . import html as H

BoxNodeType = Literal["block" | "inline"]

_outside_display_indirection = {
    'block': build_block_box_node,
    'inline': build_inline_box_node
}

class BoxNode:
    source: Optional[H.Node]

    """ Box tree node """
    def __init__(self, type: BoxNodeType, source: Optional[H.Node] = None, children: Optional[Iterable[BoxNode]] = None):
        self.type = type
        self.source = source
        self.box: G.Box = G.Box()
        self.children: list[BoxNode] = list(children) if children else []

    def is_text_sequence(self) -> bool:
        return isinstance(self, TextSequence)

    def is_anonymous(self) -> bool:
        return not self.source

    def is_block(self) -> bool:
        return self.type == "block"

    def is_inline(self) -> bool:
        return self.type == "inline"

    def append_child(self, node: BoxNode):
        self.children.append(node)

    def __iter__(self) -> Iterator[BoxNode]:
        return iter(self.children)

class TextSequence(BoxNode):
    def __init__(self, text: str, source: Optional[H.Text]):
        super().__init__(self, type="inline", source=source)
        self.text = text

def iter_chunk_by_types(nodes: Iterator[BoxNode]) -> Iterator[(BoxNodeType, list[BoxNode])]:
    """ Generate a serie of chunks of the same type. """
    first = next(nodes, None)
    
    if not first:
        return

    typ = first.type
    group = [first]

    while (node := next(nodes, None)) is not None:
        if node.type != typ:
            yield (typ, group)
            typ = node.type
            group = [node]
        else:
            group.append(node)

    if group:
        yield (typ, group)

def has_block_box(nodes: Iterable[BoxNode]) -> bool:
    return any(lambda n: n.is_block(), nodes)

def remove_none_boxes(node: Iterator[BoxNode | None]) -> Iterator[BoxNode]:
    return filter(__bool__, map(build_box_tree, iter(h_node)))

def ensure_anonymous_block_boxes_for_inline_boxes(nodes: Iterator[BoxNode]) -> Iterator[BoxNode]:
    """
        > If a block container box (such as that generated for the DIV above) 
        > has a block-level box inside it (such as the P above), 
        > then we force it to have only block-level boxes inside it. 
        
        Source : https://www.w3.org/TR/CSS22/visuren.html#anonymous-block-level
    """
    nodes = list(filter(__bool__, map(build_box_tree, iter(h_node))))
    
    if has_block_box(nodes):
        for (box_type, boxes) in iter_chunk_by_types(iter(nodes)):
            if box_type == "inline":
                yield BlockNode(type="block", children=boxes)
            else:
                yield from boxes

def ensure_anonymous_inline_boxes(nodes: Iterator[BoxNode]) -> Iterator[BoxNode]:
    """ 
        > Any text that is directly contained inside a block container element (not inside an inline element) 
        > must be treated as an *anonymous inline element*. 

        Source: https://www.w3.org/TR/CSS22/visuren.html#anonymous
    """
    for node in nodes:
        if node.is_text_sequence():
            node.source = None
            node.type = "inline"
        
        yield node

def build_block_box_node(h_node: H.Node) -> BoxNode:
    children = build_box_nodes(h_node)
    children = ensure_anonymous_inline_boxes(children)
    children = ensure_anonymous_block_boxes_for_inline_boxes(children)
    
    return BoxNode(type="block", source=h_node, children=children)

def build_inline_box_node(h_node: H.Node) -> BoxNode:
    """ Creates a box in a inline formatting context. """
    children = build_box_nodes(h_node)
    return BoxNode(type="inline", source=h_node, children=children)

def build_box_nodes(nodes: Iterator[H.Node]) -> Iterator[BoxNode]:
    return remove_none_boxes(map(build_box_tree, nodes))

def build_box_tree(h_node: H.Node, parent: Optional[BoxNode]) -> Optional[BoxNode]:
    style = h_node.style
    display = style.display

    if h_node.is_text():
        return TextSequence(text=h_node.text, source=h_node)

    # Display is set to 'none'
    if not display:
        return None
    
    # Normal flow
    if display.defines_outside_display():
        return _outside_display_indirection[display.outside](h_node, parent=parent)        
    
    raise NotImplementedError("Unimplemented layout building for element with display: '{display}'.")

def build_fragment_tree(root: H.Node, containing_block: G.Rectangle):
    pass
  
    



