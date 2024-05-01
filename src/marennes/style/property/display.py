from typing import Optional, Literal
from . import Property

OutsideDisplay: Literal["block" | "inline" | "run-in"]
InsideDisplay: Literal["flow" | "flow-root" | "table" | "flex" | "grid" | "ruby"]
BlockDisplay: Literal["none" | 'contents']

_outside_values = ["block", "inline", "run-in"]
_inside_values = ["flow", "flow-root", "table", "flex", "grid", "ruby"]
_block_values = ["none", "contents"]

class Display(Property):
    outside: Optional[OutsideDisplay] = None
    inside: Optional[InsideDisplay] = None
    box: Optional[BlockDisplay] = None

    def __init__(self, value: str):
        super().__init__(value=value)

        self.box =  Display.parse_block(value)
        self.outside = Display.parse_outside(value)
        self.inside = Display.parse_outside(value)
    
    def defines_outside_display(self) -> bool:
        """ Return True if the display property has an outside display set. """
        return self.outside

    def defines_inside_display(self) -> bool:
        """ Return True if the display property has an inside display set. """
        return self.inside

    def __bool__(self) -> bool:
        """ Return False if the display is set to 'none'. """
        return not self.box == "none"

    @staticmethod
    def parse_outside(value: str) -> Optional[OutsideDisplay]:
        values = map(lambda s: s.strip(), value.split(" "))
        return next(filter(lambda v: v in _outside_values, values), default=None)      

    @staticmethod
    def parse_inside(value: str) -> Optional[InsideDisplay]:
        values = map(lambda s: s.strip(), value.split(" "))
        return next(filter(lambda v: v in _inside_values, values), default=None)   

    @staticmethod
    def parse_block(value: str) -> Optional[BlockDisplay]:
        values = map(lambda s: s.strip(), value.split(" "))
        return next(filter(lambda v: v in _block_values, values), default=None)   