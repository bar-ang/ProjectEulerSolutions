from project_euler import Measure, Progress, validation, solution
import math
import sys


def p123(n):
    low = math.log10(1.23)
    high = math.log10(1.24)

    t = 1
    found = 0
    while found < n:
        x = t*math.log10(2)
        x -= math.floor(x)
        if x < high and x > low:
            found += 1
            if found % (n//17) == 0:
                print(f"found {round(found*100/n)}%")
        t += 1
    return t-1

@validation
def validate():
    assert p123(45) == 12710, p123(45)

@solution
def solve():
    return p123(678910)
