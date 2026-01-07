import project_euler as pe
import itertools

LIM = 10 ** 4

def is_5_smooth(n, primes=[2, 3, 5]):
    for p in primes:
        while n % p == 0:
            n //= p
    return n == 1

def overprime_sieve(num, measure=None):
    prime = [True for i in range(num + 1)]
    if measure:
        print(measure)
    p = 2
    while p  <= num:
        if prime[p] == True:
            for i in range(p * p, num + 1, p):
                prime[i] = False
            if not is_5_smooth(p-1):
                prime[p] = False
        p += 1

    if measure:
        print(measure)
    return [i for i in range(2, num + 1) if prime[i]]

class Blocks:
    def __init__(self, lst):
        self.lst = lst
    def __iter__(self):
        self._c = 0
        return self
    def __next__(self):
        #import pdb; pdb.set_trace()
        c = self._c
        s = 1
        for p in self.lst:
            if c & 1 == 1:
                s *= p
            c >>= 1

        self._c += 1
        return s

def mul(lst):
    s = 1
    for t in lst:
        s *= t
    return s

def validation():
    assert is_5_smooth(2)
    assert is_5_smooth(3)
    assert is_5_smooth(5)
    assert is_5_smooth(15)
    assert is_5_smooth(25)
    assert is_5_smooth(256)
    assert is_5_smooth(256*81*125)
    assert not is_5_smooth(14)
    assert not is_5_smooth(14*15)
    assert not is_5_smooth(15*11*101)


def solve():
    print("sieving...")
    with pe.Measure("sieving") as m:
        overprimes = overprime_sieve(LIM, m)

    combs = [itertools.combinations(overprimes, r) for r in range(len(overprimes)+1)]
    sets = itertools.chain.from_iterable(combs)
    
    smooths = []
    print("LEN:")
    print("LEN:", len(overprimes))
    for p in sets:
        m = mul(p)
        if m <= LIM:
            print(m)
            smooths.append(m)
    
    print(smooths)

validation()

blocks = Blocks([2, 3])

print("FOO")
t = iter(blocks)
for x in t:
    print(x)