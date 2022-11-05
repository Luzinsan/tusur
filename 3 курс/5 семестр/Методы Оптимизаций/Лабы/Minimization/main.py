import dearpygui.dearpygui as dpg
from sympy import *
import numpy as np
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application

dpg.create_context()
dpg.create_viewport(title='Minimization', width=960, height=750)

x1, x2 = var('x_1 x_2')
ITERATIONS = 50


class ExpressionMin:
    def __init__(self, source) -> None:
        if source == "from file":
            filename = dpg.get_value('filename')
            with open(filename, "rt") as file:
                expression = file.readline()
                transformations = (standard_transformations + (implicit_multiplication_application,))
                self.function: Expr = parse_expr(expression, transformations=transformations)
                self.x_0 = list(map(int, file.readline().split()))  # начальная точка
                self.delta = int(file.readline())  # длина ребра симплекса
                self.alpha = float(file.readline())  # коэффициент сжатия
                self.eps_x = float(file.readline())  # точность по аргументу x
                self.eps_y = float(file.readline())  # точность по аргументу y
        elif source == "from field":
            expression = dpg.get_value('expr')
            transformations = (standard_transformations + (implicit_multiplication_application,))
            self.function: Expr = parse_expr(expression, transformations=transformations)
            self.x_0 = dpg.get_value('x_0')  # начальная точка
            self.delta = dpg.get_value('delta')  # длина ребра симплекса
            self.alpha = dpg.get_value('alpha')  # коэффициент сжатия
            self.eps_x = dpg.get_value('eps_x')  # точность по аргументу x
            self.eps_y = dpg.get_value('epx_y')  # точность по аргументу y

    def __str__(self):
        return f"{self.function=}" + f"{self.x_0=}" + f"{self.delta=}" + f"{self.alpha=}" + f"{self.eps_x=}" + f"{self.eps_y=}"

    def __repr__(self):
        print(f"{self.function=}", f"{self.x_0=}",
              f"{self.delta=}", f"{self.alpha=}", f"{self.eps_x=}", f"{self.eps_y=}", sep="\n")


def simplex_method(expr: ExpressionMin):
    function, x_0, delta, alpha, eps_x, eps_y = expr.function, expr.x_0, expr.delta, expr.alpha, expr.eps_x, expr.eps_y
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
            if row - 1 == column:
                V[row][column] = V[0][column] + p_n
            else:
                V[row][column] = V[0][column] + g_n
    print(f"{V=}")
    # начальное приближение точки минимума - геометрический центр симплекса
    x_approx_prev = [sum(V[:, i]) / (n + 1) for i in range(n)]
    print(f"{x_approx_prev=}")
    F_approx_prev = function.subs({x1: x_approx_prev[0], x2: x_approx_prev[1]})
    print(f"{F_approx_prev=}")
    while True:
        F_x = np.array([function.subs({x1: V[i][0], x2: V[i][1]}) for i in range(n + 1)])
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


def output_solution(sender, app_data, user_data):
    expr = ExpressionMin(dpg.get_value('mode'))
    print(expr)
    simplex_method(expr)


def mode(sender, app_data, user_data):
    dpg.delete_item('init', children_only=True)
    if dpg.get_value('mode') == "from file":
        dpg.add_input_text(label=":Filename", tag='filename', parent='init',
                           default_value="expr.txt")
    elif dpg.get_value('mode') == "from field":
        dpg.add_input_int(label="dimension", tag='dim', parent='init', default_value=2)

        def next_data():
            dpg.delete_item('next_sub-window', children_only=True)
            dpg.add_input_text(label=":Expression", tag='expr', parent='next_sub-window',
                               default_value="(x_1 - x_2) ** 2 + (x_1 ** 2 - x_2 + 2) ** 2")
            for i in range(dpg.get_value('dim')):
                dpg.add_input_float(label=f":initial Point #{i}", tag=f'x_{i}', parent='next_sub-window',
                                    default_value=0.0)
            dpg.add_input_float(label=":simplex edge length", tag='delta', parent='next_sub-window', default_value=1)
            dpg.add_input_float(label=":compression ratio", tag='alpha', parent='next_sub-window', default_value=0.5)
            dpg.add_input_float(label=":x precision", tag='eps_x', parent='next_sub-window', default_value=0.02)
            dpg.add_input_float(label=":y precision", tag='eps_y', parent='next_sub-window', default_value=0.001)

        dpg.add_button(label="Next", tag='next', parent='init', callback=next_data)
        dpg.add_child_window(label="Next", tag="next_sub-window", parent='init')


################################################# MAIN ################################################################
with dpg.window(label="Minimization", tag="Minimization", autosize=True):
    dpg.add_text("Choose method:")
    dpg.add_radio_button(tag='method',
                         items=["Simplex Method", "Hook Jeeves Method"], default_value="Simplex Method")
    dpg.add_text("Choose mode:")
    dpg.add_radio_button(tag='mode', horizontal=True, callback=mode,
                         items=["from file", "from field"], default_value="from field")
    dpg.add_child_window(label="initiation data", tag='init')
    dpg.add_separator(tag='preset')
    dpg.add_button(label="Search", tag='solution', callback=output_solution)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (77, 7, 143), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvInputInt):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 77, 70), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvText):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (15, 61, 131), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)
########################################################################################################################
dpg.set_global_font_scale(1.25)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Minimization", True)
dpg.start_dearpygui()
dpg.destroy_context()
