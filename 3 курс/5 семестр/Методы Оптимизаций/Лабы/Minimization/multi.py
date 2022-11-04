from sympy import *
import numpy as np
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application


x1, x2 = var('x_1 x_2')
ITERATIONS = 50


def simplex_method():
    filename = "expr.txt"
    with open(filename, "rt") as file:
        expression = file.readline()
        transformations = (standard_transformations + (implicit_multiplication_application,))
        function: Expr = parse_expr(expression, transformations=transformations)
        x_0 = list(map(int, file.readline().split()))  # начальная точка
        delta = int(file.readline())  # длина ребра симплекса
        alpha = float(file.readline())  # коэффициент сжатия
        eps_x = float(file.readline())  # точность по аргументу x
        eps_y = float(file.readline())  # точность по аргументу y

    print(f"{function=}\n{x_0=}\n{delta=}\n{alpha=}\n{eps_x=}\n{eps_y=}")
    n = 2
    # Симплекс 0
    V = np.ones((n + 1, n))
    V[0] = x_0  # Инициализация нулевой строки начальным приближением

    p_n = delta * (sqrt(n + 1) + n - 1) / (n * sqrt(2))
    print(f"{p_n.evalf()=}")
    g_n = p_n - delta * sqrt(2) / 2
    print(f"{g_n.evalf()=}")
    for row in range(1, n + 1):
        for column in range(n):
            if row-1 == column:
                V[row][column] = V[0][column] + p_n
            else:
                V[row][column] = V[0][column] + g_n
    print(f"{V=}")
    # начальное приближение точки минимума - геометрический центр симплекса
    x_approx_prev = [sum(V[:, i])/(n + 1) for i in range(n)]
    print(f"{x_approx_prev=}")
    F_approx_prev = function.subs({x1: x_approx_prev[0], x2: x_approx_prev[1]})
    print(f"{F_approx_prev=}")
    while True:
        F_x = np.array([function.subs({x1: V[i][0], x2: V[i][1]}) for i in range(n+1)])
        print(f"{F_x=}")
        p = F_x.argmax()
        print(f"{p=}")

        V_p = np.zeros(n)
        for row in range(n + 1):
            if row != p:
                V_p += V[row]
        V_p = V_p * (2 / n) - V[p]
        print(f"{V_p}")

        F_p = function.subs({x1: V_p[0], x2: V_p[1]})
        if F_p <= F_x[p]:
            # построить новый симплекс
            V[p] = V_p
            print(f"{V=}")
        else:
            # выполнить сжатие
            delta *= alpha
            print(f"{delta=}")
            # индекс вершины с мин.знач
            m = F_x.argmin()
            print(f"{m=}")
            V = alpha * V + (1 - alpha) * V[m]
            print(f"{V=}")
        # начальное приближение точки минимума - геометрический центр симплекса
        x_approx_curr = [sum(V[:, i]) / (n + 1) for i in range(n)]
        print(f"{x_approx_curr=}")
        F_approx_curr = function.subs({x1: x_approx_curr[0], x2: x_approx_curr[1]})
        print(f"{F_approx_curr=}")
        # Евклидова норма приближений точек оптимума
        diff_x = np.sqrt(sum(pow(a - b, 2) for a, b in zip(x_approx_prev, x_approx_curr)))
        print(f"{diff_x=}")
        diff_y = abs(F_approx_curr - F_approx_prev)
        print(f"{diff_y=}")
        if diff_x < eps_x and diff_y < eps_y:  # условие останова
            break
        else:
            x_approx_prev = x_approx_curr
            F_approx_prev = F_approx_curr

    print(f"\n\n\n\tКонечное решение: {x_approx_curr}")

simplex_method()
