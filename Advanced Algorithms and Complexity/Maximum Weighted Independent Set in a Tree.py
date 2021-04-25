#uses python3

"""
Independent sets in trees.

Planning a company party is NP-complete problem. You would like
to maximize the total fun factor (each person is assigned non
negative fun factor) with a single constraint:
you shouldn't invite a pearson with his or hers direct boss.

In mathematical words you are given a tree with weights on vertices
and you would like to find an independent set (of vertices no two
of which are adjacent) of maximum total weight.

I used dynamic programming with memoization to implement the
corresponding algorithm.
If optimal answer for the subtree rooted at vertex is not computed,
we check if the vertex v is a leaf. If so, we take it to a solution.
Otherwise we compute it's value recursively through it's children
and grandchildren. The first case is when we take the vertex into
a solution, the second when we don't. Then we select the maximum
of two values and assign it to the result.
And finally we return the result.
"""

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []
        self.children1 = []
        self.explore = int('10000000000000000')


def ReadTree():
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
        tree[a - 1].children1.append(b - 1)
        tree[b - 1].children1.append(a - 1)
    return tree


def dfs(tree, vertex, parent):
    for child in tree[vertex].children1:
        if child != parent:
            dfs(tree, child, vertex)
        else:
            tree[vertex].children.remove(child)


def MaxWeightIndependentTreeSubset(tree):
    size = len(tree)

    if size == 0:
        return 0
    dfs(tree, 0, -1)
    v = tree[0]
    result = funParty(v, tree)
    return result

def funParty(v, tree):
    if v.explore == int(10000000000000000):
        if not v.children:
            v.explore = v.weight
        else:
            m1 = v.weight
            for i in v.children:
                for j in tree[i].children:
                    m1 += funParty(tree[j], tree)
            m0 = 0
            for k in v.children:
                m0 += funParty(tree[k], tree)
            v.explore = max(m1, m0)
    return v.explore

def main():
    tree = ReadTree()
    weight = MaxWeightIndependentTreeSubset(tree)
    print(weight)


# This is to avoid stack overflow issues
threading.Thread(target=main).start()

# 6
# 1 5 3 7 5 1
# 5 4
# 2 3
# 4 2
# 1 2
# 6 2
