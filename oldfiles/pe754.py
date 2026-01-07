from math import gcd
from itertools import chain, combinations

def H(d, n):
    assert n % d == 0, (d, n)
    c = n // d
    return (d ** c)*math.factorial(c)



def brute_g(n):
    mul = 1
    for i in range(1, n+1):
        if gcd(n, i) == 1:
            mul *= i
    return mul

assert brute_g(10) == 189, brute_g(10)

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def mul():
    pass

def g_non_square(fn):
    blocks = powerset(fn)
    g = 1
    for 