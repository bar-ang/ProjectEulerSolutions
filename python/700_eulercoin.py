import project_euler as pe
import time

A = 1504170715041707
M = 4503599627370517


def next(a, x, m):
    #TODO: can be made more efficient
    return x + 1


def force(a, m):
    min = a
    sum = a
    for i in range(1, m):
        if (a * i) % m < min:
            min = (a * i) % m
            sum += (a * i) % m

    return sum


def dual(a, m):
    z = pow(a, -1, m)
    min = a + 1
    dual_min = z + 1
    sum = 0
    x = 1
    y = 1
    while (x <  (z * y) % m) and (y <  (a * x) % m):
        if (a * x) % m < min:
            min = (a * x) % m
            sum += (a * x) % m
        
        if (z * y) % m < dual_min:
            dual_min = (z * y) % m
            sum += (y) % m
        x = next(a, x, m)
        y = next(z, y, m)

    return sum

@pe.validation
def validation():
    print("validating...")

    def checker(a, m):
        d = dual(a, m)
        f = force(a, m)
        assert d == f, (a, m, d, f)

    def multi_checker(m):
        for i in range(2, m):
            checker(i, m)
    
    assert force(7, 10) == 12
    checker(7, 11)
    checker(5, 23)
    checker(13, 23)
    checker(11, 23)
    checker(53, 101)
    multi_checker(1)
    multi_checker(23)
    multi_checker(53)
    multi_checker(101)
    multi_checker(157)
    multi_checker(1201)
    print("OK")


@pe.solution
def solve():
    return dual(A, M)
