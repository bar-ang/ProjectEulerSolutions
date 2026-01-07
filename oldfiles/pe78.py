from project_euler import Measure, Progress, validation, solution

#def p_recursive(n, k=None):
#    if not k or k > n:
#        k = n
#    if k <= 1:
#        return 1
#    if n <= 1:
#        return n
#    return p_recursive(n-k, k) + p_recursive(n, k-1)

def p_recursive(n, k=None):
    if not k or k > n:
        k = n
    assert n >= 0 and k >= 0
    if k <= 1:
        return 1
    if n <= 1:
        return n
    return p_recursive(n, k//2) + p_recursive(n-k//2, k-(k//2))

@validation
def validate():
    assert p_recursive(5) == 7, p_recursive(5)

@solution
def solve_all():
    res = []
    for i in range(2, 62):
        t = p_recursive(i)
        print(f"p({i}) = {t}")
        res.append(t)
    return res
