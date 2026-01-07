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
        