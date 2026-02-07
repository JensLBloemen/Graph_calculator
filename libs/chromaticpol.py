"""Chromatic polynomial via deletion–contraction recursion.

Given a (simple) undirected graph G, the chromatic polynomial P_G(x) satisfies:
    P_G(x) = P_{G - e}(x) - P_{G / e}(x)
for any (non-loop) edge e, where G - e deletes e and G / e contracts e.

This implementation returns an instance of classes.polynomial.Polynomial,
whose coefficients are stored as (a0, a1, ..., an) for a0 + a1*x + ... + an*x^n.
"""

from __future__ import annotations

from typing import Dict, FrozenSet, Tuple, TYPE_CHECKING
from copy import deepcopy

if TYPE_CHECKING:
    from classes.graph import Graph
from classes.vertex import Vertex
from classes.polynomial import Polynomial



def get_chromatic_polynomial(G: Graph):
    it = 0

    stack = [(G.copy(), 1)]  # graph, sign
    polynomials = []
    while stack:
        graph, sign = stack.pop()

        graph.name = f"iteration {it}"

        graph.save()
        it += 1

        if graph.edges:

            G1 = graph.copy()
            G2 = graph.copy()

            edge1 = next(iter(G1.edges))         # frozenset({u, v})
            a, b = tuple(edge1)
            id1, id2 = a.id, b.id

            u = None
            v = None
            for vertex in G2.vertices:
                if vertex.id == id1:
                    u = vertex
                if vertex.id == id2:
                    v = vertex

            # edge2 = (u, v)
            assert u is not None
            assert v is not None

            G1.contract_edge(edge1)
            G2.delete_edge(frozenset({u, v}))



            stack.append((G1, -sign))
            stack.append((G2, sign))
        else:
            # print("yes")
            pol_data = [0 for _ in graph.vertices]
            pol_data.append(sign)
            polynomials.append(Polynomial(*pol_data))
    return str(sum(polynomials))
