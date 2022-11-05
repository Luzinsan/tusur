from methods import *
from sympy.plotting import plot3d
dpg.create_context()


def output_solution(sender, app_data, user_data):
    expr = ExpressionMin(dpg.get_value('mode'))
    method = dpg.get_value('method')
    plot = plot3d(expr.function, (x1, dpg.get_value('x_from'), dpg.get_value('x_to')),
                          (x2, dpg.get_value('y_from'), dpg.get_value('y_to')), show=False)
    plot.save("./image.png")
    dpg.delete_item('img', children_only=True)
    dpg.delete_item('texture_tag')
    width, height, channels, data = dpg.load_image("image.png")
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
    dpg.add_image('texture_tag', parent='img')

    match method:
        case "Simplex Method":
            result = simplex_method(expr)
            print(f"\n\n\n\tКонечное решение: {result}")
            dpg.set_value('result', result)
        case "Hook Jeeves Method":
            result = hook_jeeves_method(expr)
            print(f"\n\n\n\tКонечное решение: {result}")


def mode(sender, app_data, user_data):
    dpg.delete_item('init', children_only=True)
    if dpg.get_value('mode') == "from file":
        dpg.add_input_text(label=":Filename", tag='filename', parent='init',
                           default_value="expr.txt")
    elif dpg.get_value('mode') == "from field":
        dpg.add_input_int(label="dimension", tag='dim', parent='init', default_value=2, readonly=True)

        def next_data():
            dpg.delete_item('next_sub-window', children_only=True)
            dpg.add_input_text(label=":Expression", tag='expr', parent='next_sub-window',
                               default_value="2 - (x_1**2 + x_2**2)**(1/3)")
            for i in range(dpg.get_value('dim')):
                dpg.add_input_float(label=f":coordinate #{i}", tag=f'x_{i}', parent='next_sub-window',
                                    default_value=0.0)
            dpg.add_input_float(label=":simplex edge length", tag='delta', parent='next_sub-window', default_value=1)
            dpg.add_input_float(label=":compression ratio", tag='alpha', parent='next_sub-window', default_value=0.5)
            dpg.add_input_float(label=":x precision", tag='eps_x', parent='next_sub-window', default_value=0.001)
            dpg.add_input_float(label=":y precision", tag='eps_y', parent='next_sub-window', default_value=0.001)

        dpg.add_button(label="Next", tag='next', parent='init', callback=next_data)
        dpg.add_child_window(label="Next", tag="next_sub-window", parent='init', autosize_x=True, autosize_y=True)


################################################# MAIN ################################################################
with dpg.window(label="Minimization", tag="Minimization", autosize=True):
    dpg.add_text("Choose method:")
    dpg.add_radio_button(tag='method',
                         items=["Simplex Method", "Hook Jeeves Method"], default_value="Simplex Method")
    dpg.add_text("Choose mode:")
    dpg.add_radio_button(tag='mode', horizontal=True, callback=mode,
                         items=["from file", "from field"])
    dpg.add_child_window(label="initiation data", tag='init', autosize_x=True, height=300)
    dpg.add_separator(tag='preset')
    dpg.add_child_window(label='Images', tag='img', autosize_x=True, height=500)
    with dpg.group(label='Display Plot x', tag='range_display_x', horizontal=True):
        dpg.add_input_float(label='x:from', tag='x_from', width=200, default_value=-10)
        dpg.add_input_float(label='x:to', tag='x_to', width=200, default_value=10)
    with dpg.group(label='Display Plot y', tag='range_display_y', horizontal=True):
        dpg.add_input_float(label='y:from', tag='y_from', width=200, default_value=-10)
        dpg.add_input_float(label='y:to', tag='y_to', width=200, default_value=10)

    dpg.add_button(label="Search", tag='solution', callback=output_solution)
    dpg.add_input_text(label='Solution', tag='result', readonly=True, scientific=True, default_value='coordinates')

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


########################################################################################################################
dpg.create_viewport(title='Minimization', width=960, height=750)
dpg.bind_theme(global_theme)
dpg.set_global_font_scale(1.25)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Minimization", True)
dpg.start_dearpygui()
dpg.destroy_context()
