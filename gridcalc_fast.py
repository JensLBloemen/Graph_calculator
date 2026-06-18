from __future__ import annotations

import os
from os import listdir
from sys import stdout
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

from numba import njit

from libs.effectiveinteractions import (
    effectiveInteractionStar,
    effectiveInteractionTriangle,
    square_proj,
)


def update_progress(i: int, N: int) -> None:
    filled = (i * 40) // N if N else 40
    message = f"Progress: [{'-' * filled}{' ' * (40 - filled)}]  {i}/{N}"
    stdout.write(message)
    stdout.write("\r" * len(message))
    stdout.flush()


# ============================================================
# Settings
# ============================================================

N = 1001

x_min = -0.001
x_max = 2.0001

y_min = -1
y_max = 1

depth = 32                  # easy to change
TEST_TYPE = "extended g-func"          # Either g-func, extended g-func, 
YS_DEPTH = 100            # depth used inside get_ys
IGNOREOLD = True

NPY_DIR = "npy_files"
OUT_PNG = "out.png"
TITLE = f"Results of {TEST_TYPE} with {YS_DEPTH=}"

CHUNKSIZE = 4
MAX_WORKERS = os.cpu_count()


import numpy as np


def _disk_square_stable(a, r, n_boundary=720, tol=1e-9):
    """
    Numerically checks whether D(a,r)^2 subset D(a,r).
    Uses the criterion:
        max_{z in D(a,r)} r|z| + |a||z-1| <= r
    and samples the boundary.
    """
    if r <= 0:
        return abs(a * a - a) <= tol

    theta = np.linspace(0, 2 * np.pi, n_boundary, endpoint=False)
    z = a + r * np.exp(1j * theta)

    worst = np.max(r * np.abs(z) + abs(a) * np.abs(z - 1))
    return worst <= r + tol


def _image_disk_under_f(a, r, q, tol=1e-12):
    """
    Image of D(a,r) under f_q(z) = 1 + q/(z-1).

    Returns center A and radius R of f_q(D(a,r)).
    Requires 1 notin D(a,r).
    """
    den = abs(a - 1) ** 2 - r ** 2

    if den <= tol:
        return None

    A = 1 + q * np.conj(a - 1) / den
    R = abs(q) * r / den

    return A, R


def exists_circle(q, Na=30, Nr=30, Nb=72, tol=1e-7, return_disk=False):
    """
    Returns True/False depending on whether the search finds a disk V = D(a,r)
    such that:

        0 in V,
        V^2 subset V,
        f_q(f_q(V)^2) subset V.

    Assumes q != 0 and V avoids the pole z=1.

    Parameters
    ----------
    q : complex
        Complex q-value.
    Na : int
        Number of grid points for real/imaginary parts of disk center a.
    Nr : int
        Number of grid points for radius r.
    Nb : int
        Boundary resolution for disk-square-stability check.
    tol : float
        Numerical tolerance.
    return_disk : bool
        If True, returns (True, (a,r)) when a disk is found.

    Notes
    -----
    This is numerical, not a rigorous proof of nonexistence.
    Increase Na, Nr, Nb for more reliable results.
    """

    q = complex(q)

    # Necessary condition:
    # f(V) is also multiplicatively stable, so it lies in the unit disk.
    # Since 0 in V, we have f_q(0) = 1-q in f(V).
    if abs(1 - q) > 1 + tol:
        return (False, None) if return_disk else False

    # Search region for a.
    # Since 0 in V and V^2 subset V, a nondegenerate stable disk lies in |z| <= 1.
    xs = np.linspace(-0.5, 0.5, Na)
    ys = np.linspace(-0.5, 0.5, Na)

    pole_margin = 1e-10

    for x in xs:
        for y in ys:
            a = x + 1j * y

            if abs(a) > 0.5 + tol:
                continue

            # Necessary:
            # 0 in V means |a| <= r.
            # Also f_q(1-q) = 0, so V should contain 1-q.
            r_min = max(abs(a), abs((1 - q) - a))

            # Stable disk must lie in the unit disk, so r <= 1 - |a|.
            # Also V must avoid the pole z=1.
            r_max = min(1 - abs(a), abs(1 - a) - pole_margin)

            if r_min > r_max:
                continue

            for r in np.linspace(r_min, r_max, Nr):
                # Check V^2 subset V
                if not _disk_square_stable(a, r, Nb, tol):
                    continue

                # Compute W = f_q(V)
                image = _image_disk_under_f(a, r, q)

                if image is None:
                    continue

                A, R = image

                # Cheap necessary filters for W
                if abs(A) > R + 1e-6:
                    continue

                if abs((1 - q) - A) > R + 1e-6:
                    continue

                if abs(A) + R > 1 + 1e-6:
                    continue

                # Check W^2 subset W
                if _disk_square_stable(A, R, Nb, tol):
                    return (True, (a, r)) if return_disk else True

    return (False, None) if return_disk else False


def checkzerofree(q):
    return exists_circle(q)

# ============================================================
# DFS check
# ============================================================

@njit(cache=True, fastmath=True)
def checkDFS(q, y_start=0, depth=300):
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


def checkDFS_fast(q: complex, y: complex, depth_value: int) -> bool:
    """
    Keeps depth flexible, but gives a cheap fast path for depth == 2.
    """
    if depth_value == 2:
        if abs(y) > 1:
            return True
        if y == 1:
            return True
        return abs(1 + q / (y - 1)) > 1

    return bool(checkDFS(q, y, depth=depth_value))


# ============================================================
# Unused helpers from your original file, kept for convenience
# ============================================================

def get_wheel(n, q, k=1):
    EEI = (0, 0, 0, 0)
    EEI_start = EEI
    for _ in range(n):
        EEI = effectiveInteractionStar(EEI, EEI_start, q)
    return EEI


def get_vampire(n, q):
    EEI = (0, 0, 0, 0)
    for _ in range(n):
        EEI = effectiveInteractionTriangle(EEI, EEI, q)
    return EEI



def Fs(EEI, q):
    denom = EEI[1] + EEI[2] + q - 2
    if abs(denom) < 1e-6:
        return 0
    return (EEI[0] + EEI[3]) / denom * (q - 1)


def star_power(base, n, q):
    """
    Compute base * base * ... * base (n times)
    using the associative operation effectiveInteractionStar.

    Requires n >= 1.
    """
    if n < 1:
        raise ValueError("n must be >= 1")

    result = None
    power = base

    while n > 0:
        if n & 1:
            result = power if result is None else effectiveInteractionStar(result, power, q)
        n >>= 1
        if n:
            power = effectiveInteractionStar(power, power, q)

    return result


# ============================================================
# Faster get_ys
# ============================================================

def get_ys(q: complex, depth: int = 20) -> set[complex]:
    q = complex(q)

    def f(y: complex) -> complex:
        return 1 + q / (y - 1)

    found: set[complex] = {0j}
    stack: list[tuple[complex, int]] = [(0j, depth)]
    seen_states: set[tuple[complex, int]] = {(0j, depth)}

    while stack:
        y, cur_depth = stack.pop()

        if cur_depth < 2:
            continue
               
        if abs(y) > 1 or abs(f(y)) > 1:  # to combat overflow error
            # found.add(y)
            return set([y, f(y)])

        for n in range(2, cur_depth+1):
            new_depth = cur_depth // n

            # 1. Parallel power: y^n ∈ E
            y_parallel = y ** n
            found.add(y_parallel)

            if new_depth > 1:
                state = (y_parallel, new_depth)
                if state not in seen_states:
                    seen_states.add(state)
                    stack.append(state)

            # 2. Series power: f(f(y)^n) ∈ E
            # If y == 1, then f(y)=infinity, and f(infinity)=1.
            if y == 1:
                y_series = 1 + 0j
            else:
                fy = f(y)
                if abs(fy) > 1:  # to combat overflow error
                    found.add(f(fy))
                    return set(fy)
                p = fy ** n

                # If p == 1, then f(p)=infinity.
                # Skip if you only want finite complex values.
                if p == 1:
                    continue

                y_series = f(p)

            found.add(y_series)

            if new_depth > 1:
                state = (y_series, new_depth)
                if state not in seen_states:
                    seen_states.add(state)
                    stack.append(state)

    return found

# ============================================================
# checkDense
# ============================================================
from tmp3 import build_generated_shape
def checkDense(q: complex, depth_value: int = 2, projection: str = "Fs") -> int:
    ys = get_ys(q, depth=YS_DEPTH)
    def f(y):
        return 1 + (q) / (y - 1)
    
    def h(y):   # Spoke graph
        return (y+q-2)/(y+q-3)
    
    def g(y):
        return 1 + (q-1) / (y - 1)

    if projection == "y-test":
        if q in [0,1,2]:
            return 1
        
        for y in ys:
            if abs(y) >= 1 or abs(f(y)) >= 1:
                return 1
        return 0

    if projection == "zerofree-SP":
        return not build_generated_shape(q, 100, eps=0.01, max_abs=1, verbose=False)[2]
       

    if projection == "g-func":
        if q == 2 or q == 3:
            return 1

        if abs(q-3/2) > 0.5 and abs(q) > 1:         # Proven region
            return 1
        if q.real > 3/2:
            return 1
        if abs(q-1) > 1:
            return 1

        for y in ys:  # Search for new values
            if abs(y) >= 1 or abs(f(y)) >= 1:   # Zeros from SP-graphs
                return 1

            if abs(2-q) < 1 and (abs(g(y)) > 1 or abs(g(h(y))) > 1):
                return 1

            if abs(2-q) > 1 and (abs(g(y)) < 1 or abs(g(h(y))) < 1):
                return 1
    
        return 0
    
    if projection == "extended g-func":
        if abs(q-1) > 1:
            return 1
        if abs(2-q) > 1 and abs(q) > 1:
            return 1

        for y in ys:
            if abs(y) > 1 or abs(f(y)) > 1:
                return 1

            EEI = (0, y, 1, 0)
            for i in range(1, depth_value):
                EEI_it = star_power(EEI, i, q)
                z = EEI_it[-1]
                if z == 1:
                    continue

                if abs(2-q) < 1 and (abs(g(z)) > 1 or abs(g(y)) > 1):
                    return 1

                if abs(2-q) > 1 and (abs(g(z)) < 1 or abs(g(y)) < 1):
                    return 1

        return 0

    raise ValueError("projection must be 'g-func' or ''")


# ============================================================
# Grid loading
# ============================================================

def load_old_grid(n: int, npy_dir: str) -> np.ndarray:
    old_grid = np.zeros((n, n), dtype=np.bool_)

    if not os.path.isdir(npy_dir):
        return old_grid

    for filename in listdir(npy_dir):
        if not filename.endswith(".npy") or "Zero" in filename:
            continue

        path = os.path.join(npy_dir, filename)
        arr = np.load(path)

        if arr.shape != (n, n):
            print(f"Skipping {filename}: shape {arr.shape} does not match {(n, n)}")
            continue

        old_grid |= arr.astype(np.bool_)

    return old_grid


# ============================================================
# Multiprocessing worker setup
# ============================================================

_OLD_GRID = None
_Y_VALS = None
_DEPTH = None
_PROJECTION = None
_IGNOREOLD = None


def _init_worker(old_grid, y_vals, depth_value, projection, ignoreold):
    global _OLD_GRID, _Y_VALS, _DEPTH, _PROJECTION, _IGNOREOLD
    _OLD_GRID = old_grid
    _Y_VALS = y_vals
    _DEPTH = depth_value
    _PROJECTION = projection
    _IGNOREOLD = ignoreold


def _compute_column(task):
    it, x = task
    top = np.zeros(len(_Y_VALS), dtype=np.bool_)

    old_col = None if _IGNOREOLD else _OLD_GRID[:len(_Y_VALS), it]

    for ity, y in enumerate(_Y_VALS):
        if old_col is not None and old_col[ity]:
            top[ity] = True
        else:
            q = complex(x, y)
            top[ity] = bool(checkDense(q, depth_value=_DEPTH, projection=_PROJECTION))

    return it, top


# ============================================================
# Grid computation
# ============================================================

def compute_grid(
    n: int,
    x_min_value: float,
    x_max_value: float,
    y_max_value: float,
    depth_value: int,
    projection: str,
    ignoreold: bool,
    npy_dir: str,
) -> np.ndarray:
    old_grid = load_old_grid(n, npy_dir)

    x_vals = np.linspace(x_min_value, x_max_value, n)
    y_vals = np.linspace(-y_max_value, 0, n // 2 + 1)

    grid = np.zeros((n, n), dtype=np.bool_)
    tasks = [(it, x) for it, x in enumerate(x_vals)]

    with ProcessPoolExecutor(
        max_workers=MAX_WORKERS,
        initializer=_init_worker,
        initargs=(old_grid, y_vals, depth_value, projection, ignoreold),
    ) as ex:
        for done, (it, top) in enumerate(ex.map(_compute_column, tasks, chunksize=CHUNKSIZE), 1):
            # rows 0 .. len(y_vals)-1
            grid[:len(y_vals), it] = top

            # mirror to the remaining rows
            if len(y_vals) > 1:
                grid[-(len(y_vals) - 1):, it] = top[1:][::-1]

            update_progress(done, n)

    print("\n")
    return grid


# ============================================================
# Saving
# ============================================================

def save_grid(grid: np.ndarray, npy_dir: str) -> str:
    os.makedirs(npy_dir, exist_ok=True)

    counter = 1
    while True:
        filename = f"out{counter}.npy"
        path = os.path.join(npy_dir, filename)
        if not os.path.exists(path):
            np.save(path, grid)
            return path
        counter += 1


# ============================================================
# Plotting
# ============================================================

def plot_grid(
    grid: np.ndarray,
    x_min_value: float,
    x_max_value: float,
    y_max_value: float,
    title: str,
    out_png: str,
):
    fig, ax = plt.subplots()

    ax.spines["bottom"].set_position("center")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")

    ax.xaxis.set_major_locator(MultipleLocator(0.25))
    ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))

    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")

    cmap = ListedColormap(["white", "green", "red", "blue"])

    ax.imshow(
        grid,
        extent=[x_min_value, x_max_value, -y_max_value, y_max_value],
        cmap=cmap,
        interpolation="nearest",
    )

    ax.set_xlabel(r"$\text{Re}(q)$", loc="right")
    ax.set_ylabel(r"$\text{Im}(q)$", loc="center")
    plt.title(title)
    plt.savefig(out_png, dpi=300)
    plt.show()


# ============================================================
# Main
# ============================================================

def main():
    grid = compute_grid(
        n=N,
        x_min_value=x_min,
        x_max_value=x_max,
        y_max_value=y_max,
        depth_value=depth,
        projection=TEST_TYPE,
        ignoreold=IGNOREOLD,
        npy_dir=NPY_DIR,
    )

    saved_path = save_grid(grid, NPY_DIR)
    print(f"Saved grid to: {saved_path}")

    plot_grid(
        grid=grid,
        x_min_value=x_min,
        x_max_value=x_max,
        y_max_value=y_max,
        title=TITLE,
        out_png=OUT_PNG,
    )


if __name__ == "__main__":
    freeze_support()
    main()
