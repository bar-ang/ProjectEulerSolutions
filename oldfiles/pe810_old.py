from project_euler import Measure, Progress, validation, solution
from math import log, ceil
from common.primes import prime_sieve

def num_bits(n):
    return int(log(n, 2)) + 1


def _xor_prod(a, b):
    return xor_prod_aux(a, b, m=ceil(log(a, 2)))


def xor_prod_aux(a, b, m):

    def split(a, m):
        return a >> m, a & ((1 << m) - 1)

    if a == 0 or b == 0:
        return 0
    if a == 1:
        return b
    if b == 1:
        return a

    a_1, a_0 = split(a, m)
    b_1, b_0 = split(b, m)
    n = max(m // 2, 1)

    c_2 = xor_prod_aux(a_1, b_1, n)
    c_1_0 = xor_prod_aux(a_1, b_0, n)
    c_1_1 = xor_prod_aux(a_0, b_1, n)
    c_0 = xor_prod_aux(a_0, b_0, n)

    c_1 = c_1_0 ^ c_1_1
    res = (c_2 << (2 * m)) ^ (c_1 << m) ^ c_0

    return res

POW_OF_2 = [2 ** i for i in range(64)]

def xor_prod(a, b):
    c = 1
    if a in POW_OF_2 or b in POW_OF_2:
        return a * b
    if b == 3:
        return a ^ (a << 1)
    if a == 3:
        return b ^ (b << 1)
    res = 0
    while a > 0:
        if a & 1 == 1:
            res ^= b
        a >>= 1
        b <<= 1
    return res * c

def map_in(x):
    assert x % 2 == 1, x
    return x // 2
def map_out(x):
    return x * 2 + 1

def sieve_xor_primes(lim, catch=None):
    primes = [True] * ((lim+1)//2)
    primes[map_in(1)] = False
    #primes[map_in(3)] = False
    count = 1
    lim_bits = num_bits(lim)
    for _, p in Progress(range(3, lim, 2), announce_every=8.274, announce_every_seconds=10):
        p_bits = lim_bits - num_bits(p)
        if primes[map_in(p)]:
            count += 1
            if catch and count == catch:
                return primes[:map_in(p)+1], count, p
            i = p
            sub_lim = min(lim, 1 << (p_bits+1))
            if 5*sub_lim >= lim:
                rng = Progress(range(p, sub_lim, 2), "SUB", announce_every_seconds=4, announce_every=110)
            else:
                rng = enumerate(range(p, sub_lim, 2))
            for _, i in rng:
                q = xor_prod(i, p)
                if q <= lim:
                    primes[map_in(q)] = False
                j = i << 2
                while j <= lim:
                    k = q ^ j
                    if k % 2 == 1 and k <= lim:
                        primes[map_in(k)] = False
                    j <<= 1
    return primes, count, None

def extract(primes):
    return [2] + [map_out(i) for i, p in enumerate(primes) if p]

@validation
def validate():
    assert xor_prod(7, 3) == 9, xor_prod(7, 3)
    assert xor_prod(3, 3) == 5, xor_prod(3, 3)
    assert num_bits(7) == 3
    assert num_bits(9) == 4
    assert num_bits(2 ** 5) == 6
    #assert xor_square(3) == 5, xor_square(3)
    res =  [2, 3, 7, 11, 13, 19, 25, 31, 37, 41, 47, 55, 59, 61, 67, 73, 87, 91, 97, 103]
    primes, count, _ = sieve_xor_primes(105)
    assert extract(primes) == res, extract(primes)
    assert count == len(res), (count, len(res))

    res =  [2, 3, 7, 11, 13, 19, 25, 31, 37, 41, 47, 55, 59, 61, 67, 73, 87, 91, 97, 103, 109, 115, 117, 131, 137, 143, 145, 157, 167, 171, 185, 191, 193, 203, 211, 213, 229, 239, 241, 247, 253, 283, 285, 299, 301, 313, 319, 333, 351, 355, 357, 361, 369, 375]
    primes, count, catch = sieve_xor_primes(376)
    assert extract(primes) == res, extract(primes)
    assert count == len(res), (count, len(res))

    res =  [2, 3, 7, 11, 13, 19, 25, 31, 37, 41]
    primes, count, catch = sieve_xor_primes(376, catch=10)
    assert extract(primes) == res, extract(primes)
    assert count == len(res), (count, len(res))
    assert catch == 41, catch

    res =  [2, 3, 7, 11, 13, 19, 25, 31, 37, 41, 47, 55, 59, 61, 67, 73, 87, 91, 97, 103, 109, 115, 117, 131, 137, 143]
    primes, count, catch = sieve_xor_primes(376, catch=26)
    assert extract(primes) == res, extract(primes)
    assert count == len(res), (count, len(res))
    assert catch == 143, catch

#LIM = 2 * 10 ** 5
LIM = 5 * 10 ** 6


@solution
def solve_all():
    c = 2 ** 26
    print("will sieve xor primes until: %s" % c)
    primes, count, catched = sieve_xor_primes(c, catch=LIM)
    print("done sieveing!")
    assert count >= LIM, "only %s primes were sieved :(" % len(primes)
    assert catched is not None
    return catched