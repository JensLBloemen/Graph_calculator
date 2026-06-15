import numpy as np
import matplotlib.pyplot as plt

xrange = np.linspace(0, 2.5, 1000)
yrange = np.linspace(-1.2, 1.2, 1000)
XX, YY = np.meshgrid(xrange, yrange)

old_mask = np.zeros((1000, 1000), dtype=bool)
QQ = XX + 1j * YY
out = QQ


for n in range(1, 100):
    # plt.figure()
    print(f"{n=}")

    mask = (
        (np.abs(
            (((QQ - 2) ** n - (-1) ** n) / ((QQ - 2) ** (n + 1) + (-1) ** n))**2
            * (QQ - 1) * (QQ - 2)
            
        ) > 1)

        |

        (np.abs(1 + QQ / ((((QQ - 2) ** n - (-1) ** n) / ((QQ - 2) ** (n + 1) + (-1) ** n)) ** 2
            * (QQ - 1) * (QQ - 2) - 1)
            ) > 1)

    )

    old_mask = old_mask | mask   # accumulate all previous masks

    pts = out[old_mask]

plt.scatter(pts.real, pts.imag, s=1)
plt.gca().set_aspect('equal')
plt.savefig(f"pics/{n}.png")
plt.close()