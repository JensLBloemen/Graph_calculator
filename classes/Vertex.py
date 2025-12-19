"""
Docstring for Classes.Vertex
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.graph import Graph

SELF_LOOPS = False

class Vertex:
    def __init__(self, graph: Graph, location: tuple[int, int], id: int):
        self.location = location
        self.id = id
        self.parent = graph

        self.neighbours = set()

    def add_neighbour(self, other: Vertex) -> None:
        if self != other:
            self.neighbours.add(other)
            other.neighbours.add(self)
        elif SELF_LOOPS:
            self.neighbours.add(other)
            other.neighbours.add(self)


    @staticmethod
    def degree(self):
        return len(self.neighbours)
