import numpy as np
from sympy import *
import dearpygui.dearpygui as dpg

from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application

x1, x2 = var('x_1 x_2')
ITERATIONS = 50


class ExpressionMin:
    def __init__(self, from_source) -> None:
        if from_source == "from file":
            filename = dpg.get_value('filename')
            with open(filename, "rt") as file:
                expression = file.readline()
                transformations = (standard_transformations + (implicit_multiplication_application,))
                self.function: Expr = parse_expr(expression, transformations=transformations)
                self.x_0 = list(map(float, file.readline().split()))  # начальная точка
                self.delta = float(file.readline())  # длина ребра симплекса
                self.alpha = float(file.readline())  # коэффициент сжатия
                self.eps_x = float(file.readline())  # точность по аргументу x
                self.eps_y = float(file.readline())  # точность по аргументу y
        elif from_source == "from field":
            expression = dpg.get_value('expr')
            transformations = (standard_transformations + (implicit_multiplication_application,))
            self.function: Expr = parse_expr(expression, transformations=transformations)
            self.x_0 = dpg.get_value('x_0')  # начальная точка
            self.delta = dpg.get_value('delta')  # длина ребра симплекса
            self.alpha = dpg.get_value('alpha')  # коэффициент сжатия
            self.eps_x = dpg.get_value('eps_x')  # точность по аргументу x
            self.eps_y = dpg.get_value('eps_y')  # точность по аргументу y

    def __str__(self):
        return f"{self.function=}" + f"{self.x_0=}" + f"{self.delta=}" + f"{self.alpha=}" + f"{self.eps_x=}" + f"{self.eps_y=}"


def simplex_method(expr: ExpressionMin):
    function, x_0, delta, alpha, eps_x, eps_y = expr.function, expr.x_0, expr.delta, expr.alpha, expr.eps_x, expr.eps_y
    n = 2
    # Симплекс 0
    V = np.ones((n + 1, n))
    V[0] = x_0  # Инициализация нулевой строки начальным приближением

    p_n = delta * (sqrt(n + 1) + n - 1) / (n * sqrt(2))
    g_n = p_n - delta * sqrt(2) / 2
    for row in range(1, n + 1):
        for column in range(n):
            if row - 1 == column:
                V[row][column] = V[0][column] + p_n
            else:
                V[row][column] = V[0][column] + g_n
    # начальное приближение точки минимума - геометрический центр симплекса
    x_approx_prev = [sum(V[:, i]) / (n + 1) for i in range(n)]
    F_approx_prev = function.subs({x1: x_approx_prev[0], x2: x_approx_prev[1]})
    iter = 0
    while iter < ITERATIONS:
        F_x = np.array([function.subs({x1: V[i][0], x2: V[i][1]}) for i in range(n + 1)])
        p = F_x.argmax()
        V_p = np.zeros(n)
        for row in range(n + 1):
            if row != p:
                V_p += V[row]
        V_p = V_p * (2 / n) - V[p]
        F_p = function.subs({x1: V_p[0], x2: V_p[1]})
        if F_p <= F_x[p]:
            V[p] = V_p  # построить новый симплекс
        else:
            delta *= alpha # выполнить сжатие
            m = F_x.argmin()  # индекс вершины с мин.знач
            V = alpha * V + (1 - alpha) * V[m]  # перемещение точек для получения (1/2) ребра

        # начальное приближение точки минимума - геометрический центр симплекса
        x_approx_curr = [sum(V[:, i]) / (n + 1) for i in range(n)]
        F_approx_curr = function.subs({x1: x_approx_curr[0], x2: x_approx_curr[1]})
        # Евклидова норма приближений точек оптимума
        diff_x = np.sqrt(sum(pow(a - b, 2) for a, b in zip(x_approx_prev, x_approx_curr)))
        diff_y = abs(F_approx_curr - F_approx_prev)
        if diff_x < eps_x and diff_y < eps_y:  # условие останова
            break
        else:
            x_approx_prev = x_approx_curr
            F_approx_prev = F_approx_curr
        iter +=1
    if iter == ITERATIONS:
        x_approx_curr = np.zeros(n)
    return x_approx_curr


def hook_jeeves_method(expr: ExpressionMin):
    pass