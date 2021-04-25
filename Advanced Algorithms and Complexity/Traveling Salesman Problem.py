# python3

"""
Traveling Salesman Problem (TSP).

The School Bus Problem is an NP-hard vehicle routing problem
(TSP) in which the goal is to find fastest route to start from
depot, visit all the children’s homes, get them to school and
return back to depot.

In this case I use a 2-approximation algorithm "Metric TSP".
First I have used kruscal algorithm using disjoint set data structure
to construct the minimal spanning tree, check if there is an Eulerian
cycle in it, then I doubled every edge.
Second I found an Eulorian cycle in it and turned it into Hamiltonian
cycle.
Third I calculate sum of all weighted edges, return it's value and
the path.
"""

import operator
from itertools import permutations
import collections
INF = 10 ** 9

class DisjointSet:
    def __init__(self, vertices, parent):
        self.vertices = vertices
        self.parent = parent

    def find(self, i, sets):
        if sets[i].parent != i:
            sets[i].parent = self.find(sets[i].parent, sets)
        return sets[i].parent

    def union(self, set1, set2, sets):
        root1 = self.find(set1, sets)
        root2 = self.find(set2, sets)
        sets[root1].parent = root2


def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    return graph


def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(' '.join(map(str, path)))


def optimal_path(graph):
    mst, edges = kruscal(graph)
    ans = isEulorian(edges, graph)
    if ans == -1:
        return (-1, [])

    dmst = mst.copy()
    dmst = mst + dmst
    rep = [0] * len(graph)
    for i in mst:
        y = i[0]
        z = i[1]
        if rep[y] == 0:
            rep[y] = [z]
        else:
            rep[y].append(z)
        if rep[z] == 0:
            rep[z] = [y]
        else:
            rep[z].append(y)
    res = []
    edges1 = {}
    for l in edges:
        edges1[l[0]] = l[1]
    visited = set()
    eulerianCycle(dmst, 0, rep, res, edges1, visited, graph)
    visited1 = set()
    resres = []
    for i in res:
        if i not in visited1:
            visited1.add(i)
            resres.append(i)
    sum = 0

    first = resres[0]
    i = 0
    j = 1

    for h in range(len(graph) - 1):
       if (resres[i], resres[j]) not in edges1:
           sum += edges1[(resres[j], resres[i])]
       else:
           sum += edges1[(resres[i], resres[j])]
       i += 1
       j += 1
    if (resres[i], first) not in edges1:
        sum += edges1[(first, resres[i])]
    else:
        sum += edges1[(resres[i], first)]
    resres2 = []
    for i in resres:
        resres2.append(i + 1)
    return sum, resres2


def eulerianCycle(dmst, v, rep, res, edges1, visited, graph):

    for i in range(len(rep[v]), 0, -1):
        if rep[v]:
            a = rep[v].pop(-1)
            if a not in visited:
                visited.add(a)
                eulerianCycle(dmst, a, rep, res, edges1, visited, graph)
    res.append(v)


def isEulorian(edges, graph):
    degree = [0] * len(graph)
    for i in edges:
        for j in i[0]:
            degree[j] += 1
    set(degree)
    if 1 in degree:
        return -1
    else:
        return 1


def kruscal(graph):
    n = len(graph)
    sets = []
    for i in range(n):
        sets.append(DisjointSet(i, i))
    x = list()
    edges = []
    visited = set()
    for j in range(n):
        for k in range(n):
            if (k, j) not in visited and j != k and graph[j][k] != 1000000000:
                visited.add((j, k))
                edges.append([(j, k), (graph[j][k])])
    edges.sort(key= lambda y: y[1])

    for f in edges:
        m = f[0][0]
        n = f[0][1]
        if sets[2].find(m, sets) != sets[n].find(n, sets):
            x.append((m, n))
            sets[m].union(m, n, sets)
    return list(x), edges


if __name__ == '__main__':
    print_answer(*optimal_path(read_data()))

# 4 6
# 1 2 20
# 1 3 42
# 1 4 35
# 2 3 30
# 2 4 34
# 3 4 12