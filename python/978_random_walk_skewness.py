from project_euler import validation, solution, Testing
from math import sqrt

def extended_fibonnaci(n, a, b):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1

    prev2 = 0
    prev1 = 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, a * prev1 + b * prev2

    return prev1

def skew(t):
    g_t = extended_fibonnaci(t, 1, 3)
    f_t = extended_fibonnaci(t, 1, 1)

    sq_f_t = (f_t-1)**(1.5)

    return (g_t-3*f_t+2)/sq_f_t


@validation
def validate():
    Testing.equals(0, extended_fibonnaci, 0, 1, 1)
    Testing.equals(1, extended_fibonnaci, 1, 1, 1)
    Testing.equals(1, extended_fibonnaci, 2, 1, 1)
    Testing.equals(2, extended_fibonnaci, 3, 1, 1)
    Testing.equals(55, extended_fibonnaci, 10, 1, 1)
    Testing.equals(61, extended_fibonnaci, 5, 2, 3)
    Testing.equals(64, extended_fibonnaci, 4, 4, 0)

    Testing.equals(4181, extended_fibonnaci, 19, 1, 1)
    Testing.equals(2117473, extended_fibonnaci, 19, 1, 3)
    Testing.equals(6765, extended_fibonnaci, 20, 1, 1)
    Testing.equals(4875913, extended_fibonnaci, 20, 1, 3)

    print(extended_fibonnaci(5, 1, 1))
    print(extended_fibonnaci(5, 1, 3))
    for i in range(3, 10):
        print(i, skew(i))

    Testing.equals(0.75, skew, 5)
    Testing.almost_equals(2.50997097, skew, precision=8, t=10)

@solution
def solution():
    return round(skew(50), 8)
