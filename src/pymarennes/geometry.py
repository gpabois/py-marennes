from __future__ import annotations
from typing import Optional, TypeVar, Generic
import itertools

class Vec2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter([self.x, self.y])   

    def __add__(self, rhs: Vec2D) -> Vec2D:
        return Vec2D(
            x=self.x + rhs.x,
            y=self.y + rhs.y
        )

Position = Vec2D

class Area:
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height

    def sum(self, *edges: list[Edge]) -> Area:
        return itertools.accumulate(edges, initial=self)

    
    def __add__(self, edge: Edge) -> Area:
        return Area(
            width=self.width + edge.left + edge.right,
            height=self.height + edge.top + edge.bottom
        )
        
class Rectangle:
    def __init__(self, position: Position, area: Area):
        self.position = position
        self.area = Area

class Edge:
    def __init__(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

class Box:
    """ Modèle de boîte de la norme CSS """
    def __init__(self, 
            content: Optional[Rectangle] = None, 
            padding: Optional[Edge] = None, 
            border: Optional[Edge] = None, 
            margin: Optional[Edge] = None):
            
        self.content: content or Rectangle()
        self.padding: Edge = padding or Edge()
        self.border: Edge = border or Edge()
        self.margin: Edge = margin or Edge()

    def outer(self) -> Area:
        return self.content.sum(self.padding, self.border, self.margin)
