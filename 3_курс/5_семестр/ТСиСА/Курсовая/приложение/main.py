import dearpygui.dearpygui as dpg
import numpy as np
dpg.create_context()


def on_exit(sender, app_data, user_data):
    print("closed")


estimates = np.array([1, 1, 1])


def switch_expert(sender, app_data, expert_data):
    # expert_data = [number_of_expert, count_of_alternatives, count_of_experts]
    dpg.configure_item(f'evaluation{expert_data[0]}', show=False)
    for i in range(expert_data[1]):
        for j in range(expert_data[1]):
            estimates[expert_data[0]][i][j] = dpg.get_value(f'mark{expert_data[0]}{i}{j}')
    if expert_data[0] + 1 != expert_data[2]:
        dpg.configure_item(f'evaluation{expert_data[0]+1}', show=True)


def experts():
    dpg.delete_item('expert_window', children_only=True)
    dpg.configure_item('expert_window', show=True)
    with dpg.group(horizontal=True, tag="group_target_const", parent='expert_window'):
        dpg.add_text(default_value=f"ЦЕЛЬ: ")
        dpg.add_input_text(readonly=True, default_value=dpg.get_value('target'))
    count_expert = dpg.get_value('experts')
    count_alternatives = dpg.get_value('alternatives')
    alternatives = []
    for i in range(count_alternatives):
        alternatives.append(dpg.get_value(f'alter_text{i}'))

    dpg.add_listbox(tag='list_alternatives', items=alternatives, parent='expert_window',
                    tracked=True, width=1920, num_items=count_alternatives)
    estimates.resize([count_expert, count_alternatives, count_alternatives])
    for i in range(count_expert):
        with dpg.child_window(tag=f'evaluation{i}', parent='expert_window', height=720, width=1920, show=False):
            with dpg.group(horizontal=True, tag=f"group_role{i}"):
                dpg.add_text(default_value=f"Роль эксперта #{i}: ")
                dpg.add_input_text(tag=f'role{i}')
            # табличка с альтернативами
            with dpg.table(tag=f'table{i}',
                           header_row=True, row_background=True,
                           resizable=True, policy=dpg.mvTable_SizingStretchProp,
                           borders_innerH=True, borders_outerH=True, borders_innerV=True,
                           borders_outerV=True):
                dpg.add_table_column(label=' ', tag=f'col{i}')
                for j in range(0, count_alternatives):
                    dpg.add_table_column(label=f'Alternative #{j+1}', tag=f'col{i}{j}')

                for j in range(0, count_alternatives):
                    with dpg.table_row():
                        dpg.add_text(default_value=f'Alternative #{j+1}', tag=f'row{i}{j}')
                        for k in range(0, count_alternatives):
                            dpg.add_input_int(tag=f'mark{i}{j}{k}',
                                              min_value=0, max_value=1,
                                              min_clamped=True, max_clamped=True)
            # Переход к другому эксперту
            dpg.add_button(label=f"Перейти к эксперту #{i + 1}", tag=f'next{i+1}',
                           callback=switch_expert, user_data=[i, count_alternatives, count_expert])
    dpg.configure_item('evaluation1', show=True)


def add_alternatives():
    dpg.delete_item('alternatives_window', children_only=True)
    for i in range(dpg.get_value('alternatives')):
        dpg.add_input_text(tag=f'alter_text{i}', multiline=True,
                           default_value=f'Альтернатива решения #{i + 1}',
                           height=50, parent='alternatives_window')


with dpg.window(label="Expert", tag="expert_window", autosize=True, show=False, modal=True, width=1920):
    dpg.add_separator()


with dpg.window(label="Main", tag="Main", autosize=True):
    with dpg.group(horizontal=True, tag="group_target"):
        dpg.add_text(default_value='Введите рассматриваемую цель: ')
        dpg.add_input_text(label=" ", tag='target', default_value='у самурая нет цели, есть только путь')
    with dpg.group(horizontal=True, tag="group_experts"):
        dpg.add_text(default_value='Выберите количество экспертов: ')
        dpg.add_input_int(label=" ", tag='experts', default_value=3)
    with dpg.group(horizontal=True, tag="group_alternatives"):
        dpg.add_text(default_value='Выберите количество альтернатив: ')
        dpg.add_input_int(label=" ", tag='alternatives', default_value=5)

    dpg.add_button(label="Ввести альтернативы", width=150, callback=add_alternatives)
    dpg.add_child_window(tag='alternatives_window')
    dpg.add_button(label="Продолжить", tag='expert_button', width=150, callback=experts)


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

with dpg.font_registry():
    with dpg.font(f'/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 20, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

dpg.bind_theme(global_theme)
########################################################################################################################
dpg.create_viewport(title='DECISION MAKING', width=1920, height=920)
dpg.set_global_font_scale(1.25)
dpg.set_exit_callback(on_exit)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
