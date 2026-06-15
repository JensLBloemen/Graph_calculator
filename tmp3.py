import numpy as np
import matplotlib.pyplot as plt

def f_q(z, q):
    return 1 + q / (z - 1)

def quantize(z, eps):
    return (
        np.round(z.real / eps).astype(np.int64),
        np.round(z.imag / eps).astype(np.int64)
    )



def build_generated_shape(
    q,
    steps=30,
    eps=1e-3,
    max_abs=5,
    pair_chunk=300_000,
    pole_tol=1e-10,
    verbose=True,
    break_on_escape=True
):
    """
    Approximate the limiting generated set by binning points onto an eps-grid.

    V_0 = {0}
    V_{n+1} = V_n union V_n^2 union f_q(V_n)

    where V_n^2 = {v*w : v,w in V_n}.

    If break_on_escape=True, the process stops as soon as a generated point
    satisfies |z| > max_abs.
    """

    keys = set()
    escaped = False
    escaped_point = None

    def add_points(arr):
        nonlocal escaped, escaped_point

        arr = np.asarray(arr, dtype=complex).ravel()

        finite_mask = (
            np.isfinite(arr.real)
            & np.isfinite(arr.imag)
        )

        arr = arr[finite_mask]

        if len(arr) == 0:
            return np.array([], dtype=complex)

        # Check escape before filtering
        escape_mask = np.abs(arr) > max_abs

        if break_on_escape and np.any(escape_mask):
            escaped = True
            escaped_point = arr[escape_mask][0]
            return np.array([], dtype=complex)

        # Keep only points inside max_abs
        arr = arr[~escape_mask]

        if len(arr) == 0:
            return np.array([], dtype=complex)

        kr, ki = quantize(arr, eps)

        new = []
        for a, b in zip(kr, ki):
            key = (int(a), int(b))
            if key not in keys:
                keys.add(key)
                new.append(eps * (a + 1j * b))

        return np.array(new, dtype=complex)

    points = add_points(np.array([0 + 0j]))
    frontier = points.copy()

    history = [points.copy()]

    for step in range(1, steps + 1):
        old_points = points.copy()
        new_step = []

        if len(frontier) == 0:
            break

        rows_per_chunk = max(1, pair_chunk // max(1, len(old_points)))

        for start in range(0, len(frontier), rows_per_chunk):
            X = frontier[start:start + rows_per_chunk]

            # Operation 1: all products x*y
            prod = X[:, None] * old_points[None, :]
            new_prod = add_points(prod)

            if escaped:
                if verbose:
                    print(
                        f"Stopped at step {step}: point escaped max_abs. "
                        f"|z| = {abs(escaped_point):.6g}, z = {escaped_point}"
                    )
                return points, history, escaped

            if len(new_prod) > 0:
                new_step.append(new_prod)

            # Operation 2: f_q(x)
            valid_X = np.abs(X - 1) > pole_tol
            X_safe = X[valid_X]

            if len(X_safe) > 0:
                f_X = f_q(X_safe, q)
                new_f = add_points(f_X)

                if escaped:
                    if verbose:
                        print(
                            f"Stopped at step {step}: point escaped max_abs. "
                            f"|z| = {abs(escaped_point):.6g}, z = {escaped_point}"
                        )
                    return points, history, escaped

                if len(new_f) > 0:
                    new_step.append(new_f)

        if len(new_step) == 0:
            if verbose:
                print("No new grid cells added. Shape stabilized numerically.")
            break

        frontier = np.concatenate(new_step)
        points = np.concatenate([points, frontier])

        history.append(points.copy())

        if verbose:
            print(
                f"Step {step}: cells = {len(points)}, "
                f"new cells = {len(frontier)}"
            )
    if step == steps:
        return points, history, True ## no convergence yet
    return points, history, escaped

def T_q(z, q):
    a = np.sqrt(q)
    return (z - (1 + a)) / (z - (1 - a))

def plot_shape_f_and_T(points, q, plot_radius=None, T_plot_radius=10, pole_tol=1e-10):
    fig, axes = plt.subplots(1, 3, figsize=(21, 7))

    theta = np.linspace(0, 2*np.pi, 1000)
    unit_circle = np.exp(1j * theta)

    # ------------------
    # Plot V
    # ------------------
    axes[0].scatter(points.real, points.imag, s=2)
    axes[0].plot(unit_circle.real, unit_circle.imag, linewidth=1.5, label=r"$|z|=1$")
    axes[0].axhline(0, linewidth=0.5)
    axes[0].axvline(0, linewidth=0.5)
    axes[0].set_title(r"Approximate generated shape $V$")
    axes[0].set_xlabel("Re")
    axes[0].set_ylabel("Im")
    axes[0].axis("equal")
    axes[0].legend()

    # ------------------
    # Plot f_q(V)
    # ------------------
    valid = np.abs(points - 1) > pole_tol
    fpoints = f_q(points[valid], q)

    if plot_radius is not None:
        fpoints = fpoints[np.abs(fpoints) <= plot_radius]

    axes[1].scatter(fpoints.real, fpoints.imag, s=2)
    axes[1].plot(unit_circle.real, unit_circle.imag, linewidth=1.5, label=r"$|z|=1$")
    axes[1].axhline(0, linewidth=0.5)
    axes[1].axvline(0, linewidth=0.5)
    axes[1].set_title(r"Image $f_q(V)$")
    axes[1].set_xlabel("Re")
    axes[1].set_ylabel("Im")
    axes[1].axis("equal")
    axes[1].legend()

    # ------------------
    # Plot T(V)
    # ------------------
    a = np.sqrt(q)
    fixed_minus = 1 - a

    valid_T = np.abs(points - fixed_minus) > pole_tol
    Tpoints = T_q(points[valid_T], q)

    Tpoints = Tpoints[
        np.isfinite(Tpoints.real)
        & np.isfinite(Tpoints.imag)
        & (np.abs(Tpoints) <= T_plot_radius)
    ]

    axes[2].scatter(Tpoints.real, Tpoints.imag, s=2)
    axes[2].plot(unit_circle.real, unit_circle.imag, linewidth=1.5, label=r"$|w|=1$")
    axes[2].axhline(0, linewidth=0.5)
    axes[2].axvline(0, linewidth=0.5)
    axes[2].set_title(r"Transformed set $T(V)$")
    axes[2].set_xlabel("Re")
    axes[2].set_ylabel("Im")
    axes[2].axis("equal")
    axes[2].legend()

    if plot_radius is not None:
        for ax in axes[:2]:
            ax.set_xlim(-plot_radius, plot_radius)
            ax.set_ylim(-plot_radius, plot_radius)

    if T_plot_radius is not None:
        axes[2].set_xlim(-T_plot_radius, T_plot_radius)
        axes[2].set_ylim(-T_plot_radius, T_plot_radius)

    fig.suptitle(f"q = {q}")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    q = 32/27 + 0.3*1j

    points, history, escaped = build_generated_shape(q, 300, 1e-2, 1, verbose=True)
    print(escaped)
    plot_shape_f_and_T(points, q, plot_radius=3)