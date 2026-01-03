from project_euler import Measure, Progress, validation, solution, Test
from sympy import fibonacci, lucas
import math
from itertools import chain, combinations

def delta(n):
    if n == 0:
        return 6
    return (lucas(2*n+5) - lucas(2*n-1))//2

def spaced_subsets(op, n, diff=3, min=1):
    def calc(n, diff, min):
        if n < min:
            return []
        prev = calc(n-1, diff, min)
        curr = [[n]]
        for lst in prev:
            curr.append(lst)
            if max(lst) <= n - diff:
                curr.append(lst+[n])
        return curr
    res = calc(n, diff, min)
    return [sum([op(t) for t in lst]) for lst in res]

# 000100100.001001000 - delta(1)
# 010010000.000010010 - delta(2)

def solve(count):
    n = 0
    while delta(n) <= count:
        n += 1

    # phi-palindromes of type #1 - with the 1st bit off
    q1 = spaced_subsets(delta, n, diff=3)
    q1 = [t for t in q1 if t <= count]

    # phi-palindromes of type #2 - with the 1st bit on
    q2 = spaced_subsets(delta, n, diff=3, min=2)
    q2 = [t+2 for t in q2 if t+2 <= count]
    
    q = q1 + q2

    # adding irregular numbers
    q += [0, 1, 2]
    
    q.sort()
    return sum(q)

@validation
def validate():
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

        def calc(self, n, func, sign):
            assert abs(sign) == 1
            if n > 0:
                return int(func(n))
            elif n == 0:
                return 1 + sign
            else:
                return int(func(-n)) * (sign * (-1)**(-n))
            
        def unique(self):
            self.powers.sort()
            diffs = [self.powers[i+1] - p for i, p in enumerate(self.powers[:-1])]
            return all([abs(d) != 1 for d in diffs])

        def __gt__(self, n):
            return 5 * self.irrational ** 2 > (n - self.rational) ** 2

        @property
        def rational(self):
            return sum([self.calc(n, lucas, 1) for n in self.powers]) / 2

        @property
        def irrational(self):
            return sum([self.calc(n, fibonacci, -1) for n in self.powers]) / 2

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

    nums = range(50)
    for a in nums:
        for b in nums:
            for c in nums:
                if a == b or a ==c or b == c:
                    continue
                phi_a = Phidigital(a)
                phi_b = Phidigital(b)
                phi_c = Phidigital(c)
                phi = phi_a + phi_b + phi_c
                assert phi.rational == sum([k.rational for k in [phi_a, phi_b, phi_c]]), phi
                assert phi.irrational == sum([k.irrational for k in [phi_a, phi_b, phi_c]]), phi

    def all_phi_palindromes(n):
        result = []
        num = 0
        while True:
            phi = Phidigital.empty()
            bit = 0
            k = num
            while k > 0:
                if k & 1:
                    phi += Phidigital(bit) + Phidigital(-bit-1)
                bit += 1
                k >>= 1
            if phi.rational > n:
                break
            if phi.unique():
                result.append(phi)
            num += 1
        return result

    pals = all_phi_palindromes(1000)
    pals = [int(p.rational) for p in pals if p.irrational == 0]
    assert sum(pals)+1 == 4345, sum(pals)
    Test.equals(4345, solve, 1000)


@solution
def solve_all():
    return solve(10 ** 10)
