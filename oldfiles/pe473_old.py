from project_euler import Measure, Progress, validation, solution
from sympy import fibonacci, lucas
import math
from itertools import chain, combinations


class Phidigital:
    def empty():
        res = Phidigital(0)
        res.powers = []
        return res
    
    def __init__(self, n):
        self.powers = [n]

    def __repr__(self):
        return f"{self.rational} + {self.irrational}*sq(5)"

    def __add__(self, phi2):
        res = Phidigital(0)
        res.powers = self.powers + phi2.powers
        assert len(res.powers) == len(set(res.powers))
        return res

    @property
    def rational(self):
        def calc(n):
            if n > 0:
                return int(lucas(n))
            elif n == 0:
                return 2
            else:
                return int(lucas(-n)) * ((-1)**(-n))

        return sum([calc(n) for n in self.powers]) / 2

    @property
    def irrational(self):
        def calc(n):
            if n > 0:
                return int(fibonacci(n))
            elif n == 0:
                return 0
            else:
                return int(fibonacci(-n)) * ((-1)**(-n+1))

        return sum([calc(n) for n in self.powers]) / 2


def psi(n):
    return Phidigital(n) + Phidigital(-n-1)

def subset_sums(lst):
    subs = chain.from_iterable(combinations(lst, r) for r in range(len(lst) + 1))
    return [sum(s) for s in subs]


@validation
def validate():
    ph = Phidigital(8)
    assert ph.rational == 23.5, ph
    assert ph.irrational == 10.5, ph
    
    ph = Phidigital(19)
    assert ph.rational == 9349.0/2, ph
    assert ph.irrational == 4181.0/2, ph

    ph = Phidigital(1)
    assert ph.rational == 0.5, ph
    assert ph.irrational == 0.5, ph
    
    ph = Phidigital(0)
    assert ph.rational == 1, ph
    assert ph.irrational == 0, ph

    ph = Phidigital(-8)
    assert ph.rational == 23.5, ph
    assert ph.irrational == -10.5, ph
    
    ph = Phidigital(-19)
    assert ph.rational == -9349.0/2, ph
    assert ph.irrational == 4181.0/2, ph

    ph = Phidigital(-1)
    assert ph.rational == -0.5, ph
    assert ph.irrational == 0.5, ph

    ps = psi(7)
    assert ps.rational == 38, ps
    assert ps.irrational == -4, ps

    deltas = [2]
    count = 1000
    for n in range(0, 30):
        ra = psi(2*n) + psi(2*n + 3)
        ir = psi(2*n) + psi(2*n - 3)
        assert ra.irrational == 0, (n, ra)
        assert ir.rational == 0, (n, ir)
        r = int(ra.rational)
        if r <= count:
            deltas.append(r)
    deltas = list(set(deltas))
    deltas = subset_sums(deltas)
    deltas.sort()
    print(deltas)

    def all_phi_palindromes(n):
        """Return all numbers below `limit` as a list of exponents of powers of two."""
        result = []
        for num in range(1, 100*n):
            phi = Phidigital.empty()
            bit = 0
            k = num
            while k > 0:
                if k & 1:
                    phi += psi(bit)
                bit += 1
                k >>= 1
            result.append(phi)
        return result

    lst = all_phi_palindromes(count)
    assert len(lst) == count, len(lst)
    
    lst = [int(t.rational) for t in lst if t.irrational == 0]
    lst = [t for t in lst if t <= count]
    print(f"num palindromes below {count}: {len(lst)}")
    print(f"sum palindromes below {count}: {sum(lst)}")
    print(lst)
    deltas = [d for d in deltas if d < count]
    non = [p for p in lst if p not in deltas]
    assert len(non) == 0, f"{min(non)} is an integer palindrom that is not capture by delta."
    assert sum(deltas) == 4345, sum(deltas)

@solution
def solve_all():
    return 111111
