from classes.graph import Graph
from classes.vertex import Vertex
from gui.gui import App
import random
from gui.helper_functions.loadgraph import load_graph

# G = load_graph("new_graph.json")


def create_full_graph(n):
    graph = Graph(f"K{n}")
    for i in range(n):
        vertex = Vertex(graph, [random.random(), random.random()], i)
        graph.add_vertex(vertex)
    
    for vertex1 in graph.vertices:
        for vertex2 in graph.vertices:
            vertex1.add_neighbour(vertex2)
    return graph

G = create_full_graph(9)
G.save()



if __name__ == "__main__":
    app = App()
    app.run()