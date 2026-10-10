import itertools
import random
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


# 'matrify' gets 8 of these values (the sum x and the entries a, c, d, e, f, g, j)
# and returns a matrix that satisfies the conditions above.
# The other entries (b, h, i, k, l, m, n, o, p) don't need to be chosen,
# because the row, column and diagonal sums decide them.
def matrify(x, a, c, d, e, f, g, j):
    grid = np.array([
        [a, 0, c, d],
        [e, f, g, 0],
        [0, j, 0, 0],
        [0, 0, 0, 0]
    ])

    grid[0][1] = x - a - c - d                       # = B
    grid[1][3] = x - e - f - g                       # = H
    grid[2][0] = -a + d - e + g + j                  # = I
    grid[2][2] = x - f - g - j                       # = K
    grid[2][3] = a - d + e + f - j                   # = L
    grid[3][0] = x - d - g - j                       # = M
    grid[3][1] = a + c + d - f - j                   # = N
    grid[3][2] = -c + f + j                          # = O
    grid[3][3] = -a + g + j                          # = P

    return grid

def attempt(x, a, c, d, e, f, g, j):
    return (0 <= a <= 9 and 0 <= c <= 9 and 0 <= d <= 9 and 0 <= e <= 9 and
            0 <= f <= 9 and 0 <= g <= 9 and 0 <= j <= 9 and
            0 <= x - a - c - d <= 9 and                # = B
            0 <= x - e - f - g <= 9 and                # = H
            0 <= -a + d - e + g + j <= 9 and           # = I
            0 <= x - f - g - j <= 9 and                # = K
            0 <= a - d + e + f - j <= 9 and            # = L
            0 <= x - d - g - j <= 9 and                # = M
            0 <= a + c + d - f - j <= 9 and            # = N
            0 <= -c + f + j <= 9 and                   # = O
            0 <= -a + g + j <= 9)                      # = P


# prints the matrix row by row without brackets; entries longer than
# two characters (e.g. 100 or -10) are shown as '*'.
# all rows are assumed to have the same sum, so it's printed once at the end
def mat_print(grid, space=3):
    for row in grid:
        print(" ".join((str(v) if len(str(v)) <= space else "*").rjust(space) for v in row))
    print(f"sum: {sum(grid[0])}")


@validation
def validate():
    for _ in range(7):
        params = [random.randint(-20, 20) for _ in range(8)]
        x = params[0]
        mat = matrify(*params)
        mat_print(mat)

        sums = list(mat.sum(axis=1)) + list(mat.sum(axis=0)) + [np.trace(mat), np.trace(np.fliplr(mat))]
        assert all(s == x for s in sums), f"expected x={x}, got sums {sums}"
        print(f"OK: all rows, columns and diagonals sum to x={x}")
        print()


    mat = matrify(0, 1, 3, 7, 2, 0, 4, 3)
    mat_print(mat)

@solution
def solve():
    counter = 0
    for x in range(37):
        print(f"progress: {round((x)/0.37, 2)}%")
        for a in range(10):
            for g in range(10):
                for j in range(10):
                    for c in range(10):
                        for d in range(10):
                            for f in range(10):
                                for e in range(10):
                                    if attempt(x, a, c, d, e, f, g, j):
                                        counter += 1

    return counter
