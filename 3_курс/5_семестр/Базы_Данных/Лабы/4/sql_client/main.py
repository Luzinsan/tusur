from settings import *


def print_psycopg2_exception(err, obj):
    # dpg.delete_item('error')
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno
    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")
    # dpg.add_text(tag='error', default_value=f"gf", color=(255, 0, 0), before=obj)


def task_request():
    connection, cursor = dpg.get_item_user_data('auth')
    dpg.delete_item('task_error')
    try:
        request = f"SELECT street, house, apartment, fio " \
                  f"FROM t_subs " \
                  f"JOIN t_pod on t_pod.id=t_subs.idpod " \
                  f"JOIN t_address on t_address.id=t_pod.idaddr " \
                  f"GROUP BY street, house, apartment, fio;"
        cursor.execute(request)
        answer = cursor.fetchall()
        print(f"Таблица по заданию: {answer}")

        for column in ['Улица', 'Дом', 'Квартира\\Офис', 'ФИО']:
            dpg.add_table_column(label=column, parent='task_table')

        for row in answer:
            with dpg.table_row(parent='task_table'):
                for field in row:
                    dpg.add_text(default_value=field, color=(150, 30, 200))
    except Exception as err:
        # print_psycopg2_exception(err, 'task_table')
        dpg.add_text(tag='task_error', default_value=Error, color=(255, 0, 0), before='task_table')


def send_request():
    connection, cursor = dpg.get_item_user_data('auth')
    print(connection, cursor)
    list_columns = dpg.get_item_user_data('list_columns')
    values = []
    dpg.delete_item('success_insert')
    dpg.delete_item('insert_error')
    try:
        for field in list_columns:
            values.append(dpg.get_value(f"{field}"))
        values = tuple(values)
        print(values)
        table_name = dpg.get_item_user_data('list_tables')
        column_names = ', '.join(list_columns)
        insert = f"INSERT INTO {table_name}({column_names}) VALUES {values};"
        print(insert)
        cursor.execute(insert)
        connection.commit()
        dpg.add_text(tag='success_insert', default_value=f"Строка {values} успешно вставлена",
                     color=(0, 255, 0), before='table_records')

        with dpg.table_row(parent='table_records'):
            for value in values:
                dpg.add_text(default_value=value)
    except OperationalError as err:
        dpg.add_text(tag='insert_error', default_value=Error, color=(255, 0, 0), before='task_table')


def output_records(table_name, list_columns):
    connection, cursor = dpg.get_item_user_data('auth')
    dpg.delete_item('output_records_error')
    dpg.delete_item('table_records', children_only=True)
    try:
        request = f"SELECT * FROM {table_name};"
        cursor.execute(request)
        list_info_records = cursor.fetchall()
        print(f"Записи таблицы: \n{list_info_records}")
        for column in list_columns:
            dpg.add_table_column(label=column, parent='table_records')

        for row in list_info_records:
            with dpg.table_row(parent='table_records'):
                for field in row:
                    dpg.add_text(default_value=field)
        # dpg.configure_item('list_records', items=list_records, show=True, num_items=len(list_records))
        # print(f"Таблица: {list_records}")
    except (Exception, Error) as error:
        dpg.add_text(tag='output_records_error', default_value=Error, color=(255, 0, 0), before='list_records')


def add_fields(list_columns, list_info_columns):
    dpg.delete_item('box_input_fields', children_only=True)
    with dpg.group(parent='box_input_fields'):
        for number, field in enumerate(list_columns):
            if list_info_columns[number][1] == 'integer':
                dpg.add_input_int(tag=field)
            else:
                dpg.add_input_text(tag=field, hint=field)


def output_columns(sender, table_name):
    dpg.configure_item('list_tables', user_data=table_name)
    connection, cursor = dpg.get_item_user_data('auth')
    dpg.delete_item('output_columns_error')
    try:

        request = f"SELECT column_name, data_type, column_default, is_nullable, character_maximum_length  FROM information_schema.columns WHERE table_name='{table_name}';"
        cursor.execute(request)
        list_info_columns = cursor.fetchall()
        print(list_info_columns)
        list_columns = [column[0] for column in list_info_columns]
        dpg.configure_item('list_columns', items=list_columns, show=True,
                           num_items=len(list_columns), user_data=list_columns)
        dpg.configure_item('insert_button', show=True)
        print(f"Поля таблицы: {list_columns}")
        add_fields(list_columns, list_info_columns)
        output_records(table_name, list_columns)
    except (Exception, Error) as error:
        dpg.add_text(tag='output_columns_error', default_value=Error, color=(255, 0, 0), before='list_columns')


def output_tables(cursor):
    dpg.delete_item('output_list_error')
    try:
        request = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        cursor.execute(request)
        tables = [table[0] for table in cursor.fetchall()]
        dpg.configure_item('list_tables', items=tables, show=True, num_items=len(tables))
        print(f"Таблицы в базе данных: {tables}")
    except (Exception, Error) as error:
        dpg.add_text(tag='output_list_error', default_value=Error, color=(255, 0, 0), before='list_tables')


def connect_database():
    dpg.delete_item('connect_error')
    dpg.delete_item('connect_success')
    auth_data = {'user': dpg.get_value('user'),
                 'password': dpg.get_value('password'),
                 'host': dpg.get_value('host'),
                 'port': dpg.get_value('port'),
                 'database': dpg.get_value('database')}
    try:
        # Подключение к существующей базе данных с использованием контекстного менеджера
        connection = psycopg2.connect(user=auth_data['user'],
                                      password=auth_data['password'],
                                      host=auth_data['host'],
                                      port=auth_data['port'],
                                      database=auth_data['database'])
        # Распечатать сведения о PostgreSQL
        print(connection.get_dsn_parameters())
        # Инициализация курсора для выполнения операций с базой данных
        cursor = connection.cursor(cursor_factory=DictCursor)
        dpg.add_text(tag='connect_success', before='send_auth', color=(0, 255, 0),
                     default_value=f"База данных успешно подключена.")
        dpg.set_item_user_data('auth', [connection, cursor])
        dpg.configure_item('label_database', default_value=f"Список таблиц базы данных: {auth_data['database']}",
                           show=True)
        dpg.configure_item('task_button', show=True)
        output_tables(cursor)
    except (Exception, Error) as error:
        dpg.add_text(tag='connect_error', before='send_auth', color=(255, 0, 0),
                     default_value=f"Ошибка при работе с PostgreSQL: {error}")


############################################# AUTHORIZATION ############################################################
with dpg.window(label="AUTHORIZATION", modal=True, show=False, tag="auth", no_title_bar=True, autosize=True):
    dpg.add_input_text(label=":USER", tag='user', default_value=DEFAULT_USER)
    dpg.add_input_text(label=":PASSWORD", tag='password', default_value=DEFAULT_PASSWORD, password=True)
    dpg.add_separator(tag='sep')
    dpg.add_input_text(label=":HOST", tag='host', default_value=DEFAULT_HOST)
    dpg.add_input_text(label=":PORT", tag='port', default_value=DEFAULT_PORT)
    dpg.add_input_text(label=":DATABASE", tag='database', default_value=DEFAULT_DATABASE)
    with dpg.group(horizontal=True, tag='send_auth'):
        dpg.add_button(label="Connect", width=75, callback=connect_database)
        dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("auth", show=False))
########################################################################################################################


with dpg.window(label="Main", tag="Main"):
    with dpg.menu_bar():
        dpg.add_menu_item(label="Log in", callback=lambda: dpg.configure_item("auth", show=True))
    dpg.add_text(tag='label_database', default_value='Список таблиц базы данных: ', show=False, color=(170, 4, 170))
    dpg.add_listbox(tag='list_tables', callback=output_columns, show=False)
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_listbox(tag='list_columns', show=False)
        dpg.add_group(tag='box_input_fields')
    dpg.add_button(tag='insert_button', label='Добавить запись', callback=send_request, show=False)
    dpg.add_separator()

    dpg.add_table(tag='table_records', row_background=True,
                  resizable=True, policy=dpg.mvTable_SizingStretchProp,
                  borders_innerH=True, borders_outerH=True, borders_innerV=True,
                  borders_outerV=True)
    dpg.add_separator()
    dpg.add_button(tag='task_button', label="Вывод таблицы по заданию", callback=task_request, show=False)
    dpg.add_table(tag='task_table', row_background=True,
                  resizable=True, policy=dpg.mvTable_SizingStretchProp,
                  borders_innerH=True, borders_outerH=True, borders_innerV=True,
                  borders_outerV=True)
dpg.set_primary_window("Main", True)

########################################################################################################################
dpg.create_viewport(title='SQL CLIENT')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
