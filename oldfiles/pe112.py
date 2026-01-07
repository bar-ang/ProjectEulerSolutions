import random
from functools import partial

B = 10
K = 5000

def is_decending(n):
    last = -1
    while n > 0:
        d = n % 10
        if d < last:
            return False
        n //= 10
        last = d
    return True

def is_ascending(n):
    last = 10
    while n > 0:
        d = n % 10
        if d > last:
            return False
        n //= 10
        last = d
    return True

def L_force(k=K, b=B, down=True):
    n = b ** k
    c = 0
    for i in range(n):
        last = -1 if down else b+1
        is_ok = True
        while i > 0:
            if (down and i % b < last) or (not down and i % b > last):
                is_ok = False
                break
            last = i % b
            i //= b
        if is_ok:
            c += 1

    return c

def bouncy_force(n):
    c = 0
    for i in range(n):
        if not is_decending(i) and not is_ascending(i):
            c += 1

    return c

def bouncy_from_L(L_down_get, digs):
    non_bouncy = L_down_get(k=digs, b=10) + L_down_get(k=digs, b=9) + digs - 9*digs - 1
    return 10 ** digs - non_bouncy

def build_L_down(k=K, b=B):
    res = [[i+1 for i in range(b)]]
    for d in range(2, k+1):
        next = []
        for _b in range(1, b+1):
            last = res[-1]
            s = sum([last[a-1] for a in range(1, _b+1)])
            next.append(s)
        res.append(next)

    def get(k, b):
        return 1-k+sum([res[v][b-1] for v in range(0, k)])
    
    return res, get

def L_up_get_from(k, b, L_down):
    return L_down[k-1][b-2] + k

#L_down, L_down_get = build_L_down()
#L_up_get = partial(L_up_get_from, L_down=L_down)


#for i in range(100):
#    i = random.randint(1, D)
#    print("L10(%s)=%s"% (i, L_down[i][9]))

def validation():
    print("validating...")

    assert is_ascending(123)
    assert is_ascending(2269)
    assert is_ascending(4999)
    assert is_ascending(12)
    assert is_ascending(4)
    assert is_ascending(777777)
    assert is_ascending(0)

    assert is_decending(321)
    assert is_decending(721)
    assert is_decending(77777)
    assert is_decending(1)
    assert is_decending(21)
    assert is_decending(20)
    assert is_decending(200)
    assert is_decending(0)
    assert is_decending(4)
    
    for i in range(5):
        assert L_force(k=1, b=i, down=True) == i
        assert L_force(k=1, b=i, down=False) == i
        assert L_force(k=i, b=1, down=True) == 1
        assert L_force(k=i, b=1, down=False) == 1
    
    for i in range(5):
        k = random.randint(1, 6)
        b = random.randint(2, 10)
        down = L_force(k=k, b=b-1, down=True)
        up = L_force(k=k, b=b, down=False)
        assert up == down + k, (down, up, k, b)

    print("NOW")
    k_max = 6
    b_max = 10
    L_down, L_down_get = build_L_down(k=k_max, b=b_max)
    print(L_down)
    for i in range(5):
        k = random.randint(1, k_max)
        b = random.randint(2, b_max)
        print("test", i, k, b)
        ld = L_down_get(k=k, b=b)
        lfd = L_force(k=k, b=b, down=True)
        assert ld == lfd, (k, b, ld, lfd)

    for i in range(5):
        print("test", i)
        k = random.randint(1, k_max)
        b = random.randint(2, b_max)
        lu = L_down_get(k=k, b=b-1) + k
        lfu = L_force(k=k, b=b, down=False)
        assert lu == lfu, (k, b, lu, lfu)

    for i in range(5):
        print("> test", i)
        k = random.randint(3, k_max)
        bl = bouncy_from_L(L_down_get, k)
        bf = bouncy_force(10**k)
        assert bl ==  bf, (k, bl, bf)

validation()

def solve_for_num_digits(L, rat_a=99, rat_b=100):
    d = 2
    while rat_b * bouncy_from_L(L, d) < rat_a * (10 ** d):
        print(d, bouncy_from_L(L, d)/(10 ** d))
        d += 1
    return d-1
                        
def solve():
    print("building...")
    L_down, L_down_get = build_L_down(k=K, b=B)
    print("solving...")

    perc = 99
    
    d = solve_for_num_digits(L_down_get, perc, 100)

    c = bouncy_from_L(L_down_get, d)
    m = 10 ** d
    print(d, c, m)
    while 100 * c < perc * m:
        m += 1
        if not is_ascending(m) and not is_decending(m):
            c += 1
    print(m)

solve()