from classes.polynomial import Polynomial as P
X = P(0, 1)

def get111_triangle(p: P, q: P) -> P:
    r1 = p[0] * q[0] / X
    r2 = p[3] * q[3] / (X*(X-1))
    return r1 + r2

def get112_triangle(p: P, q: P) -> P:
    r1 = p[0] * q[1] / X
    r2 = p[3] * q[2] / (X*(X-1))
    r3 = p[3] * q[4] / (X*(X-1))
    return r1 + r2 + r3

def get121_triangle(p: P, q: P) -> P:
    r1 = p[2] * q[0] / X
    r2 = p[1] * q[3] / (X*(X-1))
    r3 = p[4] * q[3] / (X*(X-1))
    return r1 + r2 + r3

def get122_triangle(p: tuple[P], q: tuple[P]) -> P:
    r1 = p[2] * q[1] / (X*(X-1))
    r2 = p[1] * q[2] / (X*(X-1))
    r3 = p[4] * q[4] / (X*(X-1)*(X-2))
    return r1 + r2 + r3

def get123_triangle(p: tuple[P], q: tuple[P]) -> P:
    r1 = p[4] * q[4] / (X*(X-1)*(X-2)) * (X-3)
    r2 = p[4] * q[2] / (X*(X-1))
    r3 = p[2] * q[1] / (X*(X-1)) * (X-2)
    r4 = p[1] * q[4] / (X*(X-1))
    return r1 + r2 + r3 + r4

def get_triangle(p, q):
    return (get111_triangle(p,q), get112_triangle(p, q), get121_triangle(p, q), get122_triangle(p,q), get123_triangle(p,q))

def get111_star(p, q) -> P:
    return p[0] * q[0] / X + p[1] * q[2] / (X*(X-1))

def get112_star(p, q) -> P:
    return p[0] * q[1] / X + p[1] * q[4] / (X*(X-1)) + p[1] * q[3] / (X*(X-1))

def get121_star(p, q) -> P:
    return p[2] * q[0] / X + p[4] * q[2] / (X*(X-1)) + p[3] * q[2] / (X*(X-1))

def get122_star(p, q) -> P:
    return p[2] * q[1] / (X*(X-1)) + p[3] * q[3] / (X*(X-1)) + p[4] * q[4] / (X*(X-1)*(X-2))

def get123_star(p, q) -> P:
    p1 = p[3] * q[4] / (X*(X-1))
    p2 = p[4] * q[3] / (X*(X-1))
    p3 = p[4] * q[4] / (X*(X-1)*(X-2))*(X-3)
    p4 = p[2] * q[1] / (X*(X-1))*(X-2)
    return p1 + p2 + p3 + p4

def get_star(p, q):
    return (get111_star(p,q), get112_star(p, q), get121_star(p, q), get122_star(p,q), get123_star(p,q))



