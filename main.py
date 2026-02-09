from classes.graph import Graph
from classes.vertex import Vertex
from gui.gui import App
import random
from gui.helper_functions.loadgraph import load_graph

# G = load_graph("new_graph.json")


def create_full_graph(n):
    graph = Graph(f"K{n}")
    for i in range(n):
        vertex = Vertex(graph, [random.random(), random.random()], {0: 's', 3: 't', 5: 'u'}.get(i,i))
        graph.add_vertex(vertex)
    
    for vertex1 in graph.vertices:
        for vertex2 in graph.vertices:
            vertex1.add_neighbour(vertex2)
    return graph

G = create_full_graph(10)
G.save()

G = Graph("test")

s = Vertex(G, (-1, -1), "s")
t = Vertex(G, (-1, 1), "t")
u = Vertex(G, (1, 1), "u")
v = Vertex(G, (0,0), '0')

G.add_vertex(s)
G.add_vertex(t)
G.add_vertex(u)
G.add_vertex(v)

v.add_neighbour(s)
v.add_neighbour(t)
v.add_neighbour(u)

G.save()

if __name__ == "__main__":
    app = App()
    app.run()