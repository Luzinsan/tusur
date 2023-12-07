import dearpygui.dearpygui as dpg


def select_path(sender, app_data, user_data):
    dpg.set_item_user_data('file_dialog', user_data)
    dpg.show_item('file_dialog')


def set_path(sender, app_data):
    tag_path = dpg.get_item_user_data('file_dialog')
    dpg.configure_item(tag_path, default_value=app_data['file_path_name'])


with dpg.file_dialog(directory_selector=False, show=False, callback=set_path, tag="file_dialog",
                     width=700, height=400, modal=True):
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255), custom_text="[Text]")
    dpg.add_file_extension(".ods", color=(0, 255, 0, 255), custom_text="[Calc]")


def switch_method(sender, method):
    dpg.hide_item('Analyzing')
    dpg.show_item('continue')
    if method == 'File':
        dpg.hide_item('Manually')
        dpg.show_item(method)
    else:
        dpg.hide_item('File')
        dpg.show_item(method)


def initialize():
    with dpg.group(horizontal=True, show=True):
        dpg.add_input_text(tag='file_grammar',
                           default_value='grammar.txt')
        dpg.add_button(label='Select file with grammar', callback=select_path, user_data='file_grammar')
    dpg.add_radio_button(tag='input_method',
                         items=["Manually", "File"],
                         callback=switch_method,
                         horizontal=True)
    with dpg.group(tag='Manually', show=False):
        dpg.add_text('Input Data')
        dpg.add_input_text(tag='Manually_text', default_value=' float   b2 , sint , int_, ds[2], int7  ; ',
                           tab_input=True, multiline=True, width=1000)

    with dpg.group(horizontal=True, show=False, tag='File'):
        dpg.add_input_text(tag='input_file',
                           default_value='test.txt')
        dpg.add_button(label='Select Path Manually', callback=select_path, user_data='input_file')
    with dpg.group(tag='Analyzing', show=False, horizontal=True):
        with dpg.group():
            dpg.add_text('Input Data')
            dpg.add_text(tag='input data', label='Input Data')
        with dpg.group():
            dpg.add_text('Output Data')
            dpg.add_text(tag='test', label='Output Data')

