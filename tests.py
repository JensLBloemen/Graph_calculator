import random
from classes.graph import Graph
from classes.vertex import Vertex
from libs.special_graphs import get_vampire

from polys import get

from libs.chromaticpol import get_chromatic_polynomial, get_all_chromatic_polynomials
from libs.operation import operation

## Create random graphs
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



def test1():
    for i in range(50):

        n = random.randint(0, 20)
        m = random.randint(0, 15)
        G = random_graph(n, m)
        assert sum(get_all_chromatic_polynomials(G)) == get_chromatic_polynomial(G)
        print(f"Passed test{i}/50")

def test2():
    v0 = get_vampire(0)
    p0 = get_all_chromatic_polynomials(v0)

    v1 = get_vampire(1)
    p1 = get_all_chromatic_polynomials(v1)

    v2 = get_vampire(2)
    p2 = get_all_chromatic_polynomials(v2)

    v3 = get_vampire(3)
    p3 = get_all_chromatic_polynomials(v3)


    v12 = operation(v2, v3)
    print(f"edges: {len(v12.edges)}")

    assert get_all_chromatic_polynomials(v12) ==  get(p2, p3)

    print()
    print()

test1()
test2()
print("Passed all tests")