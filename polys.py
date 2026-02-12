from classes.polynomial import Polynomial as P
p0 = (P(), P(), P(), P(), P(0,2,-3, 1))
p1 = (P(), P(), P(), P(0,2,-3, 1), P(0,-6,11,-6,1))
p2 = (P(0,-4,8,-5,1), P(0,12,-28,23,-8,1), P(0,12,-28,23,-8,1), P(0,18,-39,29,-9,1), P(0,-54,135,-126,56,-12,1))
p3 = (
    P(0,-308, 1016, -1381, 1013, -437, 112, -16, 1),
    P(0, 708, -2600, 4061, -3557, 1926, -665, 144, -18, 1),
    P(0, 708, -2600, 4061, -3557, 1926, -665, 144, -18, 1),
    P(0, 1170, -4047, 5917, - 4839, 2447, -791, 161, - 19, 1),
    P(0, -2790, 10599, -17458, 16556, -10054, 4085, -1117, 199, -21, 1)
)

X = P(0,1)


def get_next111(p):
    return p[0]*p[0] / X + p[3] * p[3] / (X*X-X)

def get_next112(p):
    q1 = p[1]*p[0] / X
    q2 = p[2]*p[3] / (X*(X-1))
    q3 = p[-1] * p[3] / (X * (X-1))
    return q1+q2+q3

def get_next122(p):
    q1 = p[-1]*p[-1] / (X*(X-1)*(X-2))
    q2 = 2*p[1] * p[2] / (X*(X-1))
    
    return q1 + q2

def get_next123(p):
    q1 = p[-1] * p[-1] / (X*(X-1)*(X-2))*(X-3)
    q2 = 2 * p[-1]*p[1] / (X*(X-1))
    q3 = p[1]*p[1] / (X*(X-1))*(X-2)
    return q1+q2+q3

def get_next(p):
    return (get_next111(p), get_next112(p), get_next112(p), get_next122(p), get_next123(p))

assert get_next(p0) == p1
assert get_next(p1) == p2
assert get_next(p2) == p3


def get111(p: P, q: P) -> P:
    r1 = p[0] * q[0] / X
    r2 = p[3] * q[3] / (X*(X-1))
    return r1 + r2

def get112(p: P, q: P) -> P:
    r1 = p[0] * q[1] / X
    r2 = p[3] * q[2] / (X*(X-1))
    r3 = p[3] * q[4] / (X*(X-1))
    return r1 + r2 + r3

def get121(p: P, q: P) -> P:
    r1 = p[2] * q[0] / X
    r2 = p[1] * q[3] / (X*(X-1))
    r3 = p[4] * q[3] / (X*(X-1))
    return r1 + r2 + r3

def get122(p: tuple[P], q: tuple[P]) -> P:
    r1 = p[2] * q[1] / (X*(X-1))
    r2 = p[1] * q[2] / (X*(X-1))
    r3 = p[4] * q[4] / (X*(X-1)*(X-2))
    return r1 + r2 + r3

def get123(p: tuple[P], q: tuple[P]) -> P:
    r1 = p[4] * q[4] / (X*(X-1)*(X-2)) * (X-3)
    r2 = p[4] * q[2] / (X*(X-1))
    r3 = p[2] * q[1] / (X*(X-1)) * (X-2)
    r4 = p[1] * q[4] / (X*(X-1))
    return r1 + r2 + r3 + r4

def get(p, q):
    return (get111(p,q), get112(p, q), get121(p, q), get122(p,q), get123(p,q))

### 0:111, 1:112, 2: 121, 3:122, 4:123

assert get(p0, p0) == p1
assert get(p1, p1) == p2
assert get(p2, p2) == p3
