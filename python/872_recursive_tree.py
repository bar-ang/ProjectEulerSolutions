from project_euler import Measure, Progress, validation, solution
from treelib import Node, Tree
import numpy as np
import codecs
import json

def binary(k):
    return bin(k)[2:]

class Node:
    def __init__(self, n=1):
        self.n = n
        self.children = []

    def make_tree(n):
        tree = Node()
        for i in range(1, n):
            tree = tree.expand()
        return tree
    
    def expand(self):
        new_node = Node(self.n + 1)
        new_node.children.append(self)
        c = self.children
        
        while len(c) > 0:
            n = c.pop(0)
            new_node.children.append(n)
            c = n.children

        return new_node

    def to_dict(self):
        if not self.children:
            return self.n
        return { self.n : [c.to_dict() for c in self.children] }
    
    def print(self, indent=0, size=3, negate=None, base=str):
        j = "*" if not self.children else ""
        k = self.n if negate is None else negate - self.n
        print(" " * (indent * size) + base(k) + j)
        for c in self.children:
            c.print(indent + 1, size=size, negate=negate)

def path_to(tree, k):
    if tree.n == k:
        return [k]
    
    paths = [path_to(c, k) for c in tree.children]
    paths = [path for path in paths if path]
    if paths:
        return [tree.n] + paths[0]
    
    return []
        

def naive_solution(n, k):
    tree = Node.make_tree(n)
    path = path_to(tree, k)
    return sum(path)

def solve(n, k):
    sum = n
    y = n - k
    while y > 0:
        t = y
        msb = 1
        while t > 1:
            msb <<= 1
            t >>= 1
        sum += n - y
        y -= msb
    
    return sum

@validation
def validate():
    assert naive_solution(6, 1) == 12
    assert naive_solution(10, 3) == 29
    assert naive_solution(40, 18) == 40+38+34+18
    assert naive_solution(40, 2) == 40+38+34+2

    assert solve(6, 1) == 12, solve(6, 1)
    assert solve(10, 3) == 29, solve(10, 3)
    assert solve(40, 18) == 40+38+34+18, solve(40, 18)
    assert solve(40, 2) == 40+38+34+2, solve(40, 2)

    for n in range(4, 150):
        for k in range(1, n):
            print("testing: f(%d, %d)" % (n, k))
            assert naive_solution(n, k) == solve(n, k), (n, k, naive_solution(n, k), solve(n, k))

@solution
def solve_all():
    return solve(10 ** 17, 9 ** 17)