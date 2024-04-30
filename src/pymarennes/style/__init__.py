from typing import Callable
from collections.abc import Iterator

from .. import html as H
from .selector import Selector, by
from .declaration import Declaration, apply
from .rule import rule, Rule

from .value import Value, Em, Percentage, parse_value
from .display import Display
from .color import Color

class StyleSheet:
    def __init__(self, *rules: Iterator[Rule]):
        self.rules = list(rules)
    
    def apply(self, node: H.Node):
        """ Apply styles to the html node. """

        for rule in self.rules:
            rule(node)

class Property:
    raw: str
    
    initial: Value
    value: Value
    computed: Value
    used: Value
    
    def __init__(self, raw: str) -> str:
        self.raw = raw
        self.initial = parse_value(value)
        self.computed   = None
        self.used       = None
        self.actual     = None
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}: {self.value}"

    def inherits(self) -> bool:
        """ Return True if the property inherits its value from the parent's style. """
        return self.value == "inherit"

class Style:
    def __init__(self, display: Optional[Display] = None):
        self.display = display or Display()
        
        # Font
        # TODO: font-style
        # TODO: font-variant
        # TODO: font-weight
        # TODO: font-stretch
        # TODO: font-size
        # TODO: line-height
        # TODO: font-family

        # Background properties:
        # TODO: background-attachment
        # TODO: background-clip
        # TODO: background-image
        # TODO: background-origin
        # TODO: background-position
        # TODO: background-repeat
        # TODO: background-size
        self.background_color = Color()

    def __iter__(self) -> Iterator[(str, Property)]:
        properties = [
            "display",
            "background-color"
        ]

        for name in self.properties:
            yield name, self[name]

    def __getitem__(self, name: str) -> Property:
        return getattr(self, name.replace("-", "_"))

def apply_rules(node: H.Node, sheet: StyleSheet):
    stack = [node]
    
    while stack:
        node = stack.pop()
        sheet.apply(node)
        stack += list(iter(node))

_layout_dependant_properties = [
    "margin-left",
    "margin-right",
    "margin-top",
    "margin-bottom",

    "padding-left",
    "padding-right",
    "padding-top",
    "padding-bottom",   

    "top",
    "bottom",
    "right",
    "left",

    "text-ident",

    "width",
    "max-width",
    "min-width",

    "height",
    "max-height",
    "min-width"
]
""" Those properties depends on the layout if their values are relatives. """

def compute_properties(parent: H.Node, sheet: StyleSheet):
    """ Compute the properties, called after apply_rules

        - Compute values for inherit, initial, revert, revert-layer and unset.
    """

    for node in parent:
        for name, prop in node:
            if prop.inherits():
                node[name].computed = parent[name].computed
                continue

            # We have a relative value (em, or %)
            # If the property's value depends on the layout step, we don't compute it.
            if prop.has_relative_value() and name in :
                prop.is_relative()
