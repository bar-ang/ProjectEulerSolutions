from project_euler import Measure, Progress, validation, solution
from math import log, ceil, sqrt
from sympy import sieve

LIM = 5 * 10 ** 6

def prime_sieve(n):
    return list(sieve.primerange(1, n))

def xor_prod(a, b):
    res = 0;
    dig = 0;
    while b:
        if b & 1:
            res ^= a << dig
        dig += 1
        b >>= 1

    return res

def num_bits(n):
    c = 0
    while n:
        n >>= 1
        c += 1
    return c

def xor_modulo(a, b):
    rem = a
    while rem >= b:
        q = rem
        t = b
        while (q ^ b) > b:
            q >>= 1
            t <<= 1
        rem ^= t
    return rem;

def is_prime(n, primes):
    m = int(sqrt(num_bits(n))) + 1
    for p in primes:
        if p >= ((2 << m) + 1):
            break
        r = xor_modulo(n, p)
        if r == 0:
            return False
    return True

def skips(n):
    # return 4c + 2k + 1, where k == xor of all digits of c.
    xor_digs = 0
    d = n
    while d > 0:
        xor_digs ^= (d & 1)
        d >>= 1

    return (n << 2) ^ (xor_digs << 1) ^ 1

def should_print(found):
    if found >= LIM-10:
        return True
    if found <= 30:
        return True
    if found <= 400 and found % 43 == 0:
        return True
    if found <= 5000 and found % 237 == 0:
        return True
    if found <= 90000 and found % 60781 == 0:
        return True
    if found % 340781 == 0:
        return True

    return False

def sieve_xor_primes(n):
    if n == 1:
        return 2
    if n == 2:
        return 3
    if n == 3:
        return 7
    found = 3;
    c = 2;
    primes = [2, 3, 7]
    while found < n:
        if is_prime(skips(c), primes):
            found += 1
            primes.append(skips(c))
            if should_print(found):
                print("Found %sth prime: %s" % (found, skips(c)));
        c += 1;

    return primes

@validation
def validate():
    assert xor_prod(7, 3) == 9, xor_prod(7, 3)
    assert xor_prod(3, 3) == 5, xor_prod(3, 3)
    assert num_bits(7) == 3
    assert num_bits(9) == 4
    assert num_bits(2 ** 5) == 6

    res =  [2, 3, 7, 11, 13, 19, 25, 31, 37, 41, 47, 55, 59, 61, 67, 73, 87, 91, 97, 103, 109, 115, 117]
    got = sieve_xor_primes(len(res))
    assert res == got, got

    t = sieve_xor_primes(10)
    assert t[-1] == 41


@solution
def solve_all():
    m = sieve_xor_primes(LIM)
    return m[-1]
