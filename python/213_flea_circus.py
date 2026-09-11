import numpy as np
from project_euler import Measure, Progress, validation, solution

def make_grid(n):
    def unfold(x, y, m=n):
        """
        Returns the node number (in the white/black-grouped numbering)
        for grid cell at column x, row y (0-indexed, (0,0) = top-left).
        """
        base = (m // 2) * y + (x // 2)
        if (x + y) % 2 == 0:
            return base                    # white cell
        else:
            return base + m * m // 2       # black cell, offset by 18


    grid = np.zeros((n*n, n*n))

    for i in range(n):
        for j in range(n):
            if i < n-1:
                grid[unfold(i, j), unfold(i+1, j)] = 1
            if j < n-1:
                grid[unfold(i, j), unfold(i, j+1)] = 1
            if i > 0:
                grid[unfold(i, j), unfold(i-1, j)] = 1
            if j > 0:
                grid[unfold(i, j), unfold(i, j-1)] = 1

    row_sums = grid.sum(axis=1, keepdims=True)
    return grid / row_sums

@solution
def solve():
    n = 30
    grid = make_grid(n)
    grid = np.linalg.matrix_power(grid, 50)
    vacancy = np.prod(1 - grid, axis=0)
    return round(sum(vacancy), 6)
