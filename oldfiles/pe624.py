from project_euler import Progress, Measure, solution, validation
import numpy as np
from scipy.stats import binom, geom

import numpy as np


# ------- functions used for reasarch (not used for solution) ------

def fib(n):
    if n <= 1:
        return n

    matrix = np.array([[1, 1], [1, 0]], dtype=object)
    result_matrix = np.linalg.matrix_power(matrix, n - 1)
    return result_matrix[0, 0]

def lucas(n):
    if n == 0:
        return 2
    if n == 1:
        return 1
    return fib(n+1)+fib(n-1)

def P(n):
    num = (2 ** n)*fib(n-1) - (-1)**n
    denom = (4 ** n) - (2**n)*lucas(n) + (-1)**n

    d = np.gcd(num, denom)
    num //= d
    denom //= d
    return num, denom

# ------- functions that are used for solving ------

SHADOW = {}
def pisano_period(m):
    if m in SHADOW:
        return SHADOW[m]
    a, b = 0, 1
    for n in range(0, m * m):
        a, b = b, (a + b) % m
        if a == 0 and b == 1:
            SHADOW[m] = n + 1
            return n + 1
    assert False

def fib_mod(n, m):
    return fib(n % pisano_period(m)) % m

def lucas_mod(n, m):
    return (fib_mod(n+1, m) + fib_mod(n-1, m)) % m

def P_mod(n, m):
    dir = -1 if n % 2 == 1 else 1
    num = (pow(2, n , m) * fib_mod(n-1, m) - dir) % m
    denom = (pow(4, n , m) - pow(2, n , m)*lucas_mod(n, m) + dir) % m
    return num, denom

def frac_str(a, b):
    return "%s/%s" % (a, b)

def Q(a, b, p):
    return (a * pow(b, -1, p)) % p

def solve(n, m):
    a, b = P_mod(n, m)
    return (a * pow(b, -1, m)) % m

@validation
def validate():
    def test_generalize_fibonnacci(s0, s1, f, reps):
        assert f(0) == s0
        assert f(1) == s1
        for i in range(reps):
            s1, s0 = s1+s0, s1
            assert s1 == f(i+2)
    test_generalize_fibonnacci(0, 1, fib, 100)
    test_generalize_fibonnacci(2, 1, lucas, 100)

    assert solve(2, 109) == 66, solve(2, 109)
    assert solve(3, 109) == 46, solve(3, 109)

@solution
def solve_all():
    mod = 10 ** 9 + 9
    n = 10 ** 18
    return solve(n, mod)
