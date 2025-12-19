from classes.graph import Graph
from classes.vertex import Vertex


def create_full_graph(n):
    graph = Graph()
    for i in range(n):
        vertex = Vertex(graph, [i, 1], i)
        graph.add_vertex(vertex)
    
    for vertex1 in graph.vertices:
        for vertex2 in graph.vertices:
            vertex1.add_neighbour(vertex2)
    return graph


if __name__ == "__main__":
    g = create_full_graph(5)

    g.save()