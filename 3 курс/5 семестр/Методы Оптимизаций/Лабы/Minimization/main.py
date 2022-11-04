import dearpygui.dearpygui as dpg
from multi import *

dpg.create_context()
dpg.create_viewport(title='Minimization', width=960, height=750)


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
        else:
            expression = dpg.get_value('expr')
            transformations = (standard_transformations + (implicit_multiplication_application,))
            self.function: Expr = parse_expr(expression, transformations=transformations)
            self.x_0 = dpg.get_value('x_0')  # начальная точка
            self.delta = dpg.get_value('delta')  # длина ребра симплекса
            self.alpha = dpg.get_value('alpha')  # коэффициент сжатия
            self.eps_x = dpg.get_value('eps_x')  # точность по аргументу x
            self.eps_y = dpg.get_value('epx_y')  # точность по аргументу y

    def __repr__(self):
        print(f"{self.function=}", f"{self.x_0=}",
              f"{self.delta=}", f"{self.alpha=}", f"{self.eps_x=}", f"{self.eps_y=}", sep="\n")

def output_solution(sender, app_data, user_data):
    expr = ExpressionMin(dpg.get_value('source'))
    print(expr)
    # simplex_method(expr)


def mode(sender, app_data, user_data):
    dpg.delete_item('init', children_only=True)
    if dpg.get_value('mode') == "from file":
        dpg.add_input_text(label=":Filename", tag='file', parent='init',
                           default_value="expr.txt")
    elif dpg.get_value('mode') == "from field":
        dpg.add_input_int(label="dimension", tag='dim', parent='init', default_value=2)

        def next_data():
            dpg.delete_item('next_sub-window', children_only=True)
            dpg.add_input_text(label=":Expression", tag='expr', parent='next_sub-window',
                               default_value="(x_1 - x_2) ** 2 + (x_1 ** 2 - x_2 + 2) ** 2")
            for i in range(dpg.get_value('dim')):
                dpg.add_input_float(label=f":initial Point #{i}", tag=f'x_{i}', parent='next_sub-window', default_value=0.0)
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
