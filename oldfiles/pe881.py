from project_euler import Measure, Progress, validation, solution
from common.primes import prime_sieve

class BasicNumber:
    def __init__(self, primes, *exp):
        self.exp = exp
        self.primes = primes
        assert len(exp) <= len(primes)

    def get(self):
        res = 1
        for i, e in enumerate(self.exp):
            res *= self.primes[i] ** e
        return res
    

def h_naive(r, k, primes):
    pass

def g_naive(n):
    pass

@validation
def validate():
    primes = prime_sieve(10 ** 5)
    h = h_naive(BasicNumber(primes, 1, 1, 1), 3, primes)