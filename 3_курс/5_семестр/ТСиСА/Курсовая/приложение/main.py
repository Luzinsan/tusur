import dearpygui.dearpygui as dpg
dpg.create_context()


def on_exit(sender, app_data, user_data):
    print("closed")


def experts():
    dpg.configure_item('expert_window', show=True)
    dpg.delete_item('expert_window', children_only=True)
    target = dpg.get_value('target')
    dpg.add_text(label="", default_value=target, parent='expert_window')
    count_expert = dpg.get_value('experts')
    print(count_expert)
    for i in range(count_expert):
        with dpg.group(horizontal=True, tag="group_role", parent='expert_window'):
            dpg.add_text(default_value=f"Роль эксперта #{i + 1}: ", parent='expert_window')
            dpg.add_input_text(label='', tag=f'role{i + 1}', parent='expert_window')



with dpg.window(label="Expert", tag="expert_window", autosize=True, show=False, modal=True):
    dpg.add_separator()


with dpg.window(label="Main", tag="Main", autosize=True):
    with dpg.group(horizontal=True, tag="group_target"):
        dpg.add_text(default_value='Введите рассматриваемую цель: ')
        dpg.add_input_text(label=" ", tag='target', default_value='у самурая нет цели, есть только путь')
    with dpg.group(horizontal=True, tag="grou_experts"):
        dpg.add_text(default_value='Выберите количество экспертов: ')
        dpg.add_input_int(label=" ", tag='experts',default_value=3)

    dpg.add_button(label="Продолжить", width=150,
                   callback=experts)
    dpg.add_child_window(tag='box', autosize_x=True, autosize_y=True)


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
dpg.create_viewport(title='DECISION MAKING', width=1200, height=920)
dpg.set_global_font_scale(1.25)
dpg.set_exit_callback(on_exit)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
