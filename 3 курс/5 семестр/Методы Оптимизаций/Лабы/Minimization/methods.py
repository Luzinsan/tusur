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


def upper_index(base: str, index: int) -> str:
    match index:
        case 1:
            return f"{base}¹"
        case 2 | 3:
            return f"{base}{chr(ord('²') + index - 2)}"
        case 4 | 5 | 6 | 7 | 8 | 9:
            return f"{base}{chr(ord('⁰') + index)}"
        case __:
            return f"{base}⁺"


def hook_jeeves_method(expr: ExpressionMin):
    filename = "expr.txt"
    with open(filename, "rt") as file:
        expression = file.readline()
        transformations = (standard_transformations + (implicit_multiplication_application,))
        function: Expr = parse_expr(expression, transformations=transformations)  # ƒ(x)
        x_0 = np.array(list(map(float, file.readline().split())))  # начальная точка <print(f'𝒙⁰ = {x_0}')>
        delta = np.array(
            list((map(float, file.readline().split()))))  # вектор приращения (величина шага) Δ <print(f"Δ⁰ = {delta}")>
        alpha = float(file.readline())  # коэффициент сжатия (𝛂 > 1) <print(f"𝛂 = {alpha}")>
        eps_x = float(file.readline())  # точность по аргументу x (εₓ) <print(f"εₓ = {eps_x}")>
        eps_y = float(file.readline())  # точность по функции y (εᵧ) <print(f"εᵧ = {eps_y}")>

    n = 2
    e_i = np.eye(n)  # единичная матрица 𝐞
    x_approx_1 = x_0.copy()
    f_approx_1 = function.subs({x1: x_approx_1[0], x2: x_approx_1[1]})
    x_approx_0, f_approx_0 = x_approx_1.copy(), f_approx_1

    for k in range(ITERATIONS):
        print(f"\n\t\t\tИТЕРАЦИЯ: k = {k}")
        print(f"{upper_index('x̅', k)} = {x_approx_1}")  # приближение x̅ᶦ (x̅⁰ = 𝒙⁰)
        f_approx_1 = function.subs({x1: x_approx_1[0], x2: x_approx_1[1]})
        print(f"ƒ({upper_index('x̅', k)}) = {f_approx_1}")
        x_p = np.array(x_approx_1)  # исходная точка - (𝒙ᵨ⁰ = x̅ᵏ)
        print("\n\t\tИССЛЕДУЮЩИЙ ПОИСК")
        # - для каждой координаты предыдущей (исходной) точки 𝒙ᵨᶦ⁻¹
        success = False
        for i in range(n):
            print(f"{upper_index('𝒙ᵨ', i)} = {x_p}")
            f_x_p = function.subs({x1: x_p[0], x2: x_p[1]})
            print(f"ƒ({upper_index('𝒙ᵨ', i)}) = {f_x_p}")
            # x_i - 𝒙ᶦ - пробная точка
            # выполнить шаг в сторону приращения Δᵢᵏ
            x_i = x_p + delta * e_i[i]  # 𝒙ᶦ = 𝒙ᵨᶦ⁻¹ + Δᵢᵏ * 𝐞ᵢ
            print(f"Пробная точка №{i + 1}: {upper_index('𝒙', i + 1)} = {x_i}")
            f_x_i = function.subs({x1: x_i[0], x2: x_i[1]})
            if f_x_i < f_x_p:  # если в пробной значение ЦФ меньше, чем в исходной
                print(f"ƒ({upper_index('𝒙', i + 1)}) = {f_x_i}\t < \tƒ({upper_index('𝒙', i)}ᵨ) = {f_x_p}")
                # то шаг поиска удачный => 𝒙ᵨᶦ = 𝒙ᶦ
                x_p = x_i.copy()  # новой исходной точкой становится пробная
                print(f"Шаг поиска удачный: {upper_index('𝒙ᵨ', i + 1)} = {x_p}")
                success = True
            else:  # из исходной точки делается шаг в противоположном направлении
                print(f"ƒ({upper_index('𝒙', i + 1)}) = {f_x_i}\t >= \tƒ({upper_index('𝒙', i)}ᵨ) = {f_x_p}")
                # делаем шаг в обратном направлении
                x_i = x_p - delta * e_i[i]  # 𝒙ᶦ = 𝒙ᵨᶦ⁻¹ - Δᵢᵏ * 𝐞ᵢ
                print(f"Шаг в обратном направлении: {upper_index('𝒙', i + 1)} = {x_i}")
                f_x_i = function.subs({x1: x_i[0], x2: x_i[1]})
                if f_x_i < f_x_p:
                    print(
                        f"Шаг в обратном направлении удачный: ƒ({upper_index('𝒙', i + 1)}) = {f_x_i}\t < \tƒ({upper_index('𝒙', i)}ᵨ) = {f_x_p}")
                    success = True
                    x_p = x_i.copy()  # новой исходной точкой становится пробная
                print(f"Исходная точка: {upper_index('𝒙ᵨ', i + 1)} = {x_p}")
        if not success:
            print(f"\n\t\tИсследующий поиск был неудачным. \n{upper_index('x̅', k + 1)} = {x_approx_1}")
            # x_approx_1 = x_approx_0.copy()
            # f_approx_1 = f_approx_0
            delta = delta / alpha
            print(f"{upper_index('Δ', k + 1)} = {delta}")
            continue
        # Шаг №5 - Поиск по образцу
        print("\n\t\tПОИСК ПО ОБРАЗЦУ")
        print(f"{upper_index('Δ', k + 1)} = {delta}")
        # x_b - базовая точка = > 𝒙ᵦᵏ = 𝒙ᵨⁿ
        x_b = x_p.copy()
        print(f"Базовая точка: {upper_index('𝒙ᵦ', k)} = {x_b}")
        f_x_b = function.subs({x1: x_b[0], x2: x_b[1]})
        j = 1
        while True:
            # x_o - точка по образцу - шаг из полученной базовой точки вдоль прямой,
            # соединяющей эту точку с предыдущей базовой точкой
            x_o = x_p + j * (x_p - x_approx_1)
            print(f"j = {j}: Точка по образцу: {upper_index('𝒙ₒ', k)} = {x_o}")
            f_x_o = function.subs({x1: x_o[0], x2: x_o[1]})
            if f_x_o >= f_x_b:
                print(f"ƒ({upper_index('𝒙ₒ', k)}) = {f_x_o}\t >= \tƒ({upper_index('𝒙ᵦ', k)}ᵨ) = {f_x_b}")
                j -= 1
                x_o = x_b.copy()
                f_x_o = f_x_b
                print(f"При j = {j}, Поиск по образцу был удачным: {upper_index('𝒙ₒ', k)} = {x_o}")
                break
            else:
                print(f"ƒ({upper_index('𝒙ₒ', k)}) = {f_x_o}\t < \tƒ({upper_index('𝒙ᵦ', k)}) = {f_x_b}")
                print(f"Поиск по образцу удачный: {upper_index('𝒙ₒ', k)} = {x_o}")
                x_b = x_o.copy()
                f_x_b = f_x_o
                j += 1

        x_approx_0 = x_approx_1.copy()
        f_approx_0 = f_approx_1
        x_approx_1 = x_o.copy()
        f_approx_1 = f_x_o
        print(f"\n\t\t\tНовое приближение: {upper_index('x̅', k + 1)} = {x_approx_1}")

        diff_x = np.sqrt(sum(pow(coord, 2) for coord in delta))
        diff_y = abs(f_approx_1 - f_approx_0)  # |ƒ(x̅¹) - ƒ(x̅⁰)|
        print(f"|{upper_index('Δ', k + 1)}| = {diff_x}",
              f"εₓ = {eps_x}",
              f"|ƒ({upper_index('x̅', k + 1)}) - ƒ({upper_index('x̅', k)})| = {diff_y}",
              f"εᵧ = {eps_y}",
              f"ƒ({upper_index('x̅', k + 1)}) = {f_approx_1}",
              f"ƒ({upper_index('x̅', k)}) = {f_approx_0}", sep='\n')
        if diff_x <= eps_x and diff_y <= eps_y:
            break

