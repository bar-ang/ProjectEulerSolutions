from project_euler import Measure, Progress, validation, solution
from math import tanh, sqrt, ceil

def meet_threshold(func, threshold, begin=1):
    n = begin
    fn = func(n)
    while fn >= threshold:
        print(f"{func.__name__}({n}) = {round(fn, 5)} >= {threshold}")
        n += 1
        fn = func(n)
    print(f"{func.__name__}({n}) = {round(fn, 5)} < {threshold}")
    return n

def integrated(n):
    y = 1/float(1+2*n+2*sqrt(n))

    circ = sqrt((2-y) * y)

@validation
def validate():
    def func(n):
        return 1 / (sqrt(3*n))

    for r in range(5, 25):
        fr = meet_threshold(func, 1/float(r))
        t = ceil(float(r*r) / 3)
        if (r*r % 3 == 0):
            t += 1
        assert fr == t, (r, t , fr)
        
    p = 0.3646

    r = meet_threshold(func, 0.1)
    print(f"THRESH: {r}")


P = 0.001

@solution
def solve():
    return 235
