from project_euler import Measure, Progress, validation, solution
import numpy as np

N = 10

def T(k, n=N):
    t = np.zeros((n, n))
#    t[n-k-1][0] = 1
    for i in range(k):
        for j in range(i+1):
            t[i+n-k][j] = 1
    return t

def trace(k):
    t = T(k)
    for i in range(k-1, 0, -1):
        t = np.matmul(t, T(k))
        print(t)
    return t

@validation
def validate():
    t = trace(9)
    print(t)
    
