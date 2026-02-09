from classes.graph import Graph
from classes.vertex import Vertex
from numpy import sin, cos, pi

def create_full_graph(n):
    graph = Graph(f"K{n}")
    for i in range(n):
        vertex = Vertex(graph, [cos(2*i*pi / n), sin(2*i*pi / n)], {0: 's', 1: 't', 2: 'u'}.get(i,i))
        graph.add_vertex(vertex)
    
    for vertex1 in graph.vertices:
        for vertex2 in graph.vertices:
            vertex1.add_neighbour(vertex2)
    return graph

