from collections.abc import Iterator, Iterable
from itertools import chain
from . import style as S

class Node:
    tag: str
    children: list[Node]
    style: S.Style()

    def __init__(self, tag: str, *children: Iterable[Iterator[Node | str]]):
        self.tag = tag
        self.children = list(map(Node.ensure, chain(*children)))
        self.style = S.Style()

    @staticmethod
    def ensure(node_or_str: str | Node) -> Node:
        if isinstance(node_or_str, str):
            return Text(text=node_or_str)

        return node_or_str

    def __iter__(self) -> Iterator[Node]:
        return iter(self.children)

    def is_text(self) -> bool:
        return isinstance(self, Text)

    def is_element(self) -> bool:
        return isinstance(self, Element)

    def set_style(self, style: S.Style) -> Node:
        self.style = style
        return self

    def get(self, key: str) -> any:
        return None

class Text(Node):
    def __init__(self, text: str):
        super().__init__(tag="#text")
        self.text = text

class Element(Node):
    def __init__(self, tag: str, attributes: dict[str, any], *children: Iterable[Iterator[Node | str]]):
        super().__init__(self, tag, *children):
        self.attributes = attributes

    def get(self, key: str, default=None) -> any:
        if key == "tag":
            return self.tag

        return self.attributes[key] if key in self.attributes else default
        
def e(tag: str, attributes: dict[str, any], *children: Iterable[Iterator[Node | str]]) -> Element:
    return Element(tag, attributes, *children)