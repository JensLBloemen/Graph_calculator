from classes.graph import Graph
from classes.vertex import Vertex
from libs.operation import operation
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


start_graph = Graph()
l = 1 / 2 ** 0.5
s = Vertex(start_graph, (0,0), 's')
t = Vertex(start_graph, (-l,l), 't')
u = Vertex(start_graph, (l,l), 'u')

start_graph.add_vertex(s)
start_graph.add_vertex(t)
start_graph.add_vertex(u)

start_graph.add_edge((s,t))
start_graph.add_edge((u,t))
start_graph.add_edge((s,u))


def get_vampire(n):
    vampire = start_graph
    vampire.name = "vampire0"
    for i in range(n):
        vampire = operation(vampire, vampire)
        vampire.name = f"vampire{i+1}"
    return vampire

