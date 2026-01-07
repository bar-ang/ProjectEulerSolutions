from project_euler import Measure, Progress, validation, solution
from common.primes import prime_sieve
import numpy as np
from sympy import divisors
from sympy.ntheory import factorint


LIM = 10 ** 6

def brute_force(x):
    if x % 2 == 0 or x % 3 == 0:
        return 0
    if x == 5:
        return 12
    if x == 7:
        return 7

    a = np.array([[1, 7], [1, 1]])
    m = a
    c = 1
    while not np.array_equal(m, np.eye(2)):
        m = np.matmul(m, a)
        m %= x
        c += 1
        #print(m)
        assert c < x ** 2, f"failed for {x}"
    return c
    
def mat_power_mod(a, n, p):
    t = 0
    res = np.eye(2)
    while n > 0:
        k = 1
        m = a
        while 2*k <= n:
            m = np.matmul(m, m) % p
            k *= 2
        res = np.matmul(res, m) % p
        n -= k

    return res

def solve_for_prime(p):
    if p == 2 or p == 3:
        return 0
    if p == 5:
        return 12
    if p == 7:
        return 7

    a = np.array([[1, 7], [1, 1]])
    if pow(7, (p-1)//2, p) != 1:
        candids = divisors(p**2-1)
    else:
        candids = divisors(p-1)
    known = (0, np.eye(2))
    for i, c in enumerate(candids):
        if pow(-6, c, p) != 1:
            continue
        k = mat_power_mod(a, c - known[0], p)
        m = np.matmul(known[1], k) % p #np.linalg.matrix_power(a, c) % p
        known = (c, m)
        if np.array_equal(m, np.eye(2)):
            return c

    assert False, f"failed for prime {p}"
    return None

def solve_for_prime_power(p, k, s):
    if k <= 1 or s == 0:
        return s
    return s * (p ** (k-1))

def orderof(p, n):
    t = 0
    while n %  (p ** (t+1)) == 0:
        t += 1
    return t

def solve_for_all(primes, lim):
    res = [1] * (lim+1)
    res[0] = 0
    res[1] = 0
    res[2] = 0
    res[3] = 0

    for _, p in Progress(primes):
        rng = range(2*p, lim+1, p)
        if p < 400:
            rng = Progress(rng, f"filling prime {p}")
        else:
            rng = enumerate(rng)

        if p <= lim:
            res[p] = solve_for_prime(p)
        for _, n in rng:
            if p == 2 or p == 3:
                res[n] = 0
                continue
            k = orderof(p, n)
            res[n] = np.lcm(res[n], solve_for_prime_power(p, k, res[p]))
    return res
    
def solve(n):
    primes = prime_sieve(n+5)
    return sum(solve_for_all(primes, n))
    
@validation
def validate():
    assert orderof(2, 1024) == 10, orderof(2, 1024)
    assert orderof(2, 1025) == 0, orderof(2, 1025)
    assert orderof(3, 3**4 *  11) == 4
    assert orderof(5, 3 ** 4 * 5 * 11 * 23 * 23) == 1
    assert orderof(23, 3 ** 4 * 5 * 11 * 23 * 23) == 2

    assert solve_for_prime(5) == 12

    j =  mat_power_mod(np.array([[4, 0], [0, 7]]), 6, 17)
    assert np.array_equal(j, np.array([[16,0], [0, 9]])), j

    s = [brute_force(k) for _, k in Progress(range(2, 101))]
    assert sum(s) == 28891, sum(s)

    with Measure("sieving"):
        primes = prime_sieve(210)
    
    for _, i in Progress([p for p in primes if p >= 4], "Vaidting prime powers"):
        assert solve_for_prime(i) == brute_force(i), (i, solve_for_prime(i), brute_force(i))
        for k in range(1, 15):
            if i ** k > 2100:
                continue
            s = solve_for_prime(i)
            assert solve_for_prime_power(i, k, s) == brute_force(i ** k), (i, k, solve_for_prime(i), solve_for_prime_power(i, k, s), brute_force(i ** k))

    lim = 320
    a = solve_for_all(prime_sieve(320), lim)
    assert len(a) == lim+1
    for _, i in Progress(range(2, lim+1), "Moment of truth..."):
        assert a[i] == brute_force(i), (i, a[i], brute_force(i))

    assert solve(100) == 28891
    assert solve(1000) == 13131583
        
@solution
def solve_all():
    return solve(LIM)
