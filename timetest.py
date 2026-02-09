from libs.special_graphs import create_full_graph, get_vampire
from libs.chromaticpol import chrompol2, get_chromatic_polynomial, get_all_chromatic_polynomials
import time

K = create_full_graph(10)
for vertex in K.vertices:
    vertex.change_id(str(vertex.id))

G = get_vampire(3)
# G = K
print(len(G.edges))
start = time.time()
polys = get_all_chromatic_polynomials(G, NEWMODE = True)
for pol in polys:
    print(str(pol))
end = time.time()
print(end-start)


start = time.time()
polys = get_all_chromatic_polynomials(G, NEWMODE = False)
for pol in polys:
    print(str(pol))
end = time.time()
print(end-start)






