class Polynomial:
    def __init__(self, *terms: int) -> None:
        self._terms = tuple(terms)

    def __str__(self) -> str:
        out = str(self._terms[0]) if self._terms and self._terms[0] else ""
        for p, term in enumerate(self._terms[1:], 1):
            if term == 0:
                continue
            if out:
                out += " + " if term > 0 else " - "
            if abs(term) != 1:
                out += str(abs(term))
            out += "x"
            if p > 1:
                out += f"^{p}"
        return out