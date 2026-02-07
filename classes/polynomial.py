class Polynomial:
    def __init__(self, *terms: int) -> None:
        self._terms = tuple(terms)

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented

        n = max(len(self._terms), len(other._terms))
        a = self._terms + (0,) * (n - len(self._terms))
        b = other._terms + (0,) * (n - len(other._terms))

        terms = tuple(x + y for x, y in zip(a, b))

        # trim trailing zeros (keep at least one term if you want "0" polynomial)
        while len(terms) > 1 and terms[-1] == 0:
            terms = terms[:-1]

        return Polynomial(*terms)

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

            # build the term body (without sign)
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
