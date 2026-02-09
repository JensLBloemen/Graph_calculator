"""
Docstring for Classes.Graph
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from libs.chromaticpol import get_chromatic_polynomial
from copy import deepcopy
import json

# if TYPE_CHECKING:
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
            if vertex != nvert:
                self.edges.add(frozenset({vertex, nvert}))

    def add_edge(self, edge: tuple[Vertex, Vertex]) -> None:
        v1, v2 = edge
        v1.add_neighbour(v2)

    def delete_edge(self, edge: tuple[Vertex, Vertex]) -> None:
        if isinstance(edge, frozenset):
            e = edge
        else:
            u, v = edge
            e = frozenset({u, v})
        
        u, v = edge

        u.neighbours.discard(v)
        v.neighbours.discard(u)

        self.edges.discard(e)

    def contract_edge(self, edge:  tuple[Vertex, Vertex]) -> None:

        # edge is frozenset({u, v}) OR a 2-tuple (u, v)
        if isinstance(edge, frozenset):
            u, v = tuple(edge)
        else:
            u, v = edge

        # remove the edge itself (optional, but keeps edges tidy)
        self.delete_edge(frozenset({u, v}))

        v_neighbors = set(v.neighbours)  # copy
        self.delete_vertex(v)

        for neighbor in v_neighbors:
            if neighbor is not u:
                u.add_neighbour(neighbor)

    def delete_vertex(self, vertex: Vertex):
        neighbours = vertex.neighbours
        self.vertices.remove(vertex)
        for nvert in list(neighbours):
            self.delete_edge(frozenset({vertex, nvert}))
            nvert.neighbours.discard(vertex)
        self.ids.pop(vertex.id, None)

    def copy(self):
        new_graph = Graph(self.name)
        vertex_dict = dict()
        for vertex in self.vertices:
            new_vertex = Vertex(new_graph, vertex.location, vertex.id)
            new_graph.add_vertex(new_vertex)
            vertex_dict[vertex] = new_vertex

        for edge in self.edges:
            v1, v2 = edge
            new_graph.add_edge((vertex_dict[v1], vertex_dict[v2]))
        return new_graph

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
