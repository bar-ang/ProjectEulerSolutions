from project_euler import Measure, validation, solution, Progress
from sympy import sieve
from math import sqrt

LIM = 10**12
MOD = 2 ** 32

print(LIM % MOD)
N_PRIMES = int(sqrt(LIM)) + 100

def prime_sieve(n):
    return list(sieve.primerange(1, n))

with Measure("prime sieving until %s" % N_PRIMES):
    PRIMES = prime_sieve(N_PRIMES)

def is_prime_bf(n):
    if n == 1:
        return False
    for p in PRIMES:
        if p >= n:
            break
        if n % p == 0:
            return False
    return True

def smooth5_primes(lim):
    def mult(n2, n3, n5):
        return (2 ** n2) * (3 ** n3) * (5 ** n5)
    res = []
    n2 = 0
    while mult(n2, 0, 0) <= lim:
        n3 = 0 
        while mult(n2, n3, 0) <= lim:
            n5 = 0
            while mult(n2, n3, n5) <= lim:
                if is_prime_bf(mult(n2, n3, n5)+1):
                    res.append(mult(n2, n3, n5)+1)
                n5 += 1
            n3 += 1
        n2 += 1
    return res

def multiply_by_5smooth(r, lim):
    def mult(n2, n3, n5):
        return (2 ** n2) * (3 ** n3) * (5 ** n5)
    res = 0
    n2 = 0
    while r * mult(n2, 0, 0) <= lim:
        n3 = 0 
        while r * mult(n2, n3, 0) <= lim:
            n5 = 0
            while r * mult(n2, n3, n5) <= lim:
                res += r * mult(n2, n3, n5)
                n5 += 1
            n3 += 1
        n2 += 1
    return res

def multiply_all_by_5smooth(lst, lim):
    res = 0
    for i, r in enumerate(lst):
        if i % int(len(lst)*0.085) == 0:
            print("%s/%s (%s%%)" % (i, len(lst), round(i * 100 / len(lst), 2)))
        with Measure("mult %s (lim: %s)" % (r, lim), print_threshold_sec=0.1):
            res += multiply_by_5smooth(r, lim)

    return res



def iterate_square_free(lim, primes, i=None):
    if i is None:
        i = len(primes)
    if i == 1:
        return [primes[0]]

    inner = iterate_square_free(lim, primes, i=i-1)
    inner.sort()
    p = primes[i-1]
    if p > lim:
        return inner
    y = []
    for t in inner:
        if  t * p > lim:
            break
        y.append(t * p)
    return inner + y + [p]
 
@validation
def validate():
    with Measure("filtering over-smooth primes"):
        OS_PRIMES = [p for p in smooth5_primes(100) if p > 5]
        print("5smooth primes:", len(OS_PRIMES))
    lst = iterate_square_free(100, OS_PRIMES) + [1]
    s = multiply_all_by_5smooth(lst, 100)
    assert s == 3728, s

def solve(lim):
    with Measure("filtering over-smooth primes"):
        OS_PRIMES = [p for p in smooth5_primes(LIM) if p > 5]
        print("5smooth primes:", len(OS_PRIMES))
    with Measure("iterate_square_free"):
        lst = iterate_square_free(lim, OS_PRIMES) + [1]
    with Measure("multiply_all_by_5smooth"):
        s = multiply_all_by_5smooth(lst, lim)
    return s


@solution
def solve_all():
    r = solve(LIM)
    print("RESULT (full): %s" % (r))
    return r % MOD
