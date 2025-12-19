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
        self.name = name
        self.vertices = set()

    def add_vertex(self, vertex: Vertex) -> None:
        self.vertices.add(vertex)

    def save(self) -> None:
        vertex_data = dict()
        for vertex in self.vertices:
            vertex_data[vertex.id] = [ver.id for ver in vertex.neighbours]
        data = {
            "vertices": vertex_data,
        }

        json_str = json.dumps(data, indent=4)
        with open(f"graphs//{self.name}.json", "w") as f:
            f.write(json_str)