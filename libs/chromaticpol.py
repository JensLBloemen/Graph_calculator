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
    coeffs = [0 for _ in G.vertices] + [0]

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
