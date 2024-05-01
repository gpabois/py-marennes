from typing import Callable
from collections.abc import Iterator

from pymarennes import html as H
from .selector import Selector, by

class Declaration: 
    """ A CSS property declaration """
    def apply(self, node: H.Node, style: Style):
        raise NotImplementedError("Declaration requires to implement apply(node: H.Node)")

    def __call__(self, node: H.Node):
        return self.apply(node, node.style)

class SimpleDeclaration(Declaration):
    name: str
    value: str

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def apply(self, node: H.Node, style: Style):
        self[name].from_raw(self.value)

def apply(self, name: str, value: str) -> Declaration:
    return SimpleDeclaration(name=name, value=value)