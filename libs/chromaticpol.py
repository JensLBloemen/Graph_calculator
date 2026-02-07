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
    return