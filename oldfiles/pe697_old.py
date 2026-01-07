import math
from functools import partial

N = 1000
P = 0.25

def B(t, n=N):
    def part(k):
        return (math.log(t)**k)/math.factorial(k)
    return t * sum([part(k)*(-1)**(k) for k in range(n)])

def D(c, n=N):
    def part(k):
        s = sum([math.log(i) for i in range(1, k+1)])
        return k*math.log(c) - s

    s = 0
    last_p = -1
    inc = True
    for k in range(n):
        p = part(k)
        if p < last_p:
            inc = False
        if p < 200 and not inc:
            break
        last_p = p
        #print(p, c)
        s += math.exp(p-c)
    return s

def inverse(b, p, n=N, ascending=True, precision=0.00001, max_iter=1000, h=1000):
    l = 0
    c = 0
    while c < max_iter:
        c += 1
        t = float(h+l) / 2
        #import pdb; pdb.set_trace()
        if c % 30 == 0:
            print(t)
        calc = b(t)
        if abs(calc - p) < precision:
            return t
        if (calc > p and ascending) or (calc < p and not ascending):
            h = t
        else:
            l = t

    assert False, ("too many iterations. got:", t)


def to_log_base(base):
    return math.log(math.exp(1), base)

#print("ANS:", D(46.27/to_log_base(10)))

r = inverse(D, P, ascending=False)*to_log_base(10)
print("ANSWER:", r)
