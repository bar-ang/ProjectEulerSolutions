import project_euler as pe
from math import sqrt
from functools import partial


def gradient_decent(start, fn, grad, gamma=0.2, precision=10**-15):
    assert len(start) == len(grad), (len(start), len(grad))
    curr = start
    f_prev = fn(curr) + 2 * precision
    c = 0
    while abs(fn(curr) - f_prev) >= precision:
        f_prev = fn(curr)
        if c % 500 == 0:
            print(curr, f_prev)
        n = [c - gamma * grad[i](curr) for i, c in enumerate(curr)]
        curr = n
        c += 1
    print(curr, fn(curr))
    return fn(curr)


L = 5 / sqrt(2) - 2.5


def N(x, y, l):
    assert l == 1 or l == L
    return sqrt((x - y)**2 + l**2)


def T(b, v):
    first = N(b[0], 0, L)
    last = N(sqrt(50), b[-1], L)
    mid = [N(b[i + 1], b[i], 1) / v[i] for i in range(len(b) - 1)]
    return first + sum(mid) + last


def pseudo_dT(b, k, v, epsilon):
    b_new = b[:]
    b_new[k] = b[k] + epsilon
    return (T(b_new, v) - T(b, v)) / epsilon


def dT(b, k, v):
    if k > 0:
        left_part = (b[k] - b[k - 1]) / N(b[k], b[k - 1], 1)
        left_part /= v[k - 1]
    else:
        left_part = b[0] / N(b[0], 0, L)

    if k < len(b) - 1:
        right_part = (b[k + 1] - b[k]) / N(b[k + 1], b[k], 1)
        right_part /= v[k]
    else:
        right_part = (sqrt(50) - b[k]) / N(sqrt(50), b[k], L)

    return left_part + right_part


def grad(v, pseudo=False):
    d = dT
    if pseudo:
        d = partial(pseudo_dT, epsilon=0.000001)
    return [partial(d, k=k, v=v) for k in range(len(v) + 1)]


@pe.solution
def solve():
    start = [L, L + 1, L + 2, L + 3, L + 4, L + 5]
    v = [0.9, 0.8, 0.7, 0.6, 0.5]

    s_T = partial(T, v=v)
    s_grad = grad(v, pseudo=True)
    #print(s_T(start))
    #import pdb; pdb.set_trace()
    res = gradient_decent(start, s_T, s_grad)
    return round(res, 10)
