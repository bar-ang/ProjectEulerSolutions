from project_euler import Measure, Progress, validation, solution
from common.primes import prime_sieve
from common.factorization import Factorize

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

def idempotents(num, blocks):
    if num == 1:
        return [0]
    idems = []
    for b in blocks:
        t = b * pow(b, -1, num // b)
        if t > 0:
            idems.append(t)
    return idems
    
def solve(lim, announce_every=2.76812):
    facts = Factorize(lim)
    res = 0
    for _, i in Progress(range(2, lim+1), announce_every=announce_every):
        ids = idempotents(i, facts.block_divisors(i))
        res += max(ids)
    return res

@validation
def validate():
    res = idempotents(2, (1, 2))
    assert res == [1], res
    res = idempotents(10, (1, 2, 5, 10))
    assert set(res) == set([1, 5, 6]), res
    for i in range(4, 200):
        idems =  brute_force(i)
        bf = sum([max(v) for v in idems.values()])
        assert solve(i, announce_every=101) == bf, (i, solve(i), bf)

@solution
def solve_all():
    return solve(10 ** 7)