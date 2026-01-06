from project_euler import Measure, Progress, validation, solution
import numpy as np

@solution
def solve():
    matrix = np.array([
        [1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1],
        [1, 1, 0, 0, 0, 0],
    ])

    matrix = matrix / 2
    n = 100


    np.set_printoptions(formatter={'float': '{:0.3f}'.format})
    result = np.linalg.matrix_power(matrix, n)
    print(matrix)
    print("\n")
    print(result)
    return ":)"
