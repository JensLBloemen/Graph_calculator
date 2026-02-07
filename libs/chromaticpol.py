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




def get_chromatic_polynomial(G: Graph, progress_cb=None):
    stack = [(G.copy(), 1)]
    polynomial = Polynomial()

    it = 0
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
            G1 = graph.copy()
            G2 = graph.copy()

            edge1 = next(iter(G1.edges))
            a, b = tuple(edge1)
            id1, id2 = a.id, b.id

            u = v = None
            for vertex in G2.vertices:
                if vertex.id == id1:
                    u = vertex
                elif vertex.id == id2:
                    v = vertex

            assert u is not None and v is not None

            G1.contract_edge(edge1)
            G2.delete_edge(frozenset({u, v}))

            stack.append((G1, -sign))
            stack.append((G2, sign))
        else:
            n = len(graph.vertices)
            coeffs = [0] * n + [sign]
            polynomial += Polynomial(*coeffs)

    # final progress update
    if progress_cb is not None:
        progress_cb(it, 0)

    return polynomial  # return Polynomial, not str
