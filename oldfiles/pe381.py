from project_euler import Progress, Measure, solution, validation
from common.primes import Primes

LIM = 10**8

def factorial_modulo(n, p):
    if n >= p:
        return 0
    res = 1
    for i in range(2, n+1):
        res *= i
        res %= p
    return res

def solve_single(p):
    p_1 = p - 1
    p_2 = p_1 * pow(-1, -1, p)
    p_3 = p_2 * pow(-2, -1, p)
    p_4 = p_3 * pow(-3, -1, p)
    p_5 = p_4 * pow(-4, -1, p)
    s = (p_1 + p_2 + p_3 + p_4 + p_5) % p
    return s

def solve(lim):
    with Measure("prime sieving"):
        primes = Primes(lim)
    res = 0
    for _, p in Progress(primes, announce_every=8.63254, iterable_len=10):
    #for p in primes:
        if p < 5:
            continue
        res += solve_single(p)
    return res

@validation
def validate():
    primes = Primes(200)
    for _, p in Progress([p for p in primes if p < 100 and p >= 5], "validating A"):
        assert p-1 == factorial_modulo(p-1, p), (p, p-1, factorial_modulo(p-1, p))

    assert solve_single(7) == 4, solve_single(7)
    assert sum([solve_single(p) for p in primes if p < 100 and p >= 5]) == 480, sum([solve_single(p) for p in primes if p < 100 and p >= 5])
    assert solve(100) == 480, solve(100)

@solution
def solve_all():
    return solve(LIM)