import random
from classes.graph import Graph
from classes.vertex import Vertex

from libs.chromaticpol import get_chromatic_polynomial, get_all_chromatic_polynomials

## Create random graphs
def test1():

    def random_graph(n: int, m: int) -> Graph:
        # create random graph on n+3 vertices, m edges duplicates allowed

        G = Graph(f"test n={n}, m={m}")
        s = Vertex(G, [random.random(), random.random()], 's')
        t = Vertex(G, [random.random(), random.random()], 't')
        u = Vertex(G, [random.random(), random.random()], 'u')

        G.add_vertex(s)
        G.add_vertex(t)
        G.add_vertex(u)

        vertices = [s, t, u]

        for _ in range(n):
            v = Vertex(G, [random.random(), random.random()], 0)
            G.add_vertex(v)
            vertices.append(v)
        
        for _ in range(m):
            v1 = random.choice(vertices)
            v2 = random.choice(vertices)
            G.add_edge((v1, v2))

        return G

    for _ in range(50):

        n = random.randint(0, 20)
        m = random.randint(0, 15)
        G = random_graph(n, m)
        assert sum(get_all_chromatic_polynomials(G)) == get_chromatic_polynomial(G)
        # print("Passed test", n, m)

test1()
print("Passed all tests")