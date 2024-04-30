from __future__ import annotations

class Unit:
    def __init__(self, value: str, unit: str, convert):
        self.raw = value
        self.value = convert(value.strip().removesuffix(unit).strip())
        self.unit = unit
    
    def is_relative(self) -> bool:
        return self.unit in ["em", "%"]
    
    def __str__(self):
        return self.raw

class Em(Unit):
    def __init__(self, value: str):
        super().__init__(value=value, unit="em", float)

class Percentage(Unit):
    def __init__(self, value: str):
        super().__init__(value=value, unit="%", lambda v: float(v) / 100.0)

class Pixel:
    def __init__(self, value: str):
        super().__init__(value=value, unit="px", int)

def parse_value(value: str) -> Value:
    if "em" in value:
        return Em(value)
    elif "%" in value:
        return Percentage(value)
    elif "px" in value:
        return Pixel(value)
    else:
        return value

Value = Em | Percentage | Pixel | str | float | int