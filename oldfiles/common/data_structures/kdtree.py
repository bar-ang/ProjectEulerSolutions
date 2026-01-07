import numpy as np
import math

def euclidean(x, y):
    #x = np.array(x)
    #y = np.array(y)
    #return np.sqrt(np.sum((x - y)**2))
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

class KDTreeNode:
    def __init__(self, point):
        self._value = point
        self._right = None
        self._left = None

    def is_null_node(self):
        return self._value is None

    def insert(self, point, *, coord=0):
        assert self._value is not None
        if point[coord] <= self._value[coord]:
            if not self._left:
                self._left = KDTreeNode(point)
            else:
                self._left.insert(point, coord=(coord + 1) % len(self._value))
        else:
            if not self._right:
                self._right = KDTreeNode(point)
            else:
                self._right.insert(point, coord=(coord + 1) % len(self._value))

    def nearest_neighbour_search(self, point, *, coord=0, metric=euclidean):
        assert self._value is not None
        total_visited = 1
        nearest, nearest_dist = self._value, metric(self._value, point)

        if point[coord] <= self._value[coord]:
            next_branch, other_branch = self._left, self._right
        else:
            next_branch, other_branch = self._right, self._left

        if not next_branch:
            next_branch, other_branch = other_branch, next_branch

        if next_branch:
            other, dist, visited = next_branch.nearest_neighbour_search(point, coord=(coord + 1) % len(self._value))
            if dist < nearest_dist:
                nearest, nearest_dist = other, dist
            total_visited += visited
            if other_branch and dist > abs(self._value[coord] - nearest[coord]):
                other, dist, visited = other_branch.nearest_neighbour_search(point, coord=(coord + 1) % len(self._value))
                if dist < nearest_dist:
                    nearest, nearest_dist = other, dist
                total_visited += visited

        return nearest, nearest_dist, total_visited

class KDTree:
    def __init__(self, dimension, *points):
        self._dimension = dimension
        self._root = None
        self._count = 0
        for p in points:
            assert len(p) == dimension
            self.insert(p)

    def empty(self):
        return self._root is None
    
    def insert(self, point):
        assert len(point) == self._dimension
        if not self._root:
            self._root = KDTreeNode(point)
        else:
            self._root.insert(point)
        self._count += 1
    
    def nearest_neighbour_search(self, point, metric=euclidean):
        assert not self.empty(), "No nodes in tree"
        n, d, t = self._root.nearest_neighbour_search(point=point, metric=metric)
        #if self._count > 100 and t > 60*np.log(self._count):
        #    print("visited %s out of %s" % (t, self._count))
        return n, d
        