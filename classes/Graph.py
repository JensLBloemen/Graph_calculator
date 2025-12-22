"""
Docstring for Classes.Graph
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from classes.vertex import Vertex


class Graph:
    def __init__(self, name: str = "new_graph"):
        if name.endswith(".json"):
            self.name = name[:-5]
        else:
            self.name = name

        self.vertices = set()
        self.edges = set()

    def add_vertex(self, vertex: Vertex) -> None:

        self.vertices.add(vertex)
        for nvert in vertex.neighbours:
            if (nvert, vertex) not in self.edges and vertex != nvert:
                self.edges.add((vertex, nvert))

    def save(self) -> None:
        vertex_data = dict()
        for vertex in self.vertices:
            vertex_data[vertex.id] = [vertex.location, [ver.id for ver in vertex.neighbours]]
        data = {
            "vertices": vertex_data,
        }

        json_str = json.dumps(data, indent=4)
        with open(f"graphs//{self.name}.json", "w") as f:
            f.write(json_str)