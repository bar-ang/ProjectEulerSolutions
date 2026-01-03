from project_euler import Measure, Progress, validation, solution
from common.primes import prime_sieve
import numpy as np
from sympy import divisors

def pisano_period(n, lim=None):
    res = 1
    f0, f1 = 1, 1
    while f0 != 0 or f1 != 1:
        f0, f1 = f1, (f0 + f1) % n
        res += 1
        if lim and res > lim:
            return None
    return res

def solve(n, lim, recursive=True):
    a = np.array([
        [1, 1],
        [1, 0],
    ],dtype=object )

    mat = np.linalg.matrix_power(a, n)
    common_denom = np.gcd(mat[0,0]-1, mat[1, 1]-1)
    common_denom = np.gcd(common_denom, mat[0, 1])
    divs = divisors(common_denom)
    divs = [d for d in divs if d >= 2 and d <= lim and pisano_period(d) == n]
   
    return divs

def inverse_pisano(m, lim):
    lst = []
    c = 0
    for _, i in Progress(range(2, lim+1), "calculating inv pisano results", announce_every_seconds=13):
        p = pisano_period(i)
        if p is not None and p == m:
            lst.append(i)

    return lst


@validation
def validate():
    assert pisano_period(38) == 18
    assert pisano_period(76) == 18

    assert inverse_pisano(18, 100) == [19, 38, 76], inverse_pisano(18, 100)
    assert inverse_pisano(18, 50) == [19, 38], inverse_pisano(18, 50)
    
    for _, i in Progress(range(3, 11), "validating I"):
        sol = solve(i, 100)
        brute = inverse_pisano(i, 100)
        assert sum(brute) == sum(sol), (i, brute, sum(brute), sol)


    for _, i in Progress(range(10, 60), "validating II"):
        for j in range(50, 150, 21):
            sol = solve(i, j)
            brute = inverse_pisano(i, j)
            assert sum(brute) == sum(sol), (i, j, brute, sol)

    assert solve(18, 1000) == [19, 38, 76], solve(18, 1000)
    assert sum(solve(18, 50)) == 57, solve(18, 50)

@solution
def solve_all():
    return sum(solve(120, 10**9))
