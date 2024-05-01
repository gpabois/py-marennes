from typing import Callable
from collections.abc import Iterator

class Selector:
    def select(self, node: H.Node) -> Iterator[H.Node]:
        raise NotImplementedError("A selector must implement select(node: html.Node) -> Iterator[H.Node]")

    def __call__(self, node: H.Node) -> Iterator[H.Node]:
        yield from self.select(node)

class SimpleSelector:
    """ A simple selector based on a predicate. """
    def __init__(self, predicate: Callable[[H.Node], bool])
        self.predicate = predicate

    def select(self, node: H.Node) -> Iterator[H.Node]:
        if self.predicate(node):
            yield node

    def by_tag(tag: str) -> Selector:
        return SimpleSelector(lambda n: n.tag == tag)

    def by_class(cls: str) -> Selector:
        return SimpleSelector(lambda n: cls in n.get("classes", []))
    
    def by_id(id: str) -> Selector:
        return SimpleSelector(lambda n: id == in n.get("id", ""))

def by(attr_name: str, value: any) -> Selector:
    if attr_name == "class":
        return SimpleSelector(lambda n: value in n.get("classes", []))
    
    return SimpleSelector(lambda n: value == in n.get("id", None))
