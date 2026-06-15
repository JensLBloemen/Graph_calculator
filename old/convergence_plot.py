
from libs.effectiveinteractions import effectiveInteraction, IsDense

q = complex(5, 0.1)

x = (0,0,0,0)
def dif(x, y):
    eps = 1e-5
    return sum(abs(x[i] - y[i]) for i in range(4)) < eps


def caseCheck(y, q, eps = 1e-2):
    b = y[1]

    if abs(b-1) < eps:
        return 1
    
    if abs(q-2+b+b**2) < eps:
        return 2
    
    if abs(q-2+2*b**2) < eps:
        return 3
    
    if abs((q-2)**2+(3*q-7)*b + (2+q)*b**2+b**3) < eps:
        return 4
    
    if abs(y[-1] - 2) < eps:
        return 5
    # print(abs(b / y[0] + 1 - q))
    return 6

from sys import stdout
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



def update_progress(i, N):
        message = f"Progress: [{'-'*((i*40)//N)+' '*(40 - (i*40)//N)}]  {i}/{N}"
        stdout.write(message)
        stdout.write('\r'*len(message))
        stdout.flush()


def f(y, q):
    return abs(1+q / (y - 1)) > 1

N = 101
x_min, x_max = -4, 5
y_min, y_max = -5, 5

grid = np.zeros((N, N))

hits = np.zeros(6)

itx = -1
for x in np.linspace(x_min, x_max, N):
    itx += 1
    update_progress(itx, N)
    ity = -1
    for y in np.linspace(y_max, y_min, N):
        ity += 1
        q = complex(x, y)
        E = lambda x: effectiveInteraction(x, x, q)
        x2 = (0,0,0,0)
        for _ in range(10000):
            x_old = x2

            x2 = E(x2)
            if dif(x2, x_old) or abs(x2[-1].real - 2) < 1e-2:
                # if abs(x2[-1] - 2) < 1e-2:
                #     print(x2)
                #     raise RuntimeError
                if abs(x2[-1] - 2) < 1e-2 and not abs(x2[0]) > 100:
                    continue
                b = x2[1]
                if 1 or IsDense(x2, q):
                    grid[ity][itx] = caseCheck(x2, q)
                hits[caseCheck(x2, q) - 1] += 1
                break
        # if abs(x2[1]) > 10:
        #     grid[ity][itx] = 5
        if not grid[ity][itx]:
            hits[caseCheck(x2, q) - 1] += 1
            # print(x2, caseCheck(x2,q))
print(hits)


im = plt.imshow(grid, extent=[x_min,x_max, y_min, y_max])

values = list(range(6))
labels = {0: "No convergence", 1: "$y^{112}=1$", 2: "Case 2"}

colors = [ im.cmap(im.norm(value)) for value in values]
# create a patch (proxy artist) for every color 
patches = [ mpatches.Patch(color=colors[i], label=labels.get(i, str(i))) for i in range(len(values)) ]
# put those patched as legend-handles into the legend
plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )

plt.show()
