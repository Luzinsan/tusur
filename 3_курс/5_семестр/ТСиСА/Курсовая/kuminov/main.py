import dearpygui.dearpygui as dpg
import numpy as np

WIDTH = 960
HEIGHT = 540
CENTER = int(WIDTH / 2) - 100

dpg.create_context()


def on_exit(sender, app_data, user_data):
    print("closed")


def check_inputs(crit):
    itsok = True
    if dpg.get_value(f'a1_crit{crit}') >= dpg.get_value(f'a2_crit{crit}'):
        dpg.set_value(f'a1_crit{crit}_except', 'Error!!!')
        itsok = False
    if dpg.get_value(f'a2_crit{crit}') >= dpg.get_value(f'a3_crit{crit}'):
        dpg.set_value(f'a2_crit{crit}_except', 'Error!!!')
        itsok = False
    return itsok


def switch_crit(sender, app_data, crit):
    if check_inputs(crit):
        dpg.configure_item(f'child{crit}', show=False)
        dpg.configure_item(f'child{crit+1}', show=True)
    # next = dpg.get_value(tag_next)
    # print(next)
    # if curr > next:
    #     dpg.add_text(default_value='Недопустимое значение', parent='gauss_param')


with dpg.window(label="Gauss Parameters", tag="gauss_param", width=WIDTH, height=HEIGHT, show=True, no_move=True, no_resize=True, modal=True):
    for i in range(2):
        with dpg.child_window(tag=f'child{i}', show=False):
            dpg.add_text(default_value=f'Параметры функции Гаусса для критерия #{i+1}', indent=CENTER-120)
            dpg.add_separator()
            # Ввод доминирующих значений
            dpg.add_text(default_value='Доминирующее значение Y нечёткого множества, описывающего терм, ai')
            with dpg.group(horizontal=False):
                for j in range(3):
                    with dpg.group(horizontal=True):
                        dpg.add_text(default_value=f'Ay{j+1}: ')
                        dpg.add_input_int(tag=f'a{j + 1}_crit{i}', default_value=0, width=150)
                        dpg.add_input_text(tag=f'a{j + 1}_crit{i}_except', default_value="exc")

            dpg.add_separator()
            # Ввод пограничных значений
            dpg.add_text(default_value='Пограничные значения соседних термов, j')
            with dpg.group(horizontal=False):
                for j in range(2):
                    with dpg.group(horizontal=True):
                        dpg.add_text(default_value=f'j{j + 1}: ')
                        dpg.add_input_int(tag=f'j{j + 1}_crit{i}', default_value=0, width=150)
                        dpg.add_input_text(tag=f'j{j + 1}_crit{i}_except', default_value="exc")
            dpg.add_separator()
            # Ввод степени разделения
            dpg.add_text(default_value='Степень принадлежности пограничных значений(степень разделения), М')
            with dpg.group(horizontal=False):
                for j in range(2):
                    with dpg.group(horizontal=True):
                        dpg.add_text(default_value=f'M{j + 1}: ')
                        dpg.add_input_int(tag=f'M{j + 1}_crit{i}', default_value=0, width=150)
                        dpg.add_input_text(tag=f'M{j + 1}_crit{i}_except', default_value="exc")
            dpg.add_button(label='Подтвердить', indent=CENTER,
                           callback=switch_crit, user_data=i)
        dpg.configure_item('child0', show=True)

with dpg.window(label="Simple Decision Support System", tag="Main"):
    # Справочная информация
    dpg.add_child_window(tag='info', height=380)
    # Ввод альтернатив
    with dpg.group(horizontal=True):
        dpg.add_text(default_value='Количество альтернатив: ')
        dpg.add_input_int(tag='alts', default_value=2, min_value=2, min_clamped=True)
    # Ввод критериев
    with dpg.group(horizontal=True):
        with dpg.group(horizontal=False):
            dpg.add_text(default_value='Название критерия #1: ')
            dpg.add_text(default_value='Название критерия #2: ')
        with dpg.group(horizontal=False):
            dpg.add_input_text(tag='crit1', default_value='Критерий #1')
            dpg.add_input_text(tag='crit2', default_value='Критерий #2')
    dpg.add_button(label='Подтвердить', indent=CENTER,
                   callback=lambda: dpg.configure_item('gauss_param', show=True))

with dpg.font_registry():
    with dpg.font(f'/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 20, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

########################################################################################################################
dpg.create_viewport(title='ГРУППОВОЕ ПАРНОЕ ОЦЕНИВАНИЕ', width=WIDTH, height=HEIGHT, resizable=False)
dpg.set_global_font_scale(1.25)
dpg.set_exit_callback(on_exit)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
