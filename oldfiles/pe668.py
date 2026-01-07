from project_euler import Measure, Progress, validation, solution
from common.primes import prime_sieve
from math import sqrt, floor
from numba import jit

def is_root_smooth(n, primes):
    if n == 1:
        return True
    p = max([p for p in primes if n % p == 0])
    return p * p < n

def brute_force(n, primes):
    return len([i for i in range(1, n+1) if is_root_smooth(i, primes)])

def solve_efficient(n):
    m = int(sqrt(n))
    sum_primes = 0
    sum_non_primes = 0
    sum_integers = sum([n // t for _, t in Progress(range(m+1, n+1), "summing ints")])
    prime = [1] * (m + 1)

    p = 2
    while p * p <= n:
        if prime[p] == 1:
            sum_primes += p
            for i in range(2 * p, n + 1, p):
                if i <= m:
                    prime[i] = 0
                else:
                    sum_non_primes += n // i
        p += 1

    print(sum_primes, sum_integers, sum_non_primes)
    return n - (sum_primes + sum_integers - sum_non_primes)

def _solve(n):
    m = int(sqrt(n))
    attrib_low = list(range(m + 1))
    attrib_high = [n // i for i in range(m+1, n+1)]
    attrib = attrib_low + attrib_high
    attrib[1] = 0
    p = 2
    with Measure("Sieving...", print_threshold_sec=2):
        while p * p <= n:
            if attrib[p] > 0:
                for i in range(p * p, n + 1, p):
                    attrib[i] = 0
            p += 1

    with Measure("Finishing...", print_threshold_sec=2):
        return n-sum(attrib)

def sum_floor_series(n, m):
    '''
    this will return the the sum k=1 to n of floor(n/k).
    n must be square number
    m must be the square root of n (for optimiazation))
    '''
    assert m * m == n

    s = m
    for _, k in Progress(range(1, m), "series sum!"):
        s += (k+1) * (n//k)
        s -= k * (n//(k+1))

    return s

def solve(n):
    m = int(sqrt(n))
    sum_low = 0
    sum_high = 0
    sum_all = sum_floor_series(n, m) - sum([n//k for k in range(1, m+1)])
    dep = []
    
    primes = [1] * (m+1)
    primes[0] = 0
    primes[1] = 0
    with Measure("Sieving...", print_threshold_sec=2):
        for _, p in Progress(range(2, m+1), "sieveing", announce_every=1):
            if primes[p] == 1:
                sum_low += p
                rng = range(p * p, n + 1, p)
                if p < 20:
                    rng = Progress(rng, "INNER(%s)" % p, announce_every=1.4132)
                else:
                    rng = enumerate(rng)
                for _, i in rng:
                    if i <= m:
                        primes[i] = 0
                    else:
                        if True:
                            break
                        h = int(sqrt(p))
                        for _, j in enumerate(range(2, h+1)): #Progress.in_case(p>10, range(2, p), "unique checking on %s" % p, announce_every=11.23):
                            if j % p == 0:
                                break
                        else:
                            sum_high += n // i

    return n  - sum_low - sum_all + sum_high

#@validation
def validate():
    assert sum_floor_series(9, 3) == 23, sum_floor_series(9, 3)
    assert sum_floor_series(36, 6) == 140, sum_floor_series(36, 6)
    for t in range(50, 10):
        a = sum([(t*t)//k for k in range(1, t*t+1)])
        b = sum_floor_series(t * t, t)
        assert b == a, (t, b, a)
    
    primes = prime_sieve(500)
    assert is_root_smooth(8, primes)
    assert not is_root_smooth(6, primes)
    assert is_root_smooth(12, primes)
    assert not is_root_smooth(2*3*7, primes)
    assert brute_force(100, primes) == 29, brute_force(100, primes)
    #assert solve(100) == 29, solve(100)
    for _, i in Progress(range(5, 73)):
        bf =  brute_force(i*i, primes)
        sol = solve(i*i)
        assert bf == sol, (bf, sol) 


@solution
def solve_all():
    lim = 10 ** 10
    return solve(lim)
    