import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.widgets import CheckButtons, Button
from matplotlib.ticker import MultipleLocator

# -----------------------------
# Settings
# -----------------------------
folder = "npy_files"

x_min = -0.001
x_max = 2.0001

y_min = -1
y_max = 1

plot_title = r""
x_label = r"$\mathrm{Re}(q)$"
y_label = r"$\mathrm{Im}(q)$"

tick_interval = 0.5

show_circles = True
show_grid = False

output_filename = "out.png"

cmap = ListedColormap(["white", "blue", "orange"])

# -----------------------------
# Load all .npy files
# -----------------------------
filenames = sorted([f for f in os.listdir(folder) if f.endswith(".npy")])

if not filenames:
    raise FileNotFoundError(f"No .npy files found in '{folder}'")

layers = []

for fname in filenames:
    arr = np.load(os.path.join(folder, fname)).astype(int)
    if "Z" == fname[0]:
        arr *= 2
    layers.append(arr)

layers = np.stack(layers)  # shape: (n_files, H, W)

# All layers initially off
active = np.zeros(len(filenames), dtype=int)


def compute_display():
    selected = layers[active.astype(bool)]

    if selected.size == 0:
        return np.zeros(layers.shape[1:], dtype=int)

    # 0 = white, 1 = blue, 2 = orange
    # If orange and blue overlap, orange wins.
    return np.max(selected, axis=0)


def draw_plot(ax, display_data):
    """
    Draws only the mathematical plot.
    Used both for the interactive figure and the clean saved figure.
    """

    img = ax.imshow(
        display_data,
        extent=[x_min, x_max, y_min, y_max],
        origin="lower",
        cmap=cmap,
        interpolation="nearest",
        vmin=0,
        vmax=2,
    )

    ax.set_title(plot_title, fontsize=16)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    ax.xaxis.set_major_locator(MultipleLocator(tick_interval))
    ax.yaxis.set_major_locator(MultipleLocator(tick_interval))

    # Style like your example: x-axis through Im(q)=0
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["left"].set_position(("outward", 0))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")

    # Move x-label close to the right side of the horizontal axis
    y0_axes = (0 - y_min) / (y_max - y_min)
    ax.xaxis.set_label_coords(0.96, y0_axes - 0.10)

    if show_grid:
        ax.grid(True, linewidth=0.4, alpha=0.4)

    # Optional circles
    if show_circles:
        circle1 = plt.Circle((1, 0), 1, color="r", fill=False, linewidth=1.2)
        ax.add_patch(circle1)

        circle2 = plt.Circle((1 + 1/3, 0), 1 / 3, color="g", fill=False, linewidth=1.2)
        ax.add_patch(circle2)

        circle3 = plt.Circle((0, 0), 1, color="g", fill=False, linewidth=1.2)
        ax.add_patch(circle3)

    # Optional contour curves
    X = np.linspace(x_min, x_max, 1000)
    Y = np.linspace(y_min, y_max, 1000)

    XX, YY = np.meshgrid(X, Y)
    q = XX + YY * 1j

    q_safe = np.where(q == 0, 1e-12 + 0j, q)

    # Change range(1, 1) to e.g. range(1, 10)
    # if you want contours for n = 1,...,9.
    for n in range(1, 1):
        F = 1 + (q_safe - 1) / q_safe * ((1 - q_safe) ** n - 1)
        Z = np.abs(F)

        ax.contour(X, Y, Z, levels=[1], colors="black")

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal", adjustable="box")

    return img


# -----------------------------
# Main interactive figure
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(left=0.35)

img = draw_plot(ax, compute_display())

# -----------------------------
# Check buttons
# -----------------------------
rax = plt.axes([0.02, 0.1, 0.28, 0.78])
check = CheckButtons(rax, filenames, actives=active.tolist())

label_to_idx = {name: i for i, name in enumerate(filenames)}


def on_toggle(label):
    idx = label_to_idx[label]
    active[idx] = not active[idx]

    img.set_data(compute_display())

    fig.canvas.draw_idle()


check.on_clicked(on_toggle)


# -----------------------------
# Save button
# Opens a new clean window with only the plot
# and saves it at dpi=300.
# -----------------------------
save_ax = plt.axes([0.02, 0.02, 0.28, 0.05])
save_button = Button(save_ax, "Open + save plot")


def open_and_save_clean_plot(event):
    display_data = compute_display()

    clean_fig, clean_ax = plt.subplots(figsize=(8, 6))

    draw_plot(clean_ax, display_data)

    clean_fig.tight_layout()

    clean_fig.savefig(
        output_filename,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.1,
    )

    clean_fig.show()

    print(f"Opened clean plot window and saved as {output_filename} at dpi=300")


save_button.on_clicked(open_and_save_clean_plot)

plt.show()