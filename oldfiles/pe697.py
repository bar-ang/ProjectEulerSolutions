import math
import scipy.special as sc

N = 10 ** 7
P = 0.25

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

def base(base):
    return math.log(math.exp(1), base)


res = sc.gammainccinv(N, P)

print("ANSWER:", res, res*base(10))
print("ALSO:", D(res, N))