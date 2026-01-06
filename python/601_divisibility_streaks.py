from project_euler import Measure, Progress, validation, solution
from math import gcd
import random

def lcm(a, b):
    return (a * b) // gcd(a, b)


def lcm_all(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return lcm(lcm_all(n-1), n)

LIM = 31

def streak(n):
    assert n > 1
    k = 1
    while (n + k) % (k + 1) == 0:
        k += 1
        if k > 100:
            print(n,"?")
    return k

assert streak(13) == 4, streak(13)
assert streak(120) == 1, streak(120)
assert all([streak(420*t+1) >= 7 for t in range(2, 18)])
assert all([streak(12*t+1) >= 4 for t in range(2, 150)])

def P(s, N):
    return ((N-2) // lcm_all(s)) - ((N-2) // lcm_all(s+1))

def P_bruteforce(s, N):
    count = 0
    #for _, i in ShowProgress(range(2, N+1), "bruteforcing P(%s, %s)" % (s, N), announce_every=7.438):
    for i in range(2, N):
        if streak(i) == s:
            #print("streak(%s) = %s" % (i, s))
            count += 1
    return count

assert P(6, 10**6) == 14286
assert P_bruteforce(3, 14) == 1

@validation
def validate():
    no_plus_1 = True
    for _, i in Progress(range(1, 2), "validation"):
        a = random.randint(1, 25)
        b = random.randint(a, 4**7)
        p = P(a, b)
        p_b = P_bruteforce(a, b)
        assert p == p_b or p == p_b+1, (a, b, p, p_b)
        if p == p_b+1:
            print("P(%s, %s) == %s(+1)" % (a, b, p_b))
            no_plus_1 = False
    assert no_plus_1

    p = P_bruteforce(6, 10**6)
    assert p == 14286, p
        
@solution
def solve():
    res = [P(i, 4 ** i) for i in range(1, LIM+1)]
    print(res)
    return sum(res)
    
