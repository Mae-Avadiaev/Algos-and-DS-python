# python3

"""
Optimal Diet Problem.

We have a number of types of food, and we gonna optimize
our diet so that it satisfies all the recommendations
of nutrition experts, and we also get maximum pleasure
from our food. For each dish we know all the nutrition
facts, cost of one item, an estimation of pleasure,
and our budget is limited.

The budget restriction and the nutrition recommendations
can be converted into a system of linear inequalities.
It is a linear programming problem.

We have a few edge cases, first when we have a system which
has no solution ("No solution"), second when we have no
optimum ("Infinity").

I have used Simplex Method to solve this problem.
So we begin optimization from starting vertex. We know that
the optimum is at another vertex. So we gonna find the path
between this two vertices.
First we need to find 'a' solution (starting point). For
this we add inequalities one at a time, and use linear
optimization to optimize left-hand side of next equation.
Second we need to find the best solution. So we repeat the
following: we look over each equation passing trough our
vertex and we relax the equation to get an edge. If (when we
travel along that edge) it improves the objective we replace
our vertex by the vertex that we find in the end of that edge.
If no improvement - we return the vertex (optimum).
"""

from sys import stdin
import numpy as np
import math


infinity = False
count_a = 0
art_arr = []
count_surp = 0


def solve_diet_problem(n, m, A, b, c):
    mat, count_art = gen_matrix(m, n, b)
    for ind, i in enumerate(A):
        if b[ind] >= 0:
            cons = ''
            for j in i:
                cons += str(j) + ','
            cons += 'L,'
            cons += str(b[ind])
            constrain(mat, cons, m, count_art, n)
        else:
            cons = ''
            for j in i:
                cons += str(j * -1) + ','
            cons += 'G,'
            cons += str(b[ind] * -1)
            constrain(mat, cons, m, count_art, n)

    obj_f = ''
    for ind, k in enumerate(c):
        obj_f += str(k)
        if ind != len(c) - 1:
            obj_f += ','
    obj(mat, obj_f, m, n)
    # check
    global infinity
    if n == 1:
        for l in range(len(mat[0])):
            if mat[0][l] < 0:
                coun = 0
                for q in c:
                    if q <= 0:
                        coun += 1
                if coun == len(c):
                    res = [0] * len(c)
                    infinity = True
                else:
                    res = None
                    infinity = True
    if not infinity:
        res = maxz2(mat, m, n, count_art)
    if res != 'infeasible' and res != None:
        for w in res:
            if w < 0:
                res = 'infeasible'
    if res is None:
        if infinity:
            return [1, [0] * m]
    elif res == 'infeasible':
        return [-1, [0] * m]
    else:
        return[0, res]


def maxz2(mat, var, cons, count_art):
    subtract_m(mat, count_art, var, cons)
    var_arr = solution_exists(mat)
    co = 0
    global infinity
    while min_elem_bott_row(mat) is not None:
        mebr = min_elem_bott_row(mat)
        mr = min_row(mat, mebr)
        if mr > len(var_arr) - 1:
            var_arr[-1] = mebr
        else:
            var_arr[mr] = mebr
        new_row = []
        if mat[mr][mebr] == 0:
            infinity = True
            return None
        for i in range(len(mat[mr])):
            new_row.append(mat[mr][i] / mat[mr][mebr])
        mat[mr] = new_row
        mat = gaussian_elimination(mat, mebr, mr, var, cons)
        co += 1
    res = []
    for k in art_arr:
        for p in range(var + cons, var + cons + count_art):
            u = art_var_is_basic(mat, p)
            if u:
                if round(mat[u][-1]) > 0:
                    return 'infeasible'
    for i in range(var):
        if i not in var_arr:
            res.append(0)
        else:
            a = var_arr.index(i)
            res.append(mat[a][-1])
    return res


def art_var_is_basic(mat, p):
    coun = 0
    coun_zeros = 0
    for ind, j in enumerate(mat[:, p]):
        if j > 0:
            coun += 1
            ind_bv = ind
        elif j == 0:
            coun_zeros += 1
    if coun == 1 and coun_zeros == (len(mat[:, p]) - 1):
        return ind_bv
    return False


def solution_exists(mat):
    basic_vars = []
    for i in range(len(mat[0])):
        coun = 0
        coun_zeros = 0
        for ind, j in enumerate(mat[:, i]):
            if j > 0:
                coun += 1
                ind_bv = ind
            elif j == 0:
                coun_zeros += 1
        if coun == 1 and coun_zeros == (len(mat[:, i]) - 1):
            basic_vars.append(i)
    if len(basic_vars) != 0:
        basic_vars.pop(-1)
    return basic_vars


def subtract_m(mat, count_art, var, cons):
    a = count_art
    while a > 0:
        for j in range(len(mat)):
            if mat[j][var + cons + a - 1] == 1:
                this_col = j
                break
        val = mat[-1][var + cons + a - 1]
        for i in range(len(mat[-1])):
            mat[-1][i] -= (val * mat[this_col][i])
        a -= 1


def find_first(mat, var):
    new_vertex = np.zeros((1, len(mat[0])))
    vals = mat[:, -1]
    for i in range(var, len(mat[0]) - 2):
        new_vertex[0][i] = vals[i - var]
    return new_vertex


def min_elem_bott_row(mat):
    idx = np.where(mat[-1] == min(mat[-1][:-1]))
    idx = list(idx)
    idx = int(idx[0][0])
    if mat[-1][idx] < 0:
        return idx
    else:
        return None


def min_row(mat, mebr):
    vals = mat[:-1, -1]
    new_row = []
    for i in range(len(mat) - 1):
        if round(mat[i][mebr], 4) != 0 and round(mat[i][mebr], 4) > 0:
            new_row.append(vals[i] / mat[i][mebr])
        else:
            new_row.append(float('+inf'))
    ind = new_row.index(min(new_row))
    return ind


def gaussian_elimination(mat, mebr, mr, var, cons):
    for i in range(len(mat)):
        if i != mr:
            sub_elem = mat[i][mebr]
            for j in range(len(mat[mr])):
                if sub_elem > 0:
                    mat[i][j] -= (mat[mr][j] * sub_elem)
                elif sub_elem < 0:
                    mat[i][j] += mat[mr][j] * math.fabs(sub_elem)
    return mat


def first_nonneg_in_col(mat):
    nonneg = False
    for i in range(len(mat) - 1):
        for j in range(len(mat[i])):
            if mat[i][j] < 0:
                neg_elem = mat[i][j]
                neg_col = i
                neg_ind = j
                nonneg = True
                break
    if nonneg:
        for k in range(len(mat[neg_col])):
            if mat[neg_col][k] > 0:
                return k
    else:
        return None


def gen_matrix(var, cons, b):
    count_art = 0
    for i in b:
        if i < 0:
            count_art += 1
    tab = np.zeros((cons + 1, var + cons + 2 + count_art))
    return tab, count_art


def constrain(table, eq, var1, count_art, cons):
    if add_cons(table) == True:
        lc = len(table[0, :])
        lr = len(table[:, 0])
        var = lc - lr - 1 - count_art
        j = 0
        while j < lr:
            row_check = table[j, :]
            total = 0
            for i in row_check:
                total += float(i ** 2)
            if total == 0:
                row = row_check
                break
            j += 1
        if 'G' in eq:
            G = True
        else:
            G = False
        eq = convert(eq)
        i = 0
        while i < len(eq) - 1:
            row[i] = eq[i]
            i += 1
        row[-1] = eq[-1]
        if G:
            global count_surp
            count_surp += 1
            row[var + j] = -1
            global count_a
            row[var1 + cons + count_a] = 1
            count_a += 1
            global art_arr
            art_arr.append(j)
        else:
            row[var + j] = 1
    else:
        print('Cannot add another constraint.')


def convert(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i) for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq


def add_obj(table):
    lr = len(table[:, 0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            total += j ** 2
        if total == 0:
            empty.append(total)
    if len(empty) == 1:
        return True
    else:
        return False


def obj(table, eq, var, cons):
    eq = [float(i) for i in eq.split(',')]
    lr = len(table[:, 0])
    row = table[lr - 1, :]
    i = 0
    while i < len(eq):
        row[i] = eq[i] * -1
        i += 1
    row[-2] = 1
    row[-1] = 0
    global count_a
    while count_a > 0:
        row[var + cons + count_a - 1] = 10000
        count_a -= 1


def convert_min(table):
    table[-1, :-2] = [-1 * i for i in table[-1, :-2]]
    table[-1, -1] = -1 * table[-1, -1]
    return table


def gen_var(table):
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    v = []
    for i in range(var):
        v.append('x' + str(i + 1))
    return v


def add_cons(table):
    lr = len(table[:, 0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            total += j ** 2
        if total == 0:
            empty.append(total)
    if len(empty) > 1:
        return True
    else:
        return False


def maxz(table):
    while next_round_r(table) == True:
        a = loc_piv_r(table)[0]
        b = loc_piv_r(table)[1]
        table = pivot(a, b, table)
        if table.all() == -1:
            return
    while next_round(table) == True:
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)
        if table.all() == -1:
            return
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    i = 0
    val = {}
    for i in range(var):
        col = table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc, -1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1, -1]
    return val


def minz(table):
    table = convert_min(table)
    while next_round_r(table) == True:
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)
    while next_round(table) == True:
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    i = 0
    val = {}
    for i in range(var):
        col = table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc, -1]
        else:
            val[gen_var(table)[i]] = 0
            val['min'] = table[-1, -1] * -1
    return val


n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
    A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
c = list(map(int, stdin.readline().split()))

anst, ansx = solve_diet_problem(n, m, A, b, c)

if anst == -1:
    print("No solution")
if anst == 0:
    print("Bounded solution")
    print(' '.join(list(map(lambda x: '%.18f' % x, ansx))))
if anst == 1:
    print("Infinity")


