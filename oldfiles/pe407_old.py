from project_euler import Measure, Progress, validation, solution
from common.primes import prime_sieve, Factorize

def chi(d, n):
    assert n % d == 0
    return d * pow(d, -1, n // d)

def brute_force(lim):
    idems = {}
    for i in range(2, lim+1):
        idems[i] = [1]
        for j in range(2, i):
            if j * (j-1) % i == 0:
                idems[i].append(j)
    return idems

def idempotents(num, facts):
    if num == 1:
        return [0]
    idems = [1]
    for p, k in facts:
        b = p ** k
        t = b * pow(b, -1, num // b)
        if t > 0:
            idems.append(t)
    return idems
    
def solve(lim):
    with Measure("sieveing"):
        primes = prime_sieve(lim+10)
    facts = Factorize(lim, primes)
    res = 0
    for _, (n,f) in Progress(facts, announce_every=1):
        ids = idempotents(n, f)
        res += max(ids)
    return res

#@validation
def validate():
    assert idempotents(2, ((2, 1),)) == [1], idempotents(2, ((2, 1),))
    assert set(idempotents(10, ((2, 1), (5, 1)))) == set([1, 5, 6]), idempotents(10, ((2, 1), (5, 1)))
    for i in range(4, 300):
        idems =  brute_force(i)
        bf = sum([max(v) for v in idems.values()])
        assert solve(i) == bf, (i, solve(i), bf)

@solution
def solve_all():
    return solve(10 ** 7)