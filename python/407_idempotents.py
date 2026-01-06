from project_euler import Measure, Progress, validation, solution
from sympy import sieve
from collections import Counter
from itertools import chain, combinations


def factorize_by_sieveing(num, return_raw=False):
    '''
    this will return a list map in which prime[k] holds the least divisor of k
    '''
    prime = [i for i in range(num + 1)]
    p = 2
    while p * p <= num:
        if prime[p] == p:
            for i in range(p * p, num + 1, p):
                if prime[i] > p:
                    prime[i] = p
        p += 1

    return prime

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class Factorize:
    def __init__(self, until):
        self._until = until
        self._raw = factorize_by_sieveing(until)

    def factorize(self, num):
        res = []
        while num > 1:
            res.append(self._raw[num])
            num //= self._raw[num]
        return Counter(res)
    
    def block_divisors(self, num):
        '''
        d is a block-divisor of n if d devides n and gcd(d, n/d) = 1
        '''
        fact = self.factorize(num)
        power_primes = [p ** k for p, k in fact.items()]
        res = []
        for r in range(len(power_primes)+1):
            for comb in combinations(power_primes, r):
                m = 1
                for b in comb:   
                    m *= b
                res.append(m)
        return res
        
def prime_sieve(n):
    return list(sieve.primerange(1, n))

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
