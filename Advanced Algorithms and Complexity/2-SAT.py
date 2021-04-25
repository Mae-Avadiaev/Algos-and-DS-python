# python3

"""
2-SAT problem.

The 2-satisfiability problem is to find a truth assignment to these
variables that makes the whole formula true. Such an assignment
chooses whether to make each of the variables true or false, so that
at least one literal in every clause becomes true.

SAT is NP-complete, there is no known efficient solution for it.
However 2SAT can be solved efficiently in O(n+m) where n is the number
of variables and m is the number of clauses.


Given a 2-SNF formula.
First I construct the implication graph, find it's strongly connected
components and check if the variable and it's negation lies in the same
SCC. If so the word "UNSATISFIED" returned.
Second I found a topological ordering of all SCC`s in reversed order
and if literals of SCC is not assigned yet: set them to 1 and their
negations to 0.
Third I return the satisfying assignment.

"""
from queue import Queue

v, c = map(int, input().split())
clauses = [ list(map(int, input().split())) for i in range(c) ]

import sys
import resource
import threading
threading.stack_size(2**26)
sys.setrecursionlimit(10**6)

def isSatisfiable():
    g = buil_graph(v, c, clauses)
    sccs = find_sccs(g)
    for j in sccs:
        for p in sccs[j]:
            if p * -1 in sccs[j]:
                return None

    lenSccs = len(sccs)
    result = []
    preres = {}
    for o in range(lenSccs, 1, -1):
        for f in sccs[o]:
            if f not in preres:
                result.append(f)
                preres[f * -1] = False
    result.sort(key=lambda x: abs(x))
    return result


def buil_graph(v, c, clauses):
    g = {}
    for i in range(1, v + 1):
        g[i] = []
        g[-i] = []
    for j, k in clauses:
        g[j * -1].append(k)
        g[k * -1].append(j)
    return g


def find_sccs(g):
    s = []
    dfs(g, s)
    gt = gtconstruct(g)
    scc = dfs1(gt, s)
    return scc


def dfs(g, s):
    visited = {}
    for i in g:
        if i not in visited:
            explore(i, visited, s, g)


def dfs1(gt, s):
    visited = {}
    scc = {}
    coun = 1

    while s:
        v = s.pop()
        if v not in visited:
            scc[coun] = []
            explore1(v, visited, coun, scc, gt)
            coun += 1
    return scc


def explore1(v, visited, coun, scc, gt):
    visited[v] = True
    scc[coun].append(v)
    for neibour in gt[v]:
        if neibour not in visited:
            explore1(neibour, visited, coun, scc, gt)


def explore(v, visited, s, g):
    visited[v] = True
    for value in g[v]:
        if value not in visited:
            explore(value, visited, s, g)
    s.append(v)


def gtconstruct(g):
    gt = {}
    for i in range(1, v + 1):
        gt[i] = []
        gt[-i] = []
    for j, k in clauses:
        gt[k].append(j * -1)
        gt[j].append(k * -1)
    return gt


result = isSatisfiable()
if result is None:
    print("UNSATISFIABLE")
else:
    print("SATISFIABLE")
    for i in result:
        print(i, end=' ')