import dearpygui.dearpygui as dpg
dpg.create_context()
dpg.create_viewport(title='Minimization', width=960, height=750)


def clipper_toggle(sender, value):
    if value:
        dpg.show_item("clipper")
        dpg.hide_item("no_clipper")
    else:
        dpg.show_item("no_clipper")
        dpg.hide_item("clipper")


with dpg.window(label="Tutorial"):
    dpg.add_checkbox(label="clipper", default_value=True, callback=clipper_toggle)
    with dpg.table(header_row=False, id="clipper"):
        for i in range(5):
            dpg.add_table_column()
        with dpg.clipper("Clipper"):
            for i in range(20000):
                with dpg.table_row():  # clipper must use table_row item
                    for j in range(5):
                        dpg.add_text(f"Row{i} Column{j}")

    with dpg.table(header_row=False, id="no_clipper", show=False):
        for i in range(5):
            dpg.add_table_column()
        for i in range(20000):
            with dpg.table_row():  # clipper must use table_row item
                for j in range(5):
                    dpg.add_text(f"Row{i} Column{j}")

dpg.show_metrics()
dpg.set_global_font_scale(1.25)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
