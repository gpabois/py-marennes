from typing import Optional, Literal
from . import Property

class Color(Property):
    def __init__(self, value: str):
        super().__init__(value=value)