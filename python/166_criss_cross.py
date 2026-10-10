import itertools
import numpy as np
from project_euler import Measure, Progress, validation, solution

# We're dealing with a 4x4 grid of numbers, and we mark each entry with a variable:
#
#     a b c d
#     e f g h
#     i j k l
#     m n o p
#
# Every row, every column and both diagonals add up to the same sum,
# which we mark as x:
#
#     rows:      a+b+c+d = e+f+g+h = i+j+k+l = m+n+o+p = x
#     columns:   a+e+i+m = b+f+j+n = c+g+k+o = d+h+l+p = x
#     diagonals: a+f+k+p = d+g+j+m = x


# 'matrify' gets 8 of these values (the sum x and the entries a, b, c, e, f, g, i)
# and returns a matrix that satisfies the conditions above.
# The other entries (d, h, j, k, l, m, n, o, p) don't need to be chosen,
# because the row, column and diagonal sums decide them.
def matrify(x, a, b, c, e, f, g, i):
    grid = np.array([
        [a, b, c, 0],
        [e, f, g, 0],
        [i, 0, 0, 0],
        [0, 0, 0, 0]
    ])

    grid[0][3] = x - a - b - c                       # = D
    grid[1][3] = x - e- f- g                         # = H
    grid[2][1] = -x + 2*a + b + c + e - g + i        # = J
    grid[2][2] = 2*x - 2*a - b - c - e - f - i       # = K
    grid[2][3] = f + g - i                           # = L
    grid[3][0] = x - a - e - i                       # = M
    grid[3][1] = 2*x - 2*a - 2*b - c - e - f + g - i # = N
    grid[3][2] = -x + 2*a + b + e + f - g + i        # = O
    grid[3][3] = -x + a + b + c + e + i              # = P

    return grid


# checks whether every entry in the matrix is between low and high (inclusive)
def in_range(grid, low=0, high=9):
    return bool(np.all((grid >= low) & (grid <= high)))


# prints the matrix row by row without brackets; entries longer than
# two characters (e.g. 100 or -10) are shown as '*'.
# all rows are assumed to have the same sum, so it's printed once at the end
def mat_print(grid):
    for row in grid:
        print(" ".join((str(v) if len(str(v)) <= 2 else "*").rjust(2) for v in row))
    print(f"sum: {sum(grid[0])}")


def explore(explored, x, a, b, c, e, f, g, i):
    vars = (x, a, b, c, e, f, g, i)

    # every var moves by -1, 0 or +1, independently of the others
    for deltas in itertools.product((-1, 0, 1), repeat=len(vars)):
        if any(deltas):
            new_vars = tuple(v + d for v, d in zip(vars, deltas))
            mat = matrify(*new_vars)
            key = mat.tobytes()
            if key in explored or not in_range(mat):
                continue

            if in_range(mat):
                explored.add(key)
                explore(explored, *new_vars)


@validation
def validate():
    mat = matrify(50, 2, 1, 2, 1, 2, 3, 3)
    mat_print(mat)
    print(mat[1][2])


@solution
def solve():
    explored = set(np.zeros((4,4)).tobytes())
    explore(explored, 0, 0, 0, 0, 0, 0, 0,  0)
    return -444
