from . import dpg

def select_path(sender, app_data, user_data):
    dpg.set_item_user_data('file_dialog', user_data)
    dpg.show_item('file_dialog')


def set_path(sender, app_data):
    tag_path = dpg.get_item_user_data('file_dialog')
    dpg.configure_item(tag_path, default_value=app_data['file_path_name'])


with dpg.file_dialog(directory_selector=False, show=False, callback=set_path, tag="file_dialog",
                     width=700, height=400, modal=True):
    dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[CSV]")
    dpg.add_file_extension(".xlsx", color=(0, 255, 0, 255), custom_text="[Excel]")


def switch_kind(sender, kind):
    match kind:
        case 'Syntetic':
            dpg.hide_item('File')
            dpg.show_item('Syntetic')
        case 'File':
            dpg.hide_item('Syntetic')
            dpg.show_item('File')