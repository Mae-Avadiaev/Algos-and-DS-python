# python3

"""
Infer Energy Values of Ingredients Problem.

Given a restaurant menu with calorie counts of a dish
and ingredient lists provided for each dish. Infer
the energy values of ingredients.

In mathematical language we are given a system of
linear equations and we should solve it.

I have used Gaussian Elimination for this problem.
First I translated between system of equations and
augmented matrix (of coefficients).
Second I reduce rows in the matrix by basic row
operations (subtracting, adding, scaling, swapping)
which is called Gaussian Elimination (Row Reduction).
So we put the matrix into a simple standard form, and
this is the solution for the problem.

The steps of the algorithm is as following.
First we take the leftmost non-zero entry in non pivot
row (this is the thing we going to solve for) and call
it a pivot.
Second we swap the row to the top of non-pivot rows.
Third we rescale matrix to make the pivot 1.
Fourth we subtract this row from others to make other
entries in the column 0.
And we keep repeating until all non-zero entries are
in pivot rows.
"""
import math

EPS = 1e-6
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row


def ReadEquation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)


def SelectPivotElement(a, used_rows, used_columns, pivot_element):
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column]:
        pivot_element.column += 1
    if a[pivot_element.row][pivot_element.column] != 0:
        return pivot_element
    else:
        while a[pivot_element.row][pivot_element.column] == 0:
            if pivot_element.row == len(a) - 1:
                if pivot_element.column == len(a[0]) -1:
                    return -1
                else:
                    pivot_element.column += 1
            else:
                pivot_element.row += 1
        return pivot_element


def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], \
                                                                    used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column


def ProcessPivotElement(a, b, pivot_element):
    # Rescale
    divide_index = a[pivot_element.row][pivot_element.column]
    if divide_index != 1:
        for ind, val in enumerate(a[pivot_element.row]):
            a[pivot_element.row][ind] = val / divide_index
        b[pivot_element.row] = b[pivot_element.row] / divide_index
    # Substitute to other equations
    for j in range(len(a)):
        if j == pivot_element.row:
            continue
        sub_elem = a[j][pivot_element.column]
        if sub_elem != 0:
            for ind2, val2 in enumerate(a[j]):
                if sub_elem > 0:
                    a[j][ind2] -= (a[pivot_element.row][ind2] * sub_elem)
                elif sub_elem < 0:
                        a[j][ind2] += (a[pivot_element.row][ind2] * math.fabs(sub_elem))

            if sub_elem > 0:
                    b[j] -= (b[pivot_element.row] * sub_elem)
            elif sub_elem < 0:
                    b[j] += (b[pivot_element.row] * math.fabs(sub_elem))
    pass


def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True


def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    pivot_element = Position(0, 0)
    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns, pivot_element)
        if pivot_element == -1:
            return b
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    return b


def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])


if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    PrintColumn(solution)
    exit(0)

