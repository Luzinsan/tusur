from config.settings import dpg, env
from models import d2l, torch
from config.utils import switch_kind, select_path
from pipline import Pipline

def pipline(data, model, trainer):
    return trainer.fit(model, data)


def get_data(sender, app_data, pipline: Pipline):
    kind = dpg.get_value('train_data')
    match kind:
        case 'Syntetic':
            setattr(pipline, 'data', 
                    d2l.SyntheticRegressionData(w=torch.tensor([2, -3.4]), b=4.2))
        case 'File':
            file_path = dpg.get_value('input_file')
            with open(file_path, 'r') as file:
                setattr(pipline, 'data', file.read())



with dpg.window(tag="Primary Window"):
    dpg.add_text("Выберите задачу:")
    with dpg.clipper():
        tasks = env.str('TASKS').split(' ')
        dpg.add_combo(items=tasks, tag='task', default_value=tasks[0])
    
    # Добавить кнопку, которая будет загружать данные для обучения
        # Добавить check'ер, который позволит загрузить 2 файла: для обучения и валидационную
        # Добавить выбор -> генерация синтетических данных для проверки модели
    dpg.add_radio_button(tag='train_data',
                         items=["File", "Syntetic"],
                         callback=switch_kind,
                         horizontal=True)
    with dpg.collapsing_header(tag='kind_data', show=True, default_open=True):
        with dpg.group(tag='Syntetic', show=False):
            dpg.add_text('Веса')
            dpg.add_input_floatx()
            dpg.add_text('Смещение')
            dpg.add_input_floatx()
        with dpg.group(tag='File', show=True, horizontal=True):
            dpg.add_input_text(tag='input_file',
                            default_value='test.txt')
            dpg.add_button(label='Select Path Manually', callback=select_path, user_data='input_file')
        
    pipline = Pipline()
    dpg.add_button(label='Подтвердить', tag='data', callback=get_data, user_data=pipline)
    
    # Добавить область, в котором будут выбираться методы
    dpg.add_text("Выберите метод:")
    with dpg.clipper():
        methods = env.str('METHODS').split(' ')
        dpg.add_combo(items=methods, tag='method', default_value=methods[0])
    
    # Добавить область, в которой будут выбираться гиперпараметры
        
    # Добавить график, на котором будет отображаться процесс обучения
        
    # Добавить кнопку, которая позволит загрузить тестовые данные
        
    # Добавит кнопку, которая позволит скачать веса модели


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()