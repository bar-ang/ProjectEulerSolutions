from project_euler import validation, solution, Testing, Progress, Measure
from math import sqrt, isqrt

def reverse_triangle(k):
    v = 8 * k + 1
    r = isqrt(v)

    if r * r != v:
        return None

    return (r-1)//2


def triangle(m):
    return m * (m+1) // 2

def get_next_triangle(t):
    counter = 1
    pos = 1
    #import pdb; pdb.set_trace()
    rev = None
    while not rev:
        res = triangle(counter) + t*counter
        rev = reverse_triangle(res)
        counter += 1
        pos += 1
    return pos, (counter-1)+t, counter-1


def prod_series_brute_force(size):
    t = 3
    counter = 1
    series = []

    for i in range(size):
        series.append(t)
        t += counter
        if reverse_triangle(t) is not None:
            counter = 1
        else:
            counter += 1

    return series

@validation
def validate():
    ser = prod_series_brute_force(500)
    print("\n".join([f"{v}=T{reverse_triangle(v) or "~"}" for v in ser])) 

    t = 3
    pos = 0
    diff = 0
    for i in range(70):
        print(f"{i+1}.\ta{pos} =\tT{t} (+T{diff}) =\t{triangle(t)} (+{triangle(diff)})")
        m, t, diff = get_next_triangle(t)
        pos += m

