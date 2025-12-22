from classes.graph import Graph
from classes.vertex import Vertex
from gui.gui import App
import random
from gui.helper_functions.loadgraph import load_graph

# G = load_graph("new_graph.json")


def create_full_graph(n):
    graph = Graph()
    for i in range(n):
        vertex = Vertex(graph, [random.random(), random.random()], i)
        graph.add_vertex(vertex)
    
    for vertex1 in graph.vertices:
        for vertex2 in graph.vertices:
            vertex1.add_neighbour(vertex2)
    return graph

G = Graph()
vertex1 = Vertex(G, (0,0), 1)
vertex2 = Vertex(G, (0,1), 2)
vertex3 = Vertex(G, (1,0), 3)
vertex4 = Vertex(G, (1,1), 4)

vertex1.add_neighbour(vertex2)

vertex1.add_neighbour(vertex3)

vertex2.add_neighbour(vertex3)
vertex3.add_neighbour(vertex4)

G.add_vertex(vertex1)
G.add_vertex(vertex2)
G.add_vertex(vertex3)
G.add_vertex(vertex4)
G.save()


if __name__ == "__main__":
    app = App()
    app.run()
    G.save()