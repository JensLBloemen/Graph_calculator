"""
Docstring for Classes.Vertex
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.Graph import Graph

class Vertex:
    def __init__(self, graph: Graph, location: tuple[int, int], id: int):
        self.location = location
        self.id = id
        self.parent = graph

        self.neighbours = set()

    def add_neighbour(self, other: Vertex) -> None:
        self.neighbours.add(other)
        other.neighbours.add(self)

    @staticmethod
    def degree(self):
        return len(self.neighbours)
