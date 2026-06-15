from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from sys import stdout


from typing import Callable, Optional, Tuple, Set


from libs.effectiveinteractions import effectiveInteraction, IsDense


def update_progress(i, N):
        message = f"Progress: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()

it = -1
N = 101

x_min = 0.00001
x_max = np.pi

y_min = -np.pi / 3
y_max = np.pi / 3

def checkDense(q):
    EEI = (0, 0, 0, 0)
    for j in range(1, 50):
        EEI = effectiveInteraction(EEI, EEI, q)
        out = IsDense(EEI, q)
        if out:
            return 1+j
    return False

ComplexFn = Callable[[complex], complex]


def check(q, depth = 300):
    def f(y):
        return 1 + q / (y - 1)

    y = 0
    y_vals = set([0])

    stack = [(y, depth)]
    while stack:
        to_add = set()
        y, cur_depth = stack.pop()
        if cur_depth <= 1:
            continue

        if abs(y) > 1 or abs(f(y)) > 1:
            return True

        # for y_val in y_vals:
            # stack.append((y*y_val, cur_depth-1))
            # to_add.add(y*y_val)
            # stack.append((f(f(y)*f(y_val)), cur_depth-1))
            # to_add.add(f(f(y)*f(y_val)))
        for j in range(2, cur_depth):
            stack.append((f(y ** j), cur_depth // j))
            to_add.add(f(y ** j))
            # stack.append()
        y_vals.update(to_add)
    return False



grid = np.zeros((2*N, N))
for x in np.linspace(x_min, x_max, N):
    it += 1
    ity = -1
    for y in np.linspace(-y_max, 0, N+1):
        ity += 1
        q = complex(x, y)

        out = checkDense(q)
    
        grid[ity, it] += out
        if ity == N:
            continue
        grid[-ity, it] += out
        continue

    update_progress(it, N-1)
print("\n")


circle1 = plt.Circle((0.5, 0), 0.5, color='r', fill = False)

circle2 = plt.Circle((1, 0), 1, color='r', fill = False)
fig, ax = plt.subplots()
# ax.add_patch(circle1)
# ax.add_patch(circle2)
# ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


ax.xaxis.set_major_locator(MultipleLocator(0.5))
# optional: label format
ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))


# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
cmap = ListedColormap(["white", "green", "red", "blue"])
ax.imshow(grid, extent=[x_min,x_max, -y_max, y_max]) #, cmap=cmap, vmin=0, vmax=3, interpolation="nearest"
plt.savefig("out.png", dpi = 300)
plt.show()
