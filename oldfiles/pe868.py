from project_euler import Measure, Progress, validation, solution
from math import log2, ceil


def remove_highest(s):
    return ''.join(char for char in s if char != max(s))

def solve(t):
    if len(t) == 1:
        return 0
    size = len(t)
    prev_str = remove_highest(t)
    pos = t.index(max(t))
    prev = solve(prev_str)
    if prev % 2 == 0:
        return (prev + 1) * size - pos - 1
    else:
        return prev * size + pos



def brute_force(st):
    #n = min(st)
    #res = ''.join(chr(ord(char) - ord(n) + ord('A')) for char in st)
    return st

@validation
def validate():
    assert solve("BA") == 1, solve("BA")
    assert solve("CBA") == 3, solve("CBA")
    assert solve("ACBD") == 7, solve("ACBD")
    assert solve("DBCA") == 19, solve("DBCA")
    assert solve("ADEBC") == 12, solve("ADEBC")


@solution
def solve_all():
    return solve("NOWPICKBELFRYMATHS")
