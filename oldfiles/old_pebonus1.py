from project_euler import Measure, Progress, validation, solution
import numpy as np
from scipy.special import comb
import json
with Measure("import pyplot"):
    import matplotlib.pyplot as plt

N = 10 ** 12
MOD = 7
SIZE = (975//5, 585//5)

def binom(a, b, mod):
    if a < 0 or b < 0:
        return 0
    if a < b:
        return 0

    res = 1
    while a > 0 or b > 0:
        res *= comb(a % mod, b % mod, exact=True)
        res %= mod
        if res == 0:
            return 0
        a //= mod
        b //= mod
        
    return res

def paths(n, x, y, mod):
    x = abs(x)
    y = abs(y)
    if (n+x+y) % 2 != 0:
        return 0
    return (binom(n, (n-x-y)//2, mod) * binom(n, (n+x-y)//2, mod)) % mod 


def non_divisible_binomials(n, p):
    """
    for integer n and prime p,
    this function returns all k such that:
    p does NOT divide (n choose k)

    (The function relies on Lucas's theorm)
    """
    if n == 0:
        return [0]
    inner = non_divisible_binomials(n // p, p)
    res = []
    for i in range((n % p) + 1):
        for x in inner:
            res.append(x*p + i)

    return res

@validation
def validate():
    with Measure("sanity"):
        assert paths(10**12, 356446145698, 0, 7) != 0
        q = paths(10**12, 10**12-28, 0, 7)
        assert q != 0
        print(q)
    bp = non_divisible_binomials(N, MOD)
    bp = [t for t in bp if t <= N//2]
    bp.sort()
    print(bp[:100] + bp[-100:])

@solution
def solve():
    w = SIZE[0]
    for _, x in Progress(range(10001)):
        for i in range(10001):
            pres = paths(N,x+i*w, 0, MOD)
            if pres != 0:
                print(f"paths({N}, {x+i*w}, 0) mod {MOD} = {pres}")
    print(paths(N, 50, 0, mod=MOD))
    return 2001
