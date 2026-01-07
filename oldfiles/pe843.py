from project_euler import Measure, Progress, validation, solution
from sympy import divisors

def S(n):
    res = [k-n for k in divisors(n*(n-1)) if k > n]
    res = [r for r in res if (n*(n-1)//(r+n) + r + n) % 2 == 1]
    return res

def T(n):
    prg = Progress.in_case(n > 90000 and n % 50000 == 0, S(n), f"calc T({n})")
    return sum([t for _, t in prg])

def U(n):
    return sum([T(k) for _, k in Progress(range(3, n+1))])

@validation
def validate():
    assert S(10) == [5, 8, 20, 35, 80], S(10)
    assert S(11) == [11, 44, 99], S(11)

    print(S(100))
    assert T(10) == 148
    assert T(100) == 21828, T(100)

    assert U(100) == 612572

@solution
def solve():
    return U(1234567)
