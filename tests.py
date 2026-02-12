import random
from sys import stdout
from classes.graph import Graph
from classes.vertex import Vertex

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
    print("Checking whether sum of chromatic vector equals polynomial:")
    for i in range(1, 51):

        n = random.randint(0, 20)
        m = random.randint(0, 15)
        G = random_graph(n, m)
        try:
            assert sum(get_all_chromatic_polynomials(G)) == get_chromatic_polynomial(G)
        except AssertionError:
            G.name = "TestFail"
            G.save()
        except Exception as e:
            print("Failure ", e)
            raise RuntimeError
             
        message = f"Passed test: [{'-'*((i*40)//50)+' '*(40 - (i*40)//50)}]  {i}/50"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()
    stdout.write('\n')
        

def test2():
    print("Checking formulas")
    for i in range(1, 51):
        n = random.randint(0, 20)
        m = random.randint(0, 13)
        G1 = random_graph(n, m)
        p1 = get_all_chromatic_polynomials(G1)

        n = random.randint(0, 20)
        m = random.randint(0, 13)
        G2 = random_graph(n, m)
        p2 = get_all_chromatic_polynomials(G2)

        H = operation(G1, G2)
        try:
            assert get_all_chromatic_polynomials(H) ==  get(p1, p2)
        except:
            G1.name = "Failure2_1"
            G1.save()

            G2.name = "Failure2_2"
            G2.save()

            H.name = "Failure2_3"
            H.save()
            raise AssertionError


        message = f"Passed test: [{'-'*((i*40)//50)+' '*(40 - (i*40)//50)}]  {i}/50"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()


if __name__ == "__main__":
    test1()
    test2()