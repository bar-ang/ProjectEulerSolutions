import numpy as np
import project_euler as pe

def harmonic(n):
    return sum([1/float(i) for i in range(1, n+1)])

def harmonic_approx(n):
    B_num = [1, -1, 1, 0, -1, 0, 1, 0, -1, 0, 5, 0, -691, 0, 7, 0, -3617, 0, 43867, 0, -174611]
    B_denom = [1, 2, 6, 1, 30, 1, 42, 1, 30, 1, 66,1, 2730, 1, 6, 1, 510, 1, 798, 1, 330]
    assert len(B_num) == len(B_denom)
    
    base = np.log(n) + np.euler_gamma + 1/float(2*n)
    perc = sum([B_num[2*i]/(B_denom[2*i]*2*i*n**(2*i)) for i in range(1,len(B_num)//2)])
    return base - perc

def R_harmonic(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    H = harmonic_approx(n)
    return float(2 * (n + 1) * H - 3*n)/n

def R_super_slow(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    s = sum([
        a * R_super_slow(a) + (n - a - 1) * R_super_slow(n - a - 1)
        for a in range(n)
    ])
    return 1 + float(s) / (n * n)


def R_slow(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    s = sum([a * R_slow(a) for a in range(n)])
    return 1 + float(2 * s) / (n * n)

def R_dynamic(n):
    res = [0] * (n+1)
    res[0] = 0
    res[1] = 1
    for i in range(2, n+1):
        s = sum([a*res[a] for a in range(i)])
        res[i] = 1 + float(2*s)/(i*i)

    return res


def R_dynamic_stateless(n):
    res = [0] * (n+1)
    res[0] = 0
    res[1] = 1
    for i in range(2, n+1):
        j = float(i)
        res[i] = (1-(j**-2))*res[i-1] - j**-2 + 2/j

    print(res)
    return res

SHADOW = {}
def B(n):
    if n in SHADOW:
        return SHADOW[n]
    if n == 1:
        return 1
    if n == 2:
        return 1.5
    #import pdb; pdb.set_trace()
    m = float(n-1)
    up = np.ceil(m/2)
    down = np.floor(m/2)
    res = (up*B(int(up)) + down*B(int(down)) + m+1)/(m+1)
    SHADOW[n] = res
    return res

def validation():
    def approx(a, b):
        return np.isclose(a, b, atol=10**-8, rtol=0)

    assert approx(0.123456789, 0.123456781)
    assert not approx(0.23456789, 0.23456781)

    assert approx(B(6), 2.3333333333), B(6)
    print(SHADOW)
    
    print("Brute force")
    for i in range(10):
        print(i)
        assert np.isclose(R_slow(i), R_super_slow(i))

    print("Dynamic with sum")
    N = 100
    res = R_dynamic(N)
    for i in range(16):
        print(i)
        assert np.isclose(res[i], R_slow(i)), (i, res[i], R_slow(i))

    print("Dynamic Stateless")
    res_stateless = R_dynamic_stateless(N)
    for i in range(N):
        print(i)
        assert np.isclose(res[i], res_stateless[i]), (i, res[i], res_stateless[i])

    print("Harmonic approx")
    for i in range(100, 1000, 37):
        print(i)
        assert approx(harmonic(i), harmonic_approx(i)), (i, harmonic(i), harmonic_approx(i))
    
    print("R Harmonic")
    for i in range(10, N):
        print(i)
        assert approx(R_harmonic(i), res_stateless[i]), (i, R_harmonic(i), res_stateless[i])

validation()



with pe.Measure("All"):
    with pe.Measure("R"):
        r = R_harmonic(10**10)
    with pe.Measure("B"):
        b = B(10**10)
    res =  r - b

print("B", b)
print("R", r)
print("RESULT:", res)