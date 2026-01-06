from project_euler import Measure, Progress, validation, solution

MOD = 987654319

def M_brute(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    return (2 * n - 1) * sum([M_brute(k-1)*M_brute(n-k) for k in range(1, n+1)])

def solve_dynamic(n):
    m = [-1] * (n+1)
    m[0] = 1
    m[1] = 1
    for i in range(2, n+1):
        m[i] = (2 * i - 1) * sum([m[k-1]*m[i-k] for k in range(1, i+1)])
    return m[n]

@validation
def validate():
    assert M_brute(4) == 994, M_brute(4)
    assert solve_dynamic(4) == 994, solve_dynamic(4)

    for i in range(5, 15):
        print(i)
        assert M_brute(i) == solve_dynamic(i), (M_brute(i), solve_dynamic(i))

@solution
def solve_all():
    return solve_dynamic(100) % MOD