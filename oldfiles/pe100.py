from project_euler import Measure, Progress, validation, solution
from math import sqrt

def square(n):
    k = int(sqrt(n))
    if k ** 2 == n:
        return k
    else:
        return None


def solve(begin):
    b = Progress(range(7074*10**8, 7090*10**8))
    print("built...")
    for _, x in b:
        if x % 21346921 == 155:
            print(x)
        k = square(8*x*(x-1) + 1)
        if k and k % 2 == 1:
            return k
        if k:
            print("is EVEN SQUARE!")

@validation
def validate():
    assert square(16) == 4
    assert square(81) == 9
    assert square(1) == 1
    assert square(4) == 2
    assert square(10**14) == 10 ** 7
    assert square(3) is None
    assert square(5) is None
    assert square(18) is None
    assert square(80) is None
    assert square(10**15) is None

@solution
def solve_all():
    x = 1
    while True:
        t = 2*x*x-1
        t_ = square(t)
        if t_:
            print(x, t, (q+1)//2)
            if (t_+1)//2 > 10 ** 12:
                return (t+1) // 2
        x += 2
