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

TIMETEST = False
NEWMODE = True   # True is high RAM demand, False is slower and high CPU demand

from classes.polynomial import Polynomial
from itertools import repeat


import os
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def _chrompoly_subtree(graph: "Graph", sign: int, n0: int) -> list[int]:
    """Compute partial coefficient vector for one (graph, sign) subtree."""
    stack: list[tuple["Graph", int]] = [(graph, sign)]
    coeffs = [0] * (n0 + 1)

    while stack:
        g, s = stack.pop()

        if g.edges:
            # IMPORTANT: both branches must be independent graphs
            G1 = g.copy()
            G2 = g.copy()

            # pick an edge from G1 (G2 has same ids, but different Vertex objects)
            edge = next(iter(G1.edges))
            a, b = tuple(edge)

            # contraction branch on G1
            G1.contract_edge(edge)

            # deletion branch on G2 — MUST use vertices from G2
            u = G2.ids[a.id]
            v = G2.ids[b.id]
            G2.delete_edge(frozenset({u, v}))

            stack.append((G1, -s))
            stack.append((G2,  s))
        else:
            coeffs[len(g.vertices)] += s

    return coeffs

it = 0
def get_chromatic_polynomial(
    G: "Graph",
    workers: int | None = None,
    task_factor: int = 4,
) -> "Polynomial":
    """
    Parallel deletion–contraction using process-based parallelism (uses all logical CPUs by default).
    NOTE (Windows/macOS): call this from inside `if __name__ == "__main__":` (or an equivalent entrypoint).
    """
    n0 = len(G.vertices)
    if n0 == 0:
        return Polynomial(1)  # standard convention: empty graph -> 1

    if workers is None:
        workers = os.cpu_count() or 1
    workers = max(1, int(workers))
    task_factor = max(1, int(task_factor))

    # Build a frontier of independent subproblems to distribute.
    target_tasks = max(workers * task_factor, 1)
    frontier: list[tuple["Graph", int]] = [(G.copy(), 1)]
    tasks: list[tuple["Graph", int]] = []

    while frontier and len(tasks) < target_tasks:
        g, s = frontier.pop()

        if not g.edges:
            tasks.append((g, s))
            continue

        # IMPORTANT: both branches must be independent graphs
        G1 = g.copy()
        G2 = g.copy()

        edge = next(iter(G1.edges))
        a, b = tuple(edge)

        # contraction branch
        G1.contract_edge(edge)

        # deletion branch (use G2 vertices)
        u = G2.ids[a.id]
        v = G2.ids[b.id]
        G2.delete_edge(frozenset({u, v}))

        frontier.append((G1, -s))
        frontier.append((G2,  s))

    # Anything left becomes tasks as-is.
    tasks.extend(frontier)

    # Accumulate results
    coeffs = [0] * (n0 + 1)

    if workers == 1 or len(tasks) <= 1:
        for g, s in tasks:
            part = _chrompoly_subtree(g, s, n0)
            for i, v in enumerate(part):
                coeffs[i] += v
    else:
        # process-based parallelism (real CPU parallelism)
        ctx = mp.get_context("spawn")  # safest across platforms
        graphs = (g for g, _ in tasks)
        signs = (s for _, s in tasks)

        with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as ex:
            for part in ex.map(_chrompoly_subtree, graphs, signs, repeat(n0)):
                for i, v in enumerate(part):
                    coeffs[i] += v

    return Polynomial(*coeffs)

def key_by_ids(G: Graph):
    # vertex ids (ook isolated vertices blijven zo in de key)
    if len(G.edges) > 12:
        return -1
    vs = frozenset(map(str, G.ids.keys()))
    n = len(vs)
    relabel = dict()
    for i, j in zip(range(n), vs):
        relabel[j] = str(i)
    

    def norm_edge(e):
        a, b = tuple(e)
        ia, ib = a.id, b.id
        return (relabel[ia], relabel[ib]) if relabel[ia] <= relabel[ib] else (relabel[ib], relabel[ia])

    
    es = frozenset(norm_edge(e) for e in G.edges)
    vs = frozenset(map(str, relabel.keys()))

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
    if len(G.vertices) == 1:
        return Polynomial(0, 1)

    shift = 0
    to_delete = []
    for vertex in G.vertices:   # Remove isolated vertices
        if vertex.degree == 0:
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
        return Polynomial(*coeffs) * Polynomial(*([0 for _ in range(shift)]+[1]))
    
    H = G.copy()
    edge = pick_edge(G)
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
        if NEWMODE: return chrompol2(H)
        
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
        if NEWMODE: return chrompol2(H)
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
        if NEWMODE: return chrompol2(H)
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
        if NEWMODE: return chrompol2(H)
        return get_chromatic_polynomial(H, progress_cb)

    def get123():
        H = G.copy()
        s = H.ids['s']
        u = H.ids['u']
        t = H.ids['t']

        H.add_edge((s, u))
        H.add_edge((t, u))
        H.add_edge((t, s))
        if NEWMODE: return chrompol2(H)
        return get_chromatic_polynomial(H, progress_cb)

    polys = (get111(), get112(), get121(), get122(), get123())
    end = time.time()

    if TIMETEST:
        print(f"Visited {it} nodes in {end - start}s")
    return polys
