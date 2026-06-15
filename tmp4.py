import numpy as np
import matplotlib.pyplot as plt

q = 0.9
r = (2-q)**0.5

def g(z):
    return 1 + (q-1) / (z-1)

b = r - 0.0001*0
a = g(b)

print(a, b)

c = (a+b)/2
R = b - c

x = np.linspace(-2, 2, 1000)
y = np.linspace(-2, 2, 1000)

XX, YY = np.meshgrid(x, y)
z = XX + 1j * YY

mask = np.abs(z - c) < R

out = g(g(z)**2)

# Plot image of the masked disk under g
w = out[mask]
ax = plt.axes()

circle1 = plt.Circle((c, 0), R, color="r", fill=False, linewidth=1.2)
ax.add_patch(circle1)


plt.scatter(w.real, w.imag, s=0.1)
plt.gca().set_aspect("equal")
plt.xlim(a-0.1, b+0.1)
plt.ylim(-R-0.1, R+0.1)
plt.grid(True)
plt.show()