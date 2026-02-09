"""Chromatic polynomial via deletion–contraction recursion.

Given a (simple) undirected graph G, the chromatic polynomial P_G(x) satisfies:
    P_G(x) = P_{G - e}(x) - P_{G / e}(x)
for any (non-loop) edge e, where G - e deletes e and G / e contracts e.

This implementation returns an instance of classes.polynomial.Polynomial,
whose coefficients are stored as (a0, a1, ..., an) for a0 + a1*x + ... + an*x^n.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.graph import Graph

TIMETEST = True
NEWMODE = True

from classes.polynomial import Polynomial


it = 0



def get_chromatic_polynomial(G: Graph, progress_cb=None):
    global it
    stack = [(G.copy(), 1)]
    coeffs = [0 for _ in G.vertices] + [0]

    last = time.time()

    while stack:
        graph, sign = stack.pop()

        it += 1
        if not TIMETEST:
            time.sleep(0)      # yields to other threads

        # progress update (throttled)
        if progress_cb is not None:
            now = time.time()
            if now - last > 0.05:  # ~20 updates/sec max
                progress_cb(it, len(stack))
                last = now

        if graph.edges:
            G1 = graph
            G2 = graph.copy()

            edge1 = next(iter(G1.edges))
            a, b = (edge1)
            id1, id2 = a.id, b.id

            u = G2.ids[id1]
            v = G2.ids[id2]

            G1.contract_edge(edge1)
            G2.delete_edge(frozenset({u, v}))

            stack.append((G1, -sign))
            stack.append((G2, sign))
        else:
            n = len(graph.vertices)
            coeffs[n] += sign

    # final progress update
    if progress_cb is not None:
        progress_cb(it, 0)

    return Polynomial(*coeffs)  # return Polynomial, not str



def key_by_ids(G: Graph):
    # vertex ids (ook isolated vertices blijven zo in de key)
    if len(G.edges) > 12:
        return -1
    vs = frozenset(map(str, G.ids.keys()))

    def norm_edge(e):
        a, b = tuple(e)
        ia, ib = a.id, b.id
        return (ia, ib) if ia <= ib else (ib, ia)

    es = frozenset(norm_edge(e) for e in G.edges)

    return (vs, es)

# import numpy as np
lookup = dict()
tmp = set()

def pick_edge(G):
    def score(e):
        u, v = e
        return (len(u.neighbours & v.neighbours), len(u.neighbours) + len(v.neighbours))
    return max(G.edges, key=score)


def chrompol2(G: Graph, layer=0):
    shift = 0
    to_delete = []
    for vertex in G.vertices:   # Remove isolated vertices
        if vertex.degree == 0:
            if len(G.vertices) == 1:
                return Polynomial(0, 1)
            to_delete.append(vertex)
            shift += 1
            
    while to_delete:
        vertex = to_delete.pop()
        G.delete_vertex(vertex)

    keyG = key_by_ids(G)
    if keyG in lookup and keyG != -1:
        if shift == 0:
            return lookup[keyG]
        return lookup[keyG] * Polynomial(*([0 for _ in range(shift)]+[1]))
    if not G.edges:
        coeffs = [0 for _ in G.vertices] + [1]
        return Polynomial(*coeffs)
    
    H = G.copy()
    # edge = next(iter(G.edges))
    edge = pick_edge(G)
    # edge = max((edge for edge in G.edges), key = lambda x: sum(y.degree for y in x))
    u, v = edge
    u2 = H.ids[u.id]
    v2 = H.ids[v.id]
    H.contract_edge((u2, v2))
    G.delete_edge((u, v))

    out = chrompol2(G, layer+1) - chrompol2(H, layer+1)
    if len(G.edges) <= 12:
        lookup[keyG] = out
    if shift:
        return out * Polynomial(*([0 for _ in range(shift)]+[1]))
    return out


def get_all_chromatic_polynomials(G: Graph, progress_cb = None, NEWMODE = NEWMODE) -> tuple[Polynomial, ...]:

    #labels = sut
    assert 's' in G.ids and 'u' in G.ids and 't' in G.ids, "Does not contain sut vertices"
    start = time.time()
    def get111():
        print("starting 111")
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']
        if (s, u) in H or (s, t) in H or (u, t) in H:
            return Polynomial()

        H.add_edge((s, u))
        H.add_edge((s, t))
        H.add_edge((t, u))

        H.contract_edge((s, u))
        H.contract_edge((s, t))
        if NEWMODE: return chrompol2(H) * Polynomial(0, -1)
        
        return get_chromatic_polynomial(H, progress_cb)
        
    def get112():
        print("starting 112")
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']
        if (s, u) in H:
            return Polynomial()

        H.add_edge((s, u))
        H.add_edge((t, u))

        H.contract_edge((s, u))
        if NEWMODE: return chrompol2(H) * Polynomial(0, -1)
        return get_chromatic_polynomial(H, progress_cb)

    def get122():
        print("starting 122")
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']
        if (t, u) in H:
            return Polynomial()

        H.add_edge((s, u))
        H.add_edge((t, u))

        H.contract_edge((t, u))
        if NEWMODE: return chrompol2(H) * Polynomial(0, -1)
        return get_chromatic_polynomial(H, progress_cb)
    
    def get121():
        print("starting 121")
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']
        if (s, t) in H:
            return Polynomial()

        H.add_edge((s, u))
        H.add_edge((t, u))

        H.contract_edge((s, t))
        if NEWMODE: return chrompol2(H) * Polynomial(0, -1)
        return get_chromatic_polynomial(H, progress_cb)

    def get123():
        print("starting 123")
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']

        H.add_edge((s, u))
        H.add_edge((t, u))
        H.add_edge((t, s))
        if NEWMODE: return chrompol2(H) * Polynomial(0, -1)
        return get_chromatic_polynomial(H, progress_cb)

    polys = (get111(), get112(), get121(), get122(), get123())
    end = time.time()

    if TIMETEST:
        print(f"Visited {it} nodes in {end - start}s")
    return polys
