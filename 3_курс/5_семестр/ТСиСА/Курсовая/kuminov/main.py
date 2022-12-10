import dearpygui.dearpygui as dpg
from gauss_expert import *

WIDTH = 960
HEIGHT = 540
CENTER = int(WIDTH / 2) - 100

dpg.create_context()

ge = GaussExpert()
print(ge.gauss_parametrs)


def on_exit(sender, app_data, user_data):
    print("closed")


def check_inputs(crit):
    itsok = True
    if dpg.get_value(f'a1_crit{crit}') >= dpg.get_value(f'a2_crit{crit}'):
        dpg.configure_item(f'a2_crit{crit}_except', show=True)
        dpg.set_value(f'a2_crit{crit}_except', 'Значение Ay2 должно быть больше значения Ay1')
        itsok = False
    if dpg.get_value(f'a2_crit{crit}') >= dpg.get_value(f'a3_crit{crit}'):
        dpg.configure_item(f'a3_crit{crit}_except', show=True)
        dpg.set_value(f'a3_crit{crit}_except', 'Значение должно быть больше Ay1 и Ay2')
        itsok = False
    if dpg.get_value(f'j1_crit{crit}') <= dpg.get_value(f'a1_crit{crit}') \
            or dpg.get_value(f'j1_crit{crit}') >= dpg.get_value(f'a2_crit{crit}'):
        dpg.configure_item(f'j1_crit{crit}_except', show=True)
        dpg.set_value(f'j1_crit{crit}_except', 'Значение должно быть между Ay1 и Ay2')
        itsok = False
    if dpg.get_value(f'j2_crit{crit}') <= dpg.get_value(f'a2_crit{crit}') \
            or dpg.get_value(f'j2_crit{crit}') >= dpg.get_value(f'a3_crit{crit}'):
        dpg.configure_item(f'j2_crit{crit}_except', show=True)
        dpg.set_value(f'j2_crit{crit}_except', 'Значение должно быть между Ay2 и Ay3')
        itsok = False
    if itsok:
        for i in range(2):
            ge.gauss_parametrs[crit]['dominant_value'][i] = dpg.get_value(f'a{i+1}_crit{crit}')
            ge.gauss_parametrs[crit]['bound_neighb'][i] = dpg.get_value(f'j{i + 1}_crit{crit}')
            ge.gauss_parametrs[crit]['membership_deg'][i] = dpg.get_value(f'M{i + 1}_crit{crit}')
        ge.gauss_parametrs[crit]['dominant_value'][2] = dpg.get_value(f'a3_crit{crit}')
    return True


def switch_crit(sender, app_data, crit):
    if check_inputs(crit):
        if crit == 0:
            dpg.delete_item(f'child{crit}')
            dpg.configure_item(f'child{crit + 1}', show=True)
        else:
            dpg.delete_item('gauss_param')
            dpg.configure_item('window_alter', show=True)
            window_alter(dpg.get_value('alts'))


def window_alter(amount_alts):
    print(ge.gauss_parametrs)
    for i in range(amount_alts):
        with dpg.group(horizontal=True, parent='group_alts'):
            dpg.add_text(default_value=f'Ввод альтернативы #{i + 1}: ')
            dpg.add_input_text(tag=f'alt{i}', default_value=f'Альтернатива #{i + 1}')


with dpg.window(label="Input Alternatives", tag="window_alter", width=WIDTH, height=HEIGHT,
                show=False, no_move=True, no_resize=True):
    # Ввод альтернатив
    dpg.add_group(horizontal=False, tag='group_alts')


with dpg.window(label="Gauss Parameters", tag="gauss_param", width=WIDTH, height=HEIGHT,
                show=True, no_move=True, no_resize=True, modal=True):
    for i in range(2):
        with dpg.child_window(tag=f'child{i}', show=False):
            dpg.add_text(default_value=f'Параметры функции Гаусса для критерия #{i + 1}', indent=CENTER - 120)
            dpg.add_separator()
            # Ввод доминирующих значений
            dpg.add_text(default_value='Доминирующее значение Y нечёткого множества, описывающего терм, ai')
            with dpg.group(horizontal=False):
                for j in range(3):
                    with dpg.group(horizontal=True):
                        dpg.add_text(default_value=f'Ay{j + 1}: ')
                        dpg.add_input_double(tag=f'a{j + 1}_crit{i}', default_value=0, width=150)
                        dpg.add_input_text(tag=f'a{j + 1}_crit{i}_except', show=False)

            dpg.add_separator()
            # Ввод пограничных значений
            dpg.add_text(default_value='Пограничные значения соседних термов, j')
            with dpg.group(horizontal=False):
                for j in range(2):
                    with dpg.group(horizontal=True):
                        dpg.add_text(default_value=f'j{j + 1}: ')
                        dpg.add_input_double(tag=f'j{j + 1}_crit{i}', default_value=0, width=150)
                        dpg.add_input_text(tag=f'j{j + 1}_crit{i}_except', show=False)
            dpg.add_separator()
            # Ввод степени разделения
            dpg.add_text(default_value='Степень принадлежности пограничных значений(степень разделения), М')
            with dpg.group(horizontal=False):
                for j in range(2):
                    with dpg.group(horizontal=True):
                        dpg.add_text(default_value=f'M{j + 1}: ')
                        dpg.add_input_double(tag=f'M{j + 1}_crit{i}', default_value=0, width=150,
                                            min_value=0.0, min_clamped=True, max_value=1.0, max_clamped=True)
                        dpg.add_input_text(tag=f'M{j + 1}_crit{i}_except', show=False)
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
