from sys import stdout
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numba as nb
from numba import njit, prange


# -----------------------------
# Numba helpers
# -----------------------------
@njit(cache=True, fastmath=True)
def _abs2(z):
    return z.real * z.real + z.imag * z.imag


@njit(cache=True, fastmath=True)
def dif4(a, b, c, d, oa, ob, oc, od, eps):
    return (_abs2(a - oa) + _abs2(b - ob) + _abs2(c - oc) + _abs2(d - od)) < eps * eps


@njit(cache=True, fastmath=True)
def caseCheck4(b, d, q, eps=1e-2):
    eps2 = eps * eps

    if _abs2(b - 1.0) < eps2:
        return 1

    if _abs2(q - 2.0 + b + b * b) < eps2:
        return 2

    if _abs2(q - 2.0 + 2.0 * b * b) < eps2:
        return 3

    val = (q - 2.0) * (q - 2.0) + (3.0 * q - 7.0) * b + (2.0 + q) * b * b + b * b * b
    if _abs2(val) < eps2:
        return 4

    if _abs2(d - 2.0) < eps2:
        return 5

    return 6


# -----------------------------
# Your effectiveInteraction step (y0=y1=state)
# -----------------------------
@njit(cache=True, fastmath=True)
def effectiveInteraction_step(a, b, c, d, q):
    # Delta = q - 3 + y0[1] + y1[2] + y0[2] * y1[1]
    # with y0=y1: Delta = q - 3 + b + c + c*b
    Delta = q - 3.0 + b + c + c * b

    # new_y_111 = (q - 1) * y0[0] * y1[0] + y0[3] * y1[3]
    new111 = (q - 1.0) * a * a + d * d

    # new_y_112 = (q - 1) * y0[0] * y1[1] + y0[3] * y1[2] + y0[3] * (q - 2)
    new112 = (q - 1.0) * a * b + d * c + d * (q - 2.0)

    # new_y_121 = (q - 1) * y0[2] * y1[0] + y0[1] * y1[3] + y1[3] * (q - 2)
    new121 = (q - 1.0) * c * a + b * d + d * (q - 2.0)

    # new_y_122 = q - 2 + y0[2] * y1[1] + y0[1] * y1[2]
    # with y0=y1: q-2 + c*b + b*c = q-2 + 2*b*c
    new122 = (q - 2.0) + 2.0 * b * c

    invD = 1.0 / Delta
    return new111 * invD, new112 * invD, new121 * invD, new122 * invD

@njit(cache=True, fastmath=True)
def f(y, q):
    return _abs2(1+q / (y - 1))

@njit(cache=True, fastmath=True)
def IsDense(a, b, c, d, q):
    denum = c + d + q -2
    if _abs2(denum) < 1e-8:
        return False
    num = a + b
    return (_abs2(num / denum) > 1) or (f(num / denum, q) > 1)


# -----------------------------
# Main scan (Numba parallel)
# -----------------------------
@njit(parallel=True, cache=True, fastmath=True)
def scan_grid(x_lin, y_lin, max_iter, eps_conv, eps_case):
    N = x_lin.size
    grid = np.zeros((N, N), dtype=np.int8)

    for ix in prange(N):
        xre = x_lin[ix]
        for iy in range(N):
            qim = y_lin[iy]
            q = xre + 1j * qim

            a = 0.0 + 0.0j
            b = 0.0 + 0.0j
            c = 0.0 + 0.0j
            d = 0.0 + 0.0j

            for _ in range(max_iter):
                oa, ob, oc, od = a, b, c, d

                a, b, c, d = effectiveInteraction_step(a, b, c, d, q)
                # if IsDense(a,b,c,d, q):
                #     grid[iy, ix] = 1
                # if IsDense(a, b, c, d, q):
                #     grid[iy, ix] = 1
                #     break
                # your stopping condition
                if dif4(a, b, c, d, oa, ob, oc, od, eps_conv) or (_abs2(d.real - 2.0) < eps_conv):
                    # your "near 2 but not blown up => keep iterating"
                    if (_abs2(d - 2.0) < eps_case) and not (_abs2(a) > 10000.0):
                        continue
                    if IsDense(a, b, c, d, q):
                        grid[iy, ix] = caseCheck4(b, d, q, eps_case)
                    break

    return grid


# -----------------------------
# Progress bar (optional, Python-side)
# -----------------------------
def update_progress(i, N):
    message = f"Progress: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
    stdout.write(message)
    stdout.write('\r' * len(message))
    stdout.flush()


# -----------------------------
# Run
# -----------------------------
print("Starting")
N = 1001
x_min, x_max = -1, 5
y_min, y_max = -3, 3

x_lin = np.linspace(x_min, x_max, N)
y_lin = np.linspace(y_max, y_min, N)

# First call triggers compilation (can take a moment once)
grid = scan_grid(x_lin, y_lin, max_iter=100000, eps_conv=1e-3, eps_case=1e-2)

# hits summary (0..6)
hits = np.bincount(grid.ravel().astype(np.int64), minlength=7)
print("hits[0..6] =", hits)

# Plot
im = plt.imshow(grid, extent=[x_min, x_max, y_min, y_max])

values = list(range(7))
labels = {0: "No convergence", 1: "$y^{112}=1$", 2: "Case 2"}

colors = [im.cmap(im.norm(v)) for v in values]
patches = [mpatches.Patch(color=colors[i], label=labels.get(i, str(i))) for i in range(len(values))]
plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()