from sympy import *
import numpy as np
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application

x1, x2 = var('x_1 x_2')
ITERATIONS = 50

if __name__ == '__main__':
    filename = "expression.txt"
    with open(filename, "rt") as file:
        expression = file.readline()
        transformations = (standard_transformations + (implicit_multiplication_application,))
        function: Expr = parse_expr(expression, transformations=transformations)
        x_0 = list(map(int, file.readline().split()))
        delta = int(file.readline())
        alpha = float(file.readline())
        eps_x = float(file.readline())
        eps_y = float(file.readline())

    print(f"{function=}\n{x_0=}\n{delta=}\n{alpha=}\n{eps_x=}\n{eps_y=}")
    n = 2
    V = np.ones((n + 1, n))
    V[0] = x_0
    p_n = delta * (sqrt(n + 1) + n - 1) / (n * sqrt(2))
    g_n = p_n - delta * sqrt(2) / 2
    # g_n = delta * (sqrt(n + 1) - 1) / (n * sqrt(2))
    for row in range(1, n + 1):
        for column in range(n):
            if row-1 == column:
                V[row][column] = V[0][column] + p_n
            else:
                V[row][column] = V[0][column] + g_n
    print(V)
    x_approx_prev = np.array([sum(V[:, i])/(n + 1) for i in range(n)])
    x_approx = x_approx_prev*2
    print(x_approx_prev)
    F_approx_prev = function.subs({x1: x_approx_prev[0], x2: x_approx_prev[1]})
    F_approx = F_approx_prev*2
    print(F_approx_prev)
    F_x = np.ones(n + 1)
    while (sum(x_approx - x_approx_prev) >= eps_x) or (abs(F_approx - F_approx_prev) >= eps_y):
        for index in range(n + 1):
            F_x[index] = function.subs({x1: V[index][0], x2: V[index][1]})
            print(F_x[index])
        print(F_x)
        p = F_x.argmax()
        F_max = F_x.max()
        V[p] = (V[:p] + V[p + 1:]) * (2 / n) - V[p]
        print(V)
        #F_approx_prev = F_approx
        F_approx = function.subs({x1: V[p][0], x2: V[p][1]})
        print(F_approx, F_max)
        if F_approx > F_max:
            delta *= alpha
            F_min = F_x.min()
            m = F_x.argmin()
        x_approx = [sum(V[:, i]) / (n + 1) for i in range(n)]
        print(x_approx)
        print(x_approx_prev)
        print(np.sqrt(sum(pow(a - b, 2) for a, b in zip(x_approx_prev, x_approx))))
        F_approx = function.subs({x1: x_approx[0], x2: x_approx[1]})
        print(F_approx_prev)
        print(F_approx)
        print(abs(F_approx - F_approx_prev))

        x_approx_prev = x_approx

        print(x_approx)

        F_0 = function.subs({x1: x_0[0], x2: x_0[1]})
        print(F_approx)




