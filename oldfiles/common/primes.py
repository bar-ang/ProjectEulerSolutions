from collections import Counter
from common.common import BoundedQueue

def prime_sieve(num, measure=None, return_raw=False):
    prime = [True for i in range(num + 1)]
    if measure:
        print(measure)
    p = 2
    while p * p <= num:
        if prime[p] == True:
            for i in range(p * p, num + 1, p):
                prime[i] = False
        p += 1

    if measure:
        print(measure)

    if not return_raw:
        return [i for i in range(2, num + 1) if prime[i]]
    else:
        return prime

class Primes:
    def __init__(self, lim):
        self._lim = lim
        self._raw = prime_sieve(lim, return_raw=True)

    def __iter__(self):
        self._i = 2
        return self

    def __next__(self):
        if self._i >= self._lim:
            raise StopIteration
        x = self._i
        self._i += 1
        while self._i < self._lim and not self._raw[self._i]:
            self._i += 1
        return x
    
    def __len__(self):
        return len([p for p in range(self._lim) if self._raw[p]])

class Factorize:
    def __init__(self, limit, primes):
        self._limit = limit
        self._primes = primes
        self._q = BoundedQueue(limit//2)
    
    def __iter__(self):
        self._q.clear()
        self._q.insert(dict(v=1, fact=(), ref=0))
        self.count = 0
        return self

    @property
    def current(self):
        return self._q.observe()

    def next_fact(self, fact, p):
        if p not in [q for q, _ in fact]:
            return fact + ((p, 1),)
        return tuple((q, k+(1 if q==p else 0)) for q, k in fact)

    def __len__(self):
        return self._limit
    
    def __next__(self, sort=False):
        assert not sort, "sorting is not implemented yet"
        #if sort:
        #    self._q.sort(key=lambda e:e["v"])
        if len(self._q) == 0:
            raise StopIteration
        dd = self._q.extract()
        d = dd["v"]
        fact = dd["fact"]
        ref = dd["ref"]
        for i in range(ref, len(self._primes)):
            p = self._primes[i]
            if d * p > self._limit:
                break
            f = self.next_fact(fact, p)
            self._q.insert(dict(v=d*p, fact=f, ref=i))
        self.count += 1
        return d, fact

