"""
Docstring for Classes.Graph
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from libs.chromaticpol import get_chromatic_polynomial
from copy import deepcopy
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

        self.ids = dict()

    def add_vertex(self, vertex: Vertex) -> None:


        self.vertices.add(vertex)
        while vertex.id in self.ids:
            vertex.id += 1

        self.ids[vertex.id] = vertex

        for nvert in vertex.neighbours:
            if (nvert, vertex) not in self.edges and vertex != nvert:
                self.edges.add((vertex, nvert))

    def delete_edge(self, edge: tuple[Vertex, Vertex]) -> None:
        u, v = edge
        if (u, v) not in self.edges:
            u, v = v, u
        if (u, v) not in self.edges:  ## Edge does not exist
            return
        self.edges.remove((u, v))

    def contract_edge(self, edge:  tuple[Vertex, Vertex]) -> None:
        ## Self-loops become important!!
        return




    def delete_vertex(self, vertex: Vertex):
        neighbours = vertex.neighbours
        self.vertices.remove(vertex)
        for nvert in neighbours:
            if (vertex, nvert) in self.edges:
                self.edges.remove((vertex, nvert))
            else:
                self.edges.remove((nvert, vertex))
            nvert.neighbours.remove(vertex)

    def copy(self):
        return deepcopy(self)

    @property
    def chromatic_polynomial(self):
        return get_chromatic_polynomial(self)


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
