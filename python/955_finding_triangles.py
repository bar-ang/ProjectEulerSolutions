from project_euler import validation, solution, Testing, Progress, Measure
from sympy import divisors
from math import sqrt, isqrt


def triangle(m):
    return m * (m+1) // 2

def find_next_triangle(b):
    a = -1
    n = -1
    optv = -1
    divs = divisors(8*triangle(b))
    divs = [d for d in divs if d < 2*b]
    for v in divs:
        if 8*triangle(b) <= v*(v+2):
            break
        if (8*triangle(b)) % v != 0:
            continue

        if (8*triangle(b) - v*(v+2)) % (4*v) != 0:
            continue
        if (8*triangle(b) + v*(v-2)) % (4*v) != 0:
            continue

        _a = (8*triangle(b) - v*(v+2))//(4*v)
        if a < 0 or _a < a:
            a = _a
            n = (8*triangle(b) + v*(v-2))//(4*v)
            optv = v
    return a, n

def solve_single(lim):
    tri_idx = 3
    n_idx = 2
    for _, i in Progress(range(lim-2)):
        a, tri_idx = find_next_triangle(tri_idx)
        n_idx += a

    return n_idx

@validation
def validate():
    Testing.equals(2, solve_single, 2)
    Testing.equals(7, solve_single, 3)
    Testing.equals(12, solve_single, 4)
    Testing.equals(2964, solve_single, 10)


@solution
def solve():
    return solve_single(70)
