"""
Docstring for gui.helper_functions.loadgraph
"""
import json
from classes.graph import Graph
from classes.vertex import Vertex
from gui.helper_functions import FILEPATH

def load_graph(name):
    graph_data = open(FILEPATH+name, 'r')
    out = json.load(graph_data)
    vertex_data = out["vertices"]
    vertex_dict = dict()

    graph = Graph(name)

    for vertex in vertex_data:
        vertex_dict[int(vertex)] = Vertex(graph, tuple(vertex_data[vertex][0]), int(vertex))

    for vertex in vertex_data:
        for j in vertex_data[vertex][1]:
            vertex_dict[int(vertex)].add_neighbour(vertex_dict[j])

    for vertex_id in vertex_dict:
        graph.add_vertex(vertex_dict[vertex_id])


    return graph



