from project_euler import Measure, Test, Progress, validation, solution


def Q_recursive(n, d):
    def minimize(a):
        return max(q(a, d-1), q(n-a, d+a-1))

    if d == 0:
        return n - 1
    if n == 1:
        return 0
    if d > n:
        return Q_recursive(n, n)

    q = Q_recursive
    a, res = min(((t, minimize(t)) for t in range(1, n)), key=lambda x: x[1])
    return 1 + res


def Q_dynamic(nlim, dlim):
    def minimize(a):
        return max(q[a][d-1], q[n-a][min(d+a-1, dlim-1)])

    q = [[None for _ in range(dlim)] for _ in range(nlim)]

    for d in range(dlim):
        q[1][d] = 0

    for n in range(1, nlim):
        q[n][0] = n - 1

    for _, n in Progress(range(2, nlim)):
        for d in range(1, dlim):
            if d > n:
                q[n][d] = q[n][n]
                continue

            if d < (n+1)//2:
                a = min(range(d, (n+1)//2+1), key=minimize)
            else:
                a = (n+1)//2
           # a = min(range(1, n), key=minimize)
            t = 1 + minimize(a)
            q[n][d] = t

    return q


@validation
def validate():
    Test.equals(3, Q_recursive, 7, 1)
    Test.equals(3, Q_recursive, 5, 2)
    #Test.equals(10, Q_recursive, 777, 2)

    print("first test")
    maxn = 17
    maxd = 3
    q = Q_dynamic(maxn, maxd)
    for _, i in Progress(range(1, maxn)):
        for j in range(1, min(i+1, maxd)):
            assert q[i][j] == Q_recursive(i, j), (q[i][j], Q_recursive(i, j), i, j)

    print("second test")
    maxn = 13
    maxd = 13
    q = Q_dynamic(maxn, maxd)
    for _, i in Progress(range(1, maxn)):
        for j in range(1, min(i+1, maxd)):
            assert q[i][j] == Q_recursive(i, j), (q[i][j], Q_recursive(i, j), i, j)

    print("DO NOT GET STUCK!")
    with Measure("allocating"):
        q = [0 for _, _ in Progress(range(7 ** 11))]

@solution
def solve():
    n = 100#7 ** 3
    d = 7
    q = Q_dynamic(n+1, d+1)
    return sum([
        sum(
            [q[i][j] for i in range(1, n+1)]
        ) for _, j in Progress(range(1, d+1), "summing")
    ])
