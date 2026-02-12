"""
Docstring for Classes.Vertex
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.graph import Graph

SELF_LOOPS = False

class Vertex:
    def __init__(self, graph: Graph, location: tuple[float, float], id: str):
        self.location: tuple[float, float] = location
        self.id: str = str(id)
        self.parent: Graph = graph
        self.neighbours: set[Vertex] = set()

    def change_id(self, id):
        if id in self.parent.ids:
            return
        self.parent.ids[id] = self.parent.ids.pop(self.id)
        self.id = id

    def add_neighbour(self, other: Vertex) -> None:
        if self != other:
            self.neighbours.add(other)
            if self not in other.neighbours:
                other.add_neighbour(self)
            self.parent.edges.add(frozenset({self, other}))
        elif SELF_LOOPS:
            self.neighbours.add(other)
            other.neighbours.add(self)


    @property
    def degree(self):
        return len(self.neighbours)
