from gui.gui import App

from classes.graph import Graph
from classes.vertex import Vertex
from classes.polynomial import Polynomial as P
from libs.chromaticpol import get_all_chromatic_polynomials

from numpy import sin, cos, pi
# from libs.effectiveinteractions import effectiveInteraction as E

from libs.special_graphs import get_vampire
from libs.operations import star

import matplotlib.pyplot as plt
from gui.helper_functions.loadgraph import load_graph

import numpy as np

# n = 5
# G = Graph("Ladder")
# u = Vertex(G, (0,1), "u")
# G.add_vertex(u)

# oldv1 = None
# oldv2 = None
# for i in range(0, n):
#     v1 = Vertex(G, (-1, -i), str(i)+'1')
#     v2 = Vertex(G, (1, -i), str(i)+'2')
#     v3 = Vertex(G, (0, -i), str(i)+'0')
#     G.add_vertex(v1)
#     G.add_vertex(v2)
#     if i == 0:
#         G.add_vertex(v3)

#     if i == n-1:
#         s = v1
#         t = v2
#         v1.change_id("s")
#         v2.change_id("t")
#     if i == 0:
#         v3.add_neighbour(v1)
#         v3.add_neighbour(v2)

#     u.add_neighbour(v1)
#     u.add_neighbour(v2)

#     if oldv1 is not None:
#         oldv1.add_neighbour(v1)
#         oldv2.add_neighbour(v2)

#     oldv1 = v1
#     oldv2 = v2

# G.delete_edge((v3, t))
# G.delete_edge((v3, s))

# G.save()

from libs.special_graphs import get_vampire
G = get_vampire(3)
G.save()

def checkDFS(q, y_start = 0, depth = 300):
    def f(y):
        if y == 1:
            return 0
        return 1 + q / (y - 1)

    stack = [(y_start, depth)]
    while stack:
        y, cur_depth = stack.pop()
        if cur_depth <= 1:
            continue

        if abs(y) > 1 or abs(f(y)) > 1:
            return True

        for j in range(2, cur_depth):
            stack.append((f(y ** j), cur_depth // j))
    return False


N = 300
if __name__ == "__main__":
    app = App()
    app.run()
    
    
    G = load_graph("new_graph (5).json")
    print(f"#(E, V)={len(G.edges), len(G.vertices)}")
    # polys = get_all_chromatic_polynomials(G)
    # print(polys)
    X = P(0, 1)
    pol_same = None
    H = G.copy()
    s = H.ids["s"]
    t = H.ids["u"]
    if s in t.neighbours:
        pol_same = P(0)
    H.add_edge((s, t))
    pol_dif = H.chromatic_polynomial
    H.contract_edge((s,t))
    if pol_same is None:
        pol_same = H.chromatic_polynomial
    xrange = np.linspace(0, 1.9, N)
    yrange = np.linspace(-1.0001,1, N)
    print(pol_same, pol_dif)



    grid = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            q = complex(xrange[i], yrange[j])
            y = pol_same.eval(q) / pol_dif.eval(q) * (q - 1)

            if checkDFS(q, y, depth=2):
                grid[j][i] = 1
    plt.imshow(grid, extent=[0,1.9, -1, 1]) 

    plt.show()


