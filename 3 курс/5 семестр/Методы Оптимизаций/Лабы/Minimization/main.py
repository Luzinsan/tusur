import dearpygui.dearpygui as dpg
from multi import *

dpg.create_context()
dpg.create_viewport(title='Minimization', width=960, height=750)


def on_exit(sender, app_data, user_data):
    print("exit")


################################################# MAIN ################################################################
with dpg.window(label="Minimization", tag="Main", autosize=True):
    dpg.add_text("Choose mode:")
    dpg.add_radio_button(tag='mode', horizontal=True,
                         items=["from file", "from field"], default_value="from field")
    dpg.add_text("Choose method:")
    dpg.add_radio_button(tag='method',
                         items=["Simplex Method", "from field"], default_value="from field")
    dpg.add_input_text(label=":Expression|File", tag='source')
    dpg.add_button(label="Search", tag='min', callback=simplex_method)

########################################################################################################################
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
dpg.set_exit_callback(on_exit)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
