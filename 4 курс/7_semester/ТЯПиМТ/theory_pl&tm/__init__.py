import dearpygui.dearpygui as dpg


def set_path(sender, app_data):
    dpg.set_value('file', value=app_data['file_path_name'])


with dpg.file_dialog(directory_selector=False, show=False, callback=set_path, tag="file_dialog",
                     width=700, height=400, modal=True):
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255), custom_text="[Text]")


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
    dpg.add_radio_button(tag='input_method',
                         items=["Manually", "File"],
                         callback=switch_method,
                         horizontal=True)
    dpg.add_input_text(label='Input Text', tag='Manually', show=False,
                       default_value=' float   b2 , sint , int_, ds[2], int7  ; ', multiline=True)
    with dpg.group(horizontal=True, show=False, tag='File'):
        dpg.add_input_text(tag='file',
                           default_value='test.txt')
        dpg.add_button(label='Select Path Manually', callback=lambda: dpg.show_item("file_dialog"))
    with dpg.group(tag='Analyzing', show=False, horizontal=True):
        with dpg.group():
            dpg.add_text('Input Data')
            dpg.add_text(tag='input data', label='Input Data')
        with dpg.group():
            dpg.add_text('Output Data')
            dpg.add_text(tag='test', label='Output Data')


