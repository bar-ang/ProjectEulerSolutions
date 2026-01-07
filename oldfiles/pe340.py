from project_euler import Measure
#import matplotlib.pyplot as plt
import random
import sys; sys.setrecursionlimit(12000)


A = 21 ** 7
B = 7 ** 21
C = 12 ** 7
N = B



def F(n, a=A, b=B, c=C):
    if n > b:
        return n - c
    return F(a + F(a + F(a + F(a + n, a, b, c), a, b, c), a, b, c), a, b, c)

def S_force(a, b, c):
    return sum([F(n, a, b, c) for n in range(0, b+1)])

def S(a, b, c):
    assert c < a
    m = b//a
    s = b + 4*a - 4*c + m * (b + 4*(a-c) + (a-1)*(b-c) + a*(a-1)//2) + 3*a*(a-c) * (m+1)*m // 2 + ((3*m+4)*(a-c) + m*a)*(b-m*a) + (b-m*a)*(b-m*a-1)//2
    return s

def combicheck(a, b):
    q = [b]
    for t in range(1, b // a+1):
        for r in range(0, a):
            q.append(b-t*a+r)

    q += list(range(0, b-(b//a)*a))
    assert set(q) == set(range(b+1)), (a, b,  set(q).symmetric_difference(range(b+1)))

def validation():
    print("start")
    for i in range(20):
        b = random.randint(1, 20000)
        a = random.randint(2, b)
        c = random.randint(0, a-1)
        d = random.randint(1, a-1)
        t = random.randint(0, b // a)
        k = random.randint(0, b - a*(b // a))
        print("validation #%s: a=%s, b=%s, c=%s" % (i+1, a, b, c))
        assert F(b, a, b, c) == b +4*a - 4*c, (F(b, a, b, c))
        assert F(b-a+1, a, b, c) == 3*a + b - 4*c + 1
        assert F(b-2*a+1, a, b, c) == 6*a + b - 7*c + 1
        assert F(b-t*a+1, a, b, c) == 3*t*(a-c) + b - c + 1
        assert F(b-t*a-d+1, a, b, c) - F(b-t*a-d, a, b, c) == 1
        assert F(b-t*a+d, a, b, c) == 3*t*(a-c) + b - c + d
        assert F(k+a, a, b, c) == (3*(b//a)+1)*(a-c) + k + (b//a)*a
        assert F(k, a, b, c) == (3*(b//a)+4)*(a-c) + k + (b//a)*a 

    assert S_force(50, 2000, 40) == 5204240
    assert S(50, 2000, 40) == 5204240, S(50, 2000, 40) - 5204240

    with Measure("S function"):
        S(150, 20000, 70)
    
    for i in range(10):
        print("next validation #%s: a=%s, b=%s, c=%s" % (i+1, a, b, c))
        a = random.randint(1, 1000)
        b = random.randint(1, a*40)
        c = random.randint(0, a-1)
        combicheck(a, b)
        assert S(a, b, c) == S_force(a, b, c), (a, b, c, S(a, b, c), S_force(a, b, c), S(a, b, c) - S_force(a, b, c))

validation()

def plot_F():
    x = list(range(N+1))
    y = [F(i) for i in range(N+1)]
    breaks = [(i, y[i]) for i in range(0, N) if y[i] > y[i+1] or y[i] < y[i-1]] + [(0, y[0]), (B, y[B])]
    print("\t".join("F(%s) = %s" % (a, b) for a, b in breaks))
    
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('F(x)')
    
    for xy in breaks:
       plt.annotate('(%d, %d)' % xy, xy=xy)
    
    plt.title('F(x) for: a=%s, b=%s, c=%s' % (A, B, C))
    
    plt.show()

print("Now solving...")
with Measure("S(%s, %s, %s)" % (A, B, C)):
    res = S(A, B, C) 

print("Full Result:", res)
print("ANSWER:", res% 10**9)