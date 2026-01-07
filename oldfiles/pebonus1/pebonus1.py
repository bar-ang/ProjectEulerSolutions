from project_euler import Measure, Progress, validation, solution
from functools import partial
from scipy.special import comb
from scipy.signal import convolve2d
from scipy.sparse import csr_matrix, identity
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sympy import primerange
import sys

ncr = partial(comb, exact=True)

MOD = 7
COLORS = "seismic"

def ncr_mod(n, r, mod):
    """using Lucas Theorem"""
    res = 1
    while n > 0 and r > 0:
        res *= ncr(n % mod, r % mod)
        if res == 0:
            return 0
        res %= mod
        n //= mod
        r //= mod

    return res

def skip_zeros(n, k, m):
    """
        assuming that nCr(n, k) % m != 0
        the function will return the next value of k for which the value is non-zero
        i.e. for all k < x < skip(k) it holds nCr(n, x) % m == 0.
    """
    if k > n:
        return k
    if k == n:
        return k+1
    
    k += 1
    c = 1
    while k % m > n % m or k % m == 0:
        carry = k % m
        n //= m
        k //= m

        if carry != 0:
            k += 1
        c *= m

    k *= c
    return k

def count_iters(n, mod):
    res = 1
    while n > 0:
        res *= (n%mod)+1
        n //= mod
    return res

def convolate_small(matrix, steps, factor, mod):
    total_iters = count_iters(steps, mod)
    nmat = np.zeros_like(matrix, dtype=np.uint8)

    k = 0
    for i in range(total_iters):
        coef = ncr_mod(steps, k, mod)
        v = np.roll(matrix, k*factor, axis=(0, 1))
        nmat += v * coef
        nmat %= mod
        k = skip_zeros(steps, k, mod)

    return nmat

def convolate(matrix, steps, factor, mod):
    power = 1
    res = matrix
    while steps > 0:
        d = steps % mod
        res = convolate_small(res, d, factor*power, mod)
        power *= mod
        steps //= mod
    return res
        

def apply_steps(matrix, steps, mod, measure=None):
    matrix %= mod
    inner = convolate(matrix, steps, np.array([-1, -1]), mod)
    outer = convolate(inner, steps, np.array([-1, 1]), mod)
    res = np.roll(outer, steps, axis=0)
    return res


# @validation
def validate():
    def apply_single_step(matrix, mod):
        res = np.roll(matrix,  1, axis=0) + \
            np.roll(matrix, -1, axis=0) + \
            np.roll(matrix,  1, axis=1) + \
            np.roll(matrix, -1, axis=1)
        return res % mod
    
    def paths_bruteforce(n, x, y, mod, *, i=0, j=0):
        if n == 0:
            return 1 if x==i and y==j else 0

        return paths_bruteforce(n-1,x, y, mod, i=i+1, j=j) \
            + paths_bruteforce(n-1, x, y, mod, i=i-1, j=j) \
            + paths_bruteforce(n-1, x, y, mod, i=i, j=j+1) \
            + paths_bruteforce(n-1, x, y, mod, i=i, j=j-1)
               

    def paths(n, x, y, mod):
        x = abs(x)
        y = abs(y)
        if n == 0:
            return 1 if x == 0 and y == 0 else 0
        if (n+x+y)%2 != 0:
            return 0
        if n < y+x or n < y-x:
            return 0
        return ncr_mod(n, (n-x-y)//2, mod)*ncr_mod(n, (n+x-y)//2, mod)
    
    np.set_printoptions(threshold=np.inf)
    # test binom
    assert ncr(10, 5) == 252
    assert ncr(11, 6) == 462
    assert ncr(30, 13) == 119759850

    primes =list(primerange(200))


    testcases = [
        [2543, 1543, 10, 2000],
        [1667, 1665, 10, 1666],
        [44, 0, 10, 1],
        [44, 1, 10, 2],
        [1493, 1193, 10, 1200],
        [654321, 1, 10, 10],
        [5911, 1911, 10, 2000],
        [6669, 6668, 10, 6669],
        [6669, 6569, 10, 6600],
        [101, 1, 10, 100],
        [1, 1, 7, 2],
    ]

    for case in testcases:
        params = case[:-1]
        res = case[-1]
        actual = skip_zeros(*params)
        assert actual == res, (case, f"expected: {res}, got: {actual}")

    # test lucal' theorem
    for _, n in Progress(range(0, 30), "test lucas'"):
        for r in range(0, n+1):
            for m in primes:
                assert ncr_mod(n, r, m) == ncr(n, r) % m, (n, r, m, ncr_mod(n, r, m), ncr(n, r))

    assert paths_bruteforce(2, 0, 0, 1000) == 4, paths_bruteforce(2, 0, 0, 1000)
    assert paths_bruteforce(4, 0, 0, 1000) == 36, paths_bruteforce(4, 0, 0, 1000)

    
    # test paths
    for _, x in Progress(range(11), "testing paths (non-negative)"):
        for y in range(11):
            for n in range(1, 5):
                mod = 1000
                actual = paths(n, x, y, mod)
                expected = paths_bruteforce(n, x, y, mod)
                assert actual == expected, (n, x, y, mod, actual, expected)

    image_path = sys.argv[1]
    img = Image.open(image_path).convert('L')
    mat = np.array(img, dtype=np.uint8)[200:208,200:208]

    # test filtering
    for s in [0, -n]:
        for n in range(1 if s == 0 else 16, 14 if s == 0 else 23):
            for x in range(s, n+1):
                for y in range(s, n+1):
                    for m in [7]:# primes:
                        p1 = apply_steps(mat, n, m)
                        p2 = mat
                        for i in range(n):
                            p2 = apply_single_step(p2, m)
                            p2 %= m

                        if not np.array_equal(p1, p2):
                            print(p1[:8, :8])
                            print("\n")
                            print(p2[:8, :8])
                            assert False, (n, x, y, m)
    
    with Measure("applying steps TEST"):
        altered = apply_steps(mat, 10 ** 4, MOD)

@solution
def solve():    
    n = (10 ** 12)
    image_path = sys.argv[1]
    img = Image.open(image_path).convert('L')
    mat = np.array(img, dtype=np.uint8)
    mat %= MOD

    import pdb; pdb.set_trace()

    print(f"Image shape:{mat.shape}")
    with Measure("applying steps") as m:
        altered = apply_steps(mat, n, MOD, measure=m)

    bw = altered.astype(np.uint8)
    aimg = Image.fromarray((altered* 255)//6)
    print(f"SAVED: result_{n}.png") 
    aimg.save(f"result_{n}.png")

    plt.imshow(altered, cmap=COLORS)
    plt.show()
    
    return "Whatever you saw in the popup image"
