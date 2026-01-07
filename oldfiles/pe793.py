from project_euler import Measure, Progress, validation, solution

S_0 = 290797
MOD = 50515093

def generate_numbers(n, s_0=S_0, mod=MOD):
    s = s_0
    for i in range(n):
        yield s
        s = (s * s) % mod

def solve_single(n):
    m = [g for g in generate_numbers(n)]
    m.sort(reverse=True)
    c = 0
    pos = [0] * n
    for _, i in Progress(range(n), "solving", announce_every_seconds=9):
        s = m[i]*m[pos[0]]
        for j in range(1, n):
            if m[i]*m[pos[j]] > s:
                pos[j] += 1
                c += 1
                if c == n // 2:
                    return m[i]*m[pos[j]]

@validation
def validate():
    pass

@solution
def solve():
    return solve_single(10**4+3)