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
            a, b = tuple(edge1)
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

def get_all_chromatic_polynomials(G: Graph, progress_cb = None) -> tuple[Polynomial, ...]:

    #labels = sut
    assert 's' in G.ids and 'u' in G.ids and 't' in G.ids, "Does not contain sut vertices"

    def get111():
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

        return get_chromatic_polynomial(H, progress_cb)
        
    def get112():
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']
        if (s, u) in H:
            return Polynomial()

        H.add_edge((s, u))
        H.add_edge((t, u))

        H.contract_edge((s, u))

        return get_chromatic_polynomial(H, progress_cb)

    def get122():
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']
        if (t, u) in H:
            return Polynomial()

        H.add_edge((s, u))
        H.add_edge((t, u))

        H.contract_edge((t, u))

        return get_chromatic_polynomial(H, progress_cb)
    
    def get121():
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']
        if (s, t) in H:
            return Polynomial()

        H.add_edge((s, u))
        H.add_edge((t, u))

        H.contract_edge((s, t))

        return get_chromatic_polynomial(H, progress_cb)

    def get123():
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']

        H.add_edge((s, u))
        H.add_edge((t, u))
        H.add_edge((t, s))

        return get_chromatic_polynomial(H, progress_cb)

    return (get111(), get112(), get121(), get122(), get123())
