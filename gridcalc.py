from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from sys import stdout

from numba import njit
from typing import Callable, Optional, Tuple, Set

from random import random
from libs.effectiveinteractions import effectiveInteractionStar, effectiveInteractionTriangle, square_proj


def update_progress(i, N):
        message = f"Progress: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()

it = -1
N = 1001

x_min = 0.001
x_max = 2.1

y_min = -1
y_max = 1
depth = 2


@njit(cache = True, fastmath=True)
def checkDFS(q, y_start = 0, depth = 300):
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


def get_wheel(n, q, k = 1):
    def f(y):
        return 1 + q / (y - 1)
    EEI = (0, 0 ,0, 0)
    EEI_start = EEI
    for _ in range(n):
        EEI = effectiveInteractionStar(EEI, EEI_start, q)
    return EEI


def get_vampire(n, q):
    EEI = (0,0,0,0)
    for _ in range(n):
        EEI = effectiveInteractionTriangle(EEI, EEI, q)
    return EEI




def get_ys(q, depth=10):
    found = {0}
    stack = [(0, depth)]
    seen_states = {(0, depth)}   # avoids recomputing identical subtrees

    def f(y):
        if y == 1:
            return 0
        return 1 + q / (y - 1)

    stack_append = stack.append
    found_add = found.add
    seen_add = seen_states.add

    while stack:
        yval, cur_depth = stack.pop()
        if cur_depth <= 2:
            continue

        fy = f(yval)

        # p = fy**n, built incrementally instead of repeated exponentiation
        p = fy * fy  # n = 2
        for n in range(2, cur_depth):
            new_depth = cur_depth // n

            state = (p, new_depth)
            if state not in seen_states:
                seen_add(state)
                stack_append(state)

            found_add(f(p))
            p *= fy

    return found


from random import choice, random
def get_ys2(q, depth=20):
    found = set([0])
    ys = [0]
    def f(y):
        if y == 1: return 0
        return 1 + q / (y - 1)
    for _ in range(depth):
        y1 = choice(ys)
        y2 = choice(ys)
        if y1*y2 not in found and random() < 0.5:
            ys.append(y1 * y2)
            found.add(y1*y2)
        else:
            if f(f(y1)*f(y2)) in found:
                continue
            ys.append(f(f(y1)*f(y2)))
            found.add(f(f(y1)*f(y2)))
    return ys



def Fs(EEI, q):
    if abs(EEI[2]+EEI[3]+q-2) < 1e-6:
        return 0
    return (EEI[0] + EEI[3]) / (EEI[1]+EEI[2]+q-2) * (q - 1)




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


def checkDense(q):


    # EEI = (0,0,0, 1)
    # y = square_proj(EEI, EEI, q)
    # if checkDFS(q, depth=300):
    #         return 1
    ys = get_ys(q, depth=20)
    for yvalH in ys:
        # EEI = (0, 0, 0, yvalH)
        # EEI1 = (1/(q-3), (q-2) / (q-3), (q-2) / (q-3), (q-2) / (q-3), (q-2) / (q-3))
        
        # EEI1 = (1 / (yvalH + q  - 3), (q-2) / (yvalH + q  - 3), (q-2) / (yvalH + q  - 3), (yvalH + q-2) / (yvalH + q  - 3))
        yvalG = yvalH
        
        # EEI1 =  (yvalG * yvalH / (q - 1), yvalG, 1, yvalH)
        # # EEI1 = (EEI1[0], EEI1[1], EEI1[3], EEI1[2])
        EEI1 = (0,0,0,yvalH)
        EEI = EEI1

        for n in range(1, 100):
            # EEI = star_power(EEI1, n, q)
            EEI = effectiveInteractionStar(EEI, EEI1, q)
            

            EEIprime = (EEI[0], EEI[1], EEI[3], EEI[2])  #Switch s u

            y = square_proj(EEI, EEIprime, q)
            y = Fs(EEI, q)
            
            if checkDFS(q, y, depth=2):
                    return 1

            # y = Fs(EEI, q)
            # if checkDFS(q, y, depth=2):
            #         return 2
    # for n in range(1,50):
    #     EEI = (0,0,0,0)
    #     EEI1 = EEI
    #     for _ in range(n):
    #         EEI = effectiveInteractionStar(EEI, EEI1, q)
    #         EEIprime = (EEI[0], EEI[2], EEI[1], EEI[3])
    #     yvalG = square_proj(EEI, EEIprime, q)
    #     yvalH = 0
    #     EEI = (yvalG * yvalH / (q - 1), yvalG, 1, yvalH)
    #     EEI1 = EEI

    #     for n in range(1, 50):
    #         EEI = effectiveInteractionStar(EEI, EEI1, q)
    #         EEIprime = (EEI[0], EEI[2], EEI[1], EEI[3])
    #         y = square_proj(EEI, EEIprime, q)
    #         if checkDFS(q, y, depth=depth):
    #                 return 1

    # for n in range(1,50):
    #     EEI = (0,0,0,0)
    #     EEI1 = EEI
    #     for _ in range(n):
    #         EEI = effectiveInteractionStar(EEI, EEI1, q)
    #         EEIprime = (EEI[0], EEI[2], EEI[1], EEI[3])
    #     yvalH = square_proj(EEI, EEIprime, q)
    #     yvalG = 0
    #     EEI = (yvalG * yvalH / (q - 1), yvalG, 1, yvalH)
    #     EEI1 = EEI

    #     for n in range(1, 50):
    #         EEI = effectiveInteractionStar(EEI, EEI1, q)
    #         EEIprime = (EEI[0], EEI[2], EEI[1], EEI[3])
    #         y = square_proj(EEI, EEIprime, q)
    #         if checkDFS(q, y, depth=depth):
    #                 return 1
    return False


from os import listdir

grid = np.zeros((1001,1001), dtype=bool)

for files in listdir("npy_files/"):
    if not files.endswith(".npy"):
        continue
    grid |= np.array(np.load("npy_files/"+files)).astype(bool)
old_grid = grid

IGNOREOLD=False

grid = np.zeros((N, N))
for x in np.linspace(x_min, x_max, N):
    it += 1
    ity = -1
    for y in np.linspace(-y_max, 0, N//2+1):
        ity += 1
        q = complex(x, y)

        if not IGNOREOLD and old_grid[ity, it]:
            grid[ity, it] = 1
            grid[-ity, it] = 1
            continue
            
        out = checkDense(q)
    
        grid[ity, it] += out
        if ity == 0:
            continue
        grid[-ity, it] += out
        continue

    update_progress(it, N-1)
print("\n")


from os import listdir
counter = 1
while True:
    if f"out{counter}.npy" in listdir("npy_files//"):
        counter += 1
    else:
        break

np.save(f"npy_files//out{counter}.npy", grid)



# circle1 = plt.Circle((0.5, 0), 0.5, color='r', fill = False)

circle2 = plt.Circle((2, 0), 1, color='r', fill = False)
fig, ax = plt.subplots()
# ax.add_patch(circle1)
# ax.add_patch(circle2)
# ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


ax.xaxis.set_major_locator(MultipleLocator(0.25))
# optional: label format
ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))


# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
cmap = ListedColormap(["white", "green", "red", "blue"])
ax.imshow(grid, extent=[x_min,x_max, -y_max, y_max], cmap=cmap) #, cmap=cmap, vmin=0, vmax=3, interpolation="nearest"

ax.set_xlabel("$\\text{Re}(q)$", loc="right")
ax.set_ylabel("$\\text{Im}(q)$", loc="center")
plt.title("Wheel graphs")
plt.savefig("out.png", dpi = 300)
plt.show()

