class Polynomial:
    def __init__(self, *terms: int) -> None:
        self._terms = tuple(terms) if terms else (0,)

    def _trim(self, terms: tuple[int, ...]) -> "Polynomial":
        # trim trailing zeros (keep at least one term)
        while len(terms) > 1 and terms[-1] == 0:
            terms = terms[:-1]
        return Polynomial(*terms)

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented

        n = max(len(self._terms), len(other._terms))
        a = self._terms + (0,) * (n - len(self._terms))
        b = other._terms + (0,) * (n - len(other._terms))

        terms = tuple(x + y for x, y in zip(a, b))
        return self._trim(terms)

    def __neg__(self):
        return Polynomial(*(-t for t in self._terms))

    def __sub__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented
        return self.__add__(-other)

    def __rsub__(self, other):
        # allows: 0 - p or (other Polynomial) - self
        if other == 0:
            return -self
        if isinstance(other, Polynomial):
            return other.__sub__(self)
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented
        # compare after trimming trailing zeros
        a = list(self._terms)
        b = list(other._terms)
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        while len(b) > 1 and b[-1] == 0:
            b.pop()
        return a == b

    def __radd__(self, other):
        # makes sum([p1, p2, ...]) work (since sum starts with 0)
        if other == 0:
            return self
        return self.__add__(other)

    def __str__(self) -> str:
        if not self._terms or all(t == 0 for t in self._terms):
            return "0"

        out_parts = []
        first = True

        for p, term in enumerate(self._terms):
            if term == 0:
                continue

            # sign
            if first:
                sign = "-" if term < 0 else ""
            else:
                sign = " - " if term < 0 else " + "

            a = abs(term)

            # body (without sign)
            if p == 0:
                body = str(a)
            else:
                body = ""
                if a != 1:
                    body += str(a)
                body += "x"
                if p > 1:
                    body += f"^{p}"

            out_parts.append(sign + body)
            first = False

        return "".join(out_parts)

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented

        # quick zero checks
        if len(self._terms) == 1 and self._terms[0] == 0:
            return Polynomial(0)
        if len(other._terms) == 1 and other._terms[0] == 0:
            return Polynomial(0)

        a = self._terms
        b = other._terms
        res = [0] * (len(a) + len(b) - 1)

        for i, ai in enumerate(a):
            if ai == 0:
                continue
            for j, bj in enumerate(b):
                if bj == 0:
                    continue
                res[i + j] += ai * bj

        return self._trim(tuple(res))

    def __rmul__(self, other):
        # optional: allow integer * Polynomial
        if isinstance(other, int):
            if other == 0:
                return Polynomial(0)
            return self._trim(tuple(other * t for t in self._terms))
        if isinstance(other, Polynomial):
            return other.__mul__(self)
        return NotImplemented
    
    def __divmod__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented

        # trim local copies
        a = list(self._terms)
        b = list(other._terms)
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        while len(b) > 1 and b[-1] == 0:
            b.pop()

        # division by zero polynomial
        if len(b) == 1 and b[0] == 0:
            raise ZeroDivisionError("polynomial division by zero")

        # zero dividend
        if len(a) == 1 and a[0] == 0:
            return Polynomial(0), Polynomial(0)

        deg_a = len(a) - 1
        deg_b = len(b) - 1

        # degree too small => quotient 0, remainder is dividend
        if deg_a < deg_b:
            return Polynomial(0), self._trim(tuple(a))

        q = [0] * (deg_a - deg_b + 1)

        # long division (assumes exact division; will raise if not exact)
        while deg_a >= deg_b and not (len(a) == 1 and a[0] == 0):
            lead_a = a[-1]
            lead_b = b[-1]

            if lead_b == 0:
                raise ZeroDivisionError("invalid divisor leading term is zero (after trim)")

            # exact step (integer coeffs)
            if lead_a % lead_b != 0:
                raise ValueError("non-exact division (coefficients not divisible)")

            coef = lead_a // lead_b
            shift = deg_a - deg_b
            q[shift] = coef

            # subtract coef * b * x^shift from a
            for i in range(deg_b + 1):
                a[i + shift] -= coef * b[i]

            # trim a and update deg_a
            while len(a) > 1 and a[-1] == 0:
                a.pop()
            deg_a = len(a) - 1

        return self._trim(tuple(q)), self._trim(tuple(a))

    def __truediv__(self, other):
        q, r = divmod(self, other)
        if r != Polynomial(0):
            raise ValueError("division has non-zero remainder")
        return q

    def __floordiv__(self, other):
        # optional: allow p // q as exact division too
        return self.__truediv__(other)

    def __repr__(self):
        return str(self)