import numpy as np
from project_euler import Measure, ShowProgress
from functools import partial
from common.primes import prime_sieve, Factorize
from common.factorization import run_for_factors
from math import gcd, sqrt
from itertools import product as cartesian_prod


LIM = 3*10**4
A = np.array([[1, 7], [1, 1]])
with Measure("prime sieving"):
    PRIMES = prime_sieve(LIM + 10)
    LEGENDRE = {p: pow(7, (p-1)//2, p) for p in PRIMES}

PROG = dict(bar_len=100, announce_every=2.31)

EPSILON = 2 ** 5
A_EPSILON = np.linalg.matrix_power(A, EPSILON)
A_POWERS = {
    i: np.linalg.matrix_power(A, i) for i in range(1, 2 ** 5)
}
def ring_power(mat, pow, ring):
    if pow in A_POWERS:
        return np.remainder(A_POWERS[pow], ring)
    def ring_power_aux(mat, pow, ring):
        if pow == 1:
            return mat
        if pow == 0:
            return np.identity(2)
        
        res = mat
        c = 1
        while 2*c < pow:
            res = np.remainder(np.matmul(res, res), ring)
            c *= 2
    
        rem = ring_power_aux(mat, pow-c, ring)
        t = np.remainder(np.matmul(res, rem), ring)
        return t
    pow2 = pow // EPSILON
    pow2_rem = pow % EPSILON

    mat2 = np.remainder(A_EPSILON, ring)
    mat2_rem = np.remainder(np.linalg.matrix_power(mat, pow2_rem), ring)

    res = ring_power_aux(mat2, pow2, ring)
    return np.remainder(np.matmul(res, mat2_rem), ring)

def combine_divisors(*divs_lists):
    def mult(lst):
        s = 1
        for i in lst:
            s *= i
        return s
    cart = cartesian_prod(*divs_lists)
    res = []
    for tup in cart:
        m = mult(tup)
        if m not in res:
            res.append(m)
    return res

def find_divisors_single(n):
    res = []
    for k in range(1, int(sqrt(n))+1):
        if n % k == 0:
            res.append(k)
            if k * k != n:
                res.append(n // k)
    return res

assert set(find_divisors_single(6)) == set([1, 2, 3, 6]), find_divisors_single(6)
assert set(find_divisors_single(25)) == set([1, 5, 25]),find_divisors_single(25)
assert set(find_divisors_single(36)) == set([1, 2, 3, 4, 6, 9, 12, 18, 36]),find_divisors_single(36)

def find_divisors(*n):
    divs = [find_divisors_single(t) for t in n]
    return combine_divisors(*divs)

assert set(find_divisors(6, 7)) == set([1, 2, 3, 6, 7, 14, 21, 42]), find_divisors(6, 7)
assert set(find_divisors(6, 25)) == set([1, 2, 3, 6, 5, 10, 15, 30, 25, 50, 75, 150]), find_divisors(6, 25)

def solve_single(a, divs, ring):
    assert ring > 1
    if gcd(ring, ring-6) > 1:
        return 0
    #with Measure("sorting %s" % divs, print_threshold_sec=0.06):
    #    divs.sort()

    min_div = max(divs)
    for div in divs:
        if div > min_div:
            continue
        m = ring_power(a, div, ring)
        if np.all(np.equal(m, np.identity(2))):
            min_div = div
            #break
    
    return min_div

def psi(p, k):
    res = []
    if k > 1:
        res.append(p**(k-1))
    if p > 2:
        res.append(p-1)
    if LEGENDRE[p] != 1:
        res.append(p+1)
    return res

def solve_for_primes(lim):
    g = [0] * (lim+1)
    for _, p in ShowProgress(PRIMES, "solving for primes", **PROG):
        k = 1
        while p ** k <= lim:
            if gcd(p**k, p **k - 6) > 1:
                g[p ** k] = 0
                k += 1
                continue
            if p == 7:
               g[p ** k] = p ** k
               k += 1
               continue
            if k > 1:
                psim = psi(p, k)
                psit = 1
                for jj in psim:
                    psit *= jj
                g[p ** k] = psit
                k += 1
                continue

            psim = psi(p, k)
            if LEGENDRE[p]:
                with Measure("find_divisors(%s)" % psim, print_threshold_sec=0.2):
                    divs = find_divisors(*psim)
                with Measure("solve_single(divs, %s^%s)" % (p,k), print_threshold_sec=0.870):
                    g[p ** k] = solve_single(A, divs, p ** k)
                #psit = 1
                #for jj in psim:
                #    psit *= jj
                #if psit == g[p]:
                #    print("%s(%s?): g=%s, psi=%s [%s] --> %s" % (p, pow(49, (p-1)//2, p), g[p], psit, psim, psit/g[p]))
            else:
                psit = 1
                for jj in psim:
                    psit *= jj
                g[p ** k] = psit
            k += 1
    return g

def solve_g(lim, g):
    for i, (_, n, factors) in ShowProgress(Factorize(lim, PRIMES), "combining", **PROG):
        if n < 3:
            continue
        if gcd(n, n - 6) > 1:
            continue
        mult = 1
        for p, k in factors:
            mult *= g[p ** k]
        divs = find_divisors(mult)
        with Measure("solve_single[when integrating](divs, %s)" % (n), print_threshold_sec=0.5):
            g[n] = solve_single(A, divs, n)
    return sum(g)

def validation():
    with Measure("---Test Solve Single 1---"):
        s1 = solve_single(A, [1, 2, 3, 4, 6, 8, 12, 24], 5)
        assert s1 == 12, s1
    with Measure("---Test A---"):
        g = solve_for_primes(100)
        g[5] = 12
        s1 = solve_g(100, g)
        assert s1 == 28891, s1 
    with Measure("---Test B---"):
        g = solve_for_primes(1000)
        s2 = solve_g(1000, g)
        assert s2 == 13131583, s2

validation()



def solve():
    g = solve_for_primes(LIM)
    return solve_g(LIM, g)

with Measure("Solving"):
    res = solve()
print("RESULT: %s" % res)