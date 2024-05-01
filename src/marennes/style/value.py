from __future__ import annotations


def remove_unit(value: str, unit: str) -> str:
    return value.strip().removesuffix(unit).strip()


class Unit:
    def __init__(self, value: int | float, unit: str):
        self.value = value
        self.unit = unit

    def is_int(self) -> bool:
        return isinstance(self.value, int)

    def is_float(self) -> bool:
        return isinstance(self.value, float)

    def cast_to_integer(self) -> int:
        if self.is_int():
            return self.value
        else:
            return int(self.value)

    def cast_to_float(self) -> float:
        if self.is_float:
            return self.value
        else:
            return float(self.value)

    def is_relative(self) -> bool:
        return self.unit in ["em", "%"]

    def __str__(self):
        return f"{self.value} {self.unit}"


class Em(Unit):
    def __init__(self, value: str):
        super().__init__(
            value=value,
            unit="em",
            convert=float
        )


class Percentage(Unit):
    def __init__(self, value: str):
        super().__init__(
            value=value,
            unit="%",
            convert=lambda v: float(v) / 100.0
        )


class Pixel(Unit):
    def __init__(self, value: int):
        super().__init__(
            value=value,
            unit="px",
        )

    def __mul__(self, rhs: Em | Percentage) -> Pixel:
        return Pixel(
            value=int(float(self.value) * float(rhs.value))
        )


class Point:
    def __init__(self, value: float):
        super().__init__(
            value=value
        )

    def __mul__(self, rhs: Em | Percentage) -> Point:
        return Point(
            value=float(self.value) * float(rhs.value)
        )


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

