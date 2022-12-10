import dearpygui.dearpygui as dpg
import numpy as np

dpg.create_context()


def on_exit(sender, app_data, user_data):
    print("closed")


with dpg.window(label="Main", tag="Main", autosize=True):
    with dpg.group(horizontal=True, tag="group_target"):
        dpg.add_text(default_value='Количество альтернатив: ')
        dpg.add_input_int(label=" ", tag='target', default_value=2)


with dpg.font_registry():
    with dpg.font(f'/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 20, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

########################################################################################################################
dpg.create_viewport(title='ГРУППОВОЕ ПАРНОЕ ОЦЕНИВАНИЕ', width=1920, height=920)
dpg.set_global_font_scale(1.25)
dpg.set_exit_callback(on_exit)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
