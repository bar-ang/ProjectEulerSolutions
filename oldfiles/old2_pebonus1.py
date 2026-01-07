from project_euler import Measure, Progress, validation, solution
import numpy as np
from PIL import Image
from scipy.special import comb
import json
with Measure("import pyplot"):
    import matplotlib.pyplot as plt


N = 10 ** 12
MOD = 7

def sp_binom(a, b):
    return comb(a, b, exact=True)

def img_to_mat(img, scale = 1):
    w, h = img.size
    res = np.zeros((h//scale, w//scale))
    for i in range(w // scale):
        for j in range(h // scale):
            res[j,i] = img.getpixel((i*scale, j*scale))
    return res


def plot_mat(mat, with_min=False):
    min = 0 if not with_min else mat.min()
    if (mat.max() > min):
        m = (mat-min) * (255.0/(mat.max()-min))
    else:
        m = mat-min
    img = np.stack([m, m, m], axis=2).astype(np.uint8)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def binom(a, b, mod):
    if a < 0 or b < 0:
        return 0
    
    if a < b:
        return 0

    res = 1
    while a > 0 or b > 0:
        res *= int(sp_binom(a % mod, b % mod))
        res %= mod
        if res == 0:
            return 0
        a //= mod
        b //= mod
        
    return res

def paths(n, x, y, mod):
#    import pdb; pdb.set_trace()
    x = abs(x)
    y = abs(y)
    if (n+x+y) % 2 != 0:
        return 0
    return (binom(n, (n-x-y)//2, mod) * binom(n, (n+x-y)//2, mod)) % mod 

#paths(10**12, 4, 2, 7)

def paths_matrix(n, w, h):
    mat = np.zeros((w, h))
    for _,i in Progress(range(w), "generating paths matrix"):
        for j in range(h):
            ps = paths(n, i, j, MOD)
            if ps != 0:
                import pdb; pdb.set_trace()
            mat[i, j] = ps
    return mat

def calc_for_pixel(steps, mat, paths_mat, x, y, mod):
    w, h = mat.shape
    res = 0
    # for _, i in Progress(range(w), f"calc for pixel ({x}, {y})"):
    for i in range(w):
        for j in range(h):
           if mat[i, j] % mod != 0:
               res += ((mat[i,j] % mod) * (paths_mat[abs(i-x), abs(j-y)] % mod))
               res %= mod
    return res

@validation
def validate():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    for m in primes:
        for a in range(100):
            for b in range(100):
                bin = binom(a, b, m)
                s = int(sp_binom(a, b)) % m
                assert bin == s, (m, a, b, bin, s)

    def paths_slow(n, x, y, mod):
        if (n+x+y) % 2 != 0:
            return 0
        s = 0
        x = abs(x)
        y = abs(y)
        for t in range(n+1):
            s += int(binom(n, t, mod)) * int(binom(n-t, t-x, mod)) * int(binom(n - 2*t + x, (n+x+y)//2 - t, mod))
            s %= mod

        return s

    
    for _, x in Progress(range(0, 11)):
        for y in range(0, 11):
            for n in range(4, 30, 2):
                for m in primes:
                    assert paths(n, x, y, m) == paths_slow(n, x, y, m),(n, paths(n, x, y, m), paths_slow(n, x, y, m)) 

    for m in primes:
        for i in range(4, 18, 2):
            p = paths(i, 0, 0, mod=m)
            s = int(sp_binom(i, i//2)**2) % m
            assert p == s, (i, m, p, s)

    with Measure("calculating paths for high number"):
        for _, x in Progress(range(0, 110)):
            for y in range(0, 110):
                paths(10 ** 12, x, y, MOD)

@solution
def solve():
    img = Image.open("common/bonus_secret_statement.png").convert("L")
    print(img.size)
    with Measure("converting image"):
         mat = img_to_mat(img)

    print("original image:")
#    plot_mat(mat)
    mat %= 7
    print("image mod 7:")
#    plot_mat(mat)

    w, h = mat.shape
    mat2 = mat.copy()
    paths_mat = paths_matrix(N, w, h)
    matrix_list = paths_mat.tolist()
    with open('paths_matrix.json', 'w') as f:
        json.dump(matrix_list, f)
    plot_mat(paths_mat)
    print(f"paths max value: {int(paths_mat.max())}")
    assert int(paths_mat.max()) > 0
    for _, x in Progress(range(w), announce_every_seconds=20):
        for _, y in enumerate(range(h)):
            mat2[x,y] =  calc_for_pixel(N, mat, paths_mat, x, y, MOD)
    

    print("the same?:")
    plot_mat(mat)
    print("THE RESULT:")
    plot_mat(mat2)

    # Convert to a nested list
    matrix_list = mat2.tolist()

    # Save to JSON file
    with open('matrix.json', 'w') as f:
        json.dump(matrix_list, f)

    return ":)"
