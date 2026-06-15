import random
from sys import stdout
from classes.graph import Graph
from classes.vertex import Vertex

from polys import get_triangle, get_star

from libs.chromaticpol import get_chromatic_polynomial, get_all_chromatic_polynomials
from libs.operations import triangle, star
from libs.effectiveinteractions import effectiveInteractionTriangle, effectiveInteractionStar

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



def test1(N = 50):
    print("Testing whether sum of chromatic vector equals polynomial:")
    for i in range(1, 1+N):

        n = random.randint(0, 20)
        m = random.randint(0, 15)
        G = random_graph(n, m)
        try:
            assert sum(get_all_chromatic_polynomials(G)) == get_chromatic_polynomial(G)
        except AssertionError:
            G.name = "TestFail"
            G.save()
            raise AssertionError
             
        message = f"Passed test: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()
    stdout.write('\n')
        

def test2(N = 50):
    print("Testing recursion for chromatic polynomial, triangle")
    for i in range(1, 1 + N):
        n = random.randint(0, 20)
        m = random.randint(0, 13)
        G1 = random_graph(n, m)
        p1 = get_all_chromatic_polynomials(G1)

        n = random.randint(0, 20)
        m = random.randint(0, 13)
        G2 = random_graph(n, m)
        p2 = get_all_chromatic_polynomials(G2)

        H = triangle(G1, G2)
        try:
            assert get_all_chromatic_polynomials(H) ==  get_triangle(p1, p2)
        except AssertionError:
            G1.name = "Failure2_1"
            G1.save()

            G2.name = "Failure2_2"
            G2.save()

            H.name = "Failure2_3"
            H.save()
            raise AssertionError


        message = f"Passed test: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()
    stdout.write("\n")


def test3(N = 50):
    print("Testing effective edge interactions, triangle")
    for i in range(1, 1+N):
        n = random.randint(0, 20)
        m = random.randint(0, 9)
        G1 = random_graph(n, m)
        pG1 = get_all_chromatic_polynomials(G1)

        n = random.randint(0, 20)
        m = random.randint(0, 9)
        G2 = random_graph(n, m)
        pG2 = get_all_chromatic_polynomials(G2)

        
        q = complex(random.random()+1, random.random()+1) # in shifted unit square  

        chi123 = pG1[-1].eval(q)
        y1 = tuple(p.eval(q) / chi123 * (q - 2) for p in pG1[:4])

        chi123 = pG2[-1].eval(q)
        y2 = tuple(p.eval(q) / chi123 * (q - 2) for p in pG2[:4])


        H = triangle(G1, G2)
        pH = get_all_chromatic_polynomials(H)
        chi123 = pH[-1].eval(q)
        y3 = tuple(p.eval(q) / chi123 * (q - 2) for p in pH[:4])

        new_y = effectiveInteractionTriangle(y1, y2, q)

        for j in range(4):
            assert round(new_y[j].real, 5) == round(y3[j].real, 5), (y3, new_y)
            assert round(new_y[j].imag, 5) == round(y3[j].imag, 5), (y3, new_y)
        
        message = f"Passed test: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()
    stdout.write("\n")
        

def test4(N = 50):
    print("Testing recursion for chromatic polynomial, star")
    for i in range(1, 1 + N):
        n = random.randint(0, 20)
        m = random.randint(0, 13)
        G1 = random_graph(n, m)
        p1 = get_all_chromatic_polynomials(G1)

        n = random.randint(0, 20)
        m = random.randint(0, 13)
        G2 = random_graph(n, m)
        p2 = get_all_chromatic_polynomials(G2)
        H = star(G1, G2)

        assert get_all_chromatic_polynomials(H) ==  get_star(p1, p2), (get_all_chromatic_polynomials(H), get_star(p1, p2))

        message = f"Passed test: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()
    stdout.write("\n")



def test5(N = 50):
    print("Testing effective edge interactions, star")
    for i in range(1, 1+N):
        n = random.randint(0, 20)
        m = random.randint(0, 9)
        G1 = random_graph(n, m)
        pG1 = get_all_chromatic_polynomials(G1)

        n = random.randint(0, 20)
        m = random.randint(0, 9)
        G2 = random_graph(n, m)
        pG2 = get_all_chromatic_polynomials(G2)

        
        q = complex(random.random()+1, random.random()+1) # in shifted unit square  

        chi123 = pG1[-1].eval(q)
        y1 = tuple(p.eval(q) / chi123 * (q - 2) for p in pG1[:4])

        chi123 = pG2[-1].eval(q)
        y2 = tuple(p.eval(q) / chi123 * (q - 2) for p in pG2[:4])


        H = star(G1, G2)
        pH = get_all_chromatic_polynomials(H)
        chi123 = pH[-1].eval(q)
        y3 = tuple(p.eval(q) / chi123 * (q - 2) for p in pH[:4])

        new_y = effectiveInteractionStar(y1, y2, q)

        for j in range(4):
            assert round(new_y[j].real, 5) == round(y3[j].real, 5), ((y3, new_y), j)
            assert round(new_y[j].imag, 5) == round(y3[j].imag, 5), ((y3, new_y), j)
        
        message = f"Passed test: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()
    stdout.write("\n")




if __name__ == "__main__":
    try:
        i=1
        test1()

        i=2
        test2()

        i=3
        test3()

        i=4
        test4()


        i=5
        test5()

        print("Passed all tests")


    except AssertionError:
        print("Failed test", i)

