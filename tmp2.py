import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange


@njit(inline='always')
def cpow(z, n):
    """Integer power by squaring."""
    out = 1.0 + 0.0j
    base = z
    m = n
    while m > 0:
        if m & 1:
            out *= base
        base *= base
        m >>= 1
    return out


@njit
def old_dense_test_from_y(q, y_val, N, eps=1e-14):
    """
    Your old test, unchanged except that y_val is supplied externally.
    """
    y2 = y_val
    qm1 = q - 1.0
    qm2 = q - 2.0

    if abs(qm2) < eps:
        return True

    ratio = qm1 / qm2

    for _ in range(N):
        # T(z) = (y_val*z + q - 2) / (z + q - 3 + y_val)
        denomT = y2 + q - 3.0 + y_val
        if abs(denomT) < eps:
            return True

        Ty2 = (y_val * y2 + qm2) / denomT

        arg = y2 * ratio
        denomf = arg - 1.0
        if abs(denomf) < eps:
            return True

        # f(arg) = 1 + q / (arg - 1)
        fval = 1.0 + q / denomf

        if abs(Ty2 * ratio) > 1.0 or abs(fval) > 1.0:
            return True

        y2 = Ty2

    return False


@njit
def checkDense_product_search_correct(q, max_prod, N, eps=1e-14):
    """
    Searches over exponent sequences (n1,...,nk) with n1*...*nk <= max_prod,
    assuming n_j >= 2.

    Correct recurrence:
        a0 = f_q(0) = 1 - q
        a_{j+1} = f_q(a_j ^ n_{j+1})

    For every reachable a_k, run the old dense test with y_val = a_k.
    """
    max_states = 100000

    z_stack = np.empty(max_states, dtype=np.complex128)
    prod_stack = np.empty(max_states, dtype=np.int64)

    # Start at a0 = f_q(0), NOT at 0
    top = 0
    z_stack[0] = 1.0 - q
    prod_stack[0] = 1

    while top >= 0:
        z = z_stack[top]
        prod = prod_stack[top]
        top -= 1

        max_n = max_prod // prod

        for n in range(2, max_n + 1):
            zn = cpow(z, n)
            denom = zn - 1.0

            # singularity in f_q(zn)
            if abs(denom) < eps:
                return True

            y_val = 1.0 + q / denom   # = f_q(z^n)

            # Run your old test on this y_val
            if old_dense_test_from_y(q, y_val, N, eps):
                return True

            new_prod = prod * n

            # Only continue if another factor >= 2 could still fit
            if new_prod * 2 <= max_prod:
                top += 1
                if top >= max_states:
                    return False
                z_stack[top] = y_val
                prod_stack[top] = new_prod

    return False


@njit(parallel=True)
def compute_mask(xrange, yrange, max_prod, N):
    nx = len(xrange)
    ny = len(yrange)
    mask = np.zeros((ny, nx), dtype=np.bool_)

    for ix in prange(nx):
        x = xrange[ix]
        for iy in range(ny):
            y = yrange[iy]
            q = x + 1j * y
            mask[iy, ix] = checkDense_product_search_correct(q, max_prod, N)

    return mask


# Parameters
xrange = np.linspace(0, 1.5, 300)
yrange = np.linspace(-0.75, 0.75, 300)
N = 200
max_prod = 300

# Compute
mask = compute_mask(xrange, yrange, max_prod, N)

# Plot
XX, YY = np.meshgrid(xrange, yrange)
QQ = XX + 1j * YY
pts = QQ[mask]

plt.figure(figsize=(8, 6))
plt.scatter(pts.real, pts.imag, s=1)
plt.gca().set_aspect('equal')
plt.show()
plt.close()