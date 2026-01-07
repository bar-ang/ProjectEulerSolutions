from simplekv.fs import FilesystemStore
from project_euler import Measure
from common.primes import prime_sieve
import json

LIM = 10 ** 5 + 10 ** 4
with Measure("prime sieving"):
    PRIMES = prime_sieve(LIM + 100)

SHADOW = {}
def get_divisors_aux(n, visited):
    visited.append(n)
    res = [n]
    if n == 1:
        return res
    if n in SHADOW:
        primes = SHADOW[n]
        #print("SHADOWED: %s %s" % (primes, n))
        newly = False
    else:
        primes = PRIMES
        SHADOW[n] = []
        newly = True
    for p in primes:
        if p > n:
            break
        if n % p == 0:
            if newly:
                SHADOW[n].append(p)
            if n//p not in visited:
                res += get_divisors_aux(n // p, visited=visited)
    return res

def get_divisors(n):
    assert type(n) in [tuple, list], (n, type(n))
    visited = []
    res =  [1]
    for t in n:
        divs = get_divisors_aux(t, visited=visited)
        nres = []
        for div in divs:
            nres += [div * r for r in res]

        res += nres
    return res

store = FilesystemStore('./store')

PRINTS = int(LIM*0.065)
for i in range(2, LIM+1):
    new_entries = 0
    uni = str(u"k%s" % i)
    try:
        store.get(uni)
    except KeyError:
        new_entries += 1
        divs = get_divisors((i,))
        bs = bytes(json.dumps(divs), "utf-8")
        store.put(uni, bs)

    if i % PRINTS == 0:
        print("-- %s%% (%s new entries) --" % ((i * 100 / LIM),new_entries))

print("%s new entries were added." % new_entries)

