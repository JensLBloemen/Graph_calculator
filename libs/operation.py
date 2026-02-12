## Add the operation from the thesis (Needs to be named still)

from classes.graph import Graph
from classes.vertex import Vertex

def operation(G: Graph, H: Graph) -> Graph:

    # Make graphs the same size!
    lengthG = abs(G.ids['s'].location[0] - G.ids['u'].location[0])
    lengthH = abs(H.ids['s'].location[0] - H.ids['u'].location[0])
    
    for vertex in H.vertices:
        x, y = vertex.location
        x *= lengthG / lengthH
        y *= lengthG / lengthH
        vertex.location = (x,y)


    out = Graph()

    l = 1 / 2 ** 0.5
    for vertex in G.vertices:
        identity = vertex.id + '_1'

        # Rotate 45 degrees and shift
        x, y = vertex.location
        x, y = l * (x + y), l * (y-x)
        location = (-x-1, y)

        new_vertex = Vertex(out, location, identity)
        out.add_vertex(new_vertex)
    
    for edge in G.edges:
        u, v = edge

        u1, v1 = out.ids[u.id+"_1"], out.ids[v.id+"_1"]
        out.add_edge((u1, v1))

    for vertex in H.vertices:
        identity = vertex.id + '_2'
        x, y = vertex.location
        x, y = l * (x - y), l * (x + y)

        location = (1 - x, y)

        new_vertex = Vertex(out, location, identity)
        out.add_vertex(new_vertex)
    
    for edge in H.edges:
        u, v = edge

        u1, v1 = out.ids[u.id+"_2"], out.ids[v.id+"_2"]
        out.add_edge((u1, v1))

    # contract s_1, s_2
    s1 = out.ids["s_1"]
    s2 = out.ids["s_2"]
    
    out.add_edge((s1, s2))
    out.contract_edge((s1, s2))

    s1.change_id('0')
    s1.location = (0,0)


    # contract t1 and u2 into s
    t1 = out.ids["t_1"]
    u2 = out.ids["u_2"]

    out.add_edge((t1, u2))
    out.contract_edge((t1, u2))
    t1.change_id('s')
    x,y = t1.location
    t1.location = (0, y)


    # change id of u1 and t2
    u1 = out.ids['u_1']
    t2 = out.ids['t_2']

    u1.change_id('u')
    t2.change_id('t')


    # Flip again
    s = t1

    x, y = s.location
    for vertex in out.vertices:
        xv, yv = vertex.location
        vertex.location = (-xv, y-yv)

    midpoint = out.ids['0']
    midpoint.location = (0, t2.location[1])

    return out
    
    