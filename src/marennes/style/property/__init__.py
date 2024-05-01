from .. import Value, parse_value

from .display import Display
from .font import FontWeight
from .color import Color


class Property:
    raw: str

    initial: Value
    value: Value
    computed: Value
    used: Value

    def __init__(self, raw: str) -> str:
        self.raw = raw
        self.initial = parse_value(raw)
        self.computed = None
        self.used = None
        self.actual = None

    def __repr__(self) -> str:
        return f"{type(self).__name__}: {self.value}"

    def inherits(self) -> bool:
        """ Return True if the property inherits its value from the parent's style. """
        return self.value == "inherit"
