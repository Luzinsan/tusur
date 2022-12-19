from settings import *


def insert_record():

    # values = [
    #     ('59', '492749', 'Атомный gdf', 'Зеленогорск', 'Хорова', '46', '491'),
    # ]
    # insert = sql.SQL(
    #     'INSERT INTO t_address (id, post_code, region, city, street, house, apartment) VALUES {}').format(
    #     sql.SQL(',').join(map(sql.Literal, values))
    # )
    # cursor.execute(insert)
    # cursor.execute("SELECT * FROM t_address;")
    # print(cursor.fetchall())
    pass


def send_request():
    # region Выполнение SQL-запроса
    # pubname = "Миниатюрные говорящие ослы"
    # cursor.execute("SELECT fio as Подписчики "
    #                "FROM t_subs "
    #                "JOIN t_publishing on idpub=id "
    #                "JOIN t_pod on t_subs.idpod=t_pod.id "
    #                "WHERE pubname=%s;", (pubname, ))
    # последовательный вывод данных
    # print(cursor.fetchall())
    # for row in cursor:
    #     print(row[:])
    # endregion
    # values = [
    #     ('59', '492749', 'Атомный gdf', 'Зеленогорск', 'Хорова', '46', '491'),
    # ]
    # insert = sql.SQL(
    #     'INSERT INTO t_address (id, post_code, region, city, street, house, apartment) VALUES {}').format(
    #     sql.SQL(',').join(map(sql.Literal, values))
    # )
    # cursor.execute(insert)
    # cursor.execute("SELECT * FROM t_address;")
    # print(cursor.fetchall())
    pass


def output_records(table_name, list_columns):
    connection, cursor = dpg.get_item_user_data('auth')
    dpg.delete_item('output_records_error')
    dpg.delete_item('table_records', children_only=True)
    try:
        request = f"SELECT * FROM {table_name};"
        cursor.execute(request)
        list_info_records = cursor.fetchall()
        print(f"Записи таблицы: \n{list_info_records}")
        try:
            for column in list_columns:
                dpg.add_table_column(label=column, parent='table_records')
            amount_columns = len(list_columns)
            for row in list_info_records:
                with dpg.table_row(parent='table_records'):
                    for field in row:
                        dpg.add_text(default_value=field)

            # dpg.configure_item('list_records', items=list_records, show=True, num_items=len(list_records))
            # print(f"Таблица: {list_records}")
        except (Exception, Error) as error:
            print(Error)

    except (Exception, Error) as error:
        dpg.add_text(tag='output_records_error', default_value=Error, color=(255, 0, 0), before='list_records')


def set_fields(list_columns, list_info_columns):
    dpg.delete_item('box_input_fields', children_only=True)
    with dpg.group(parent='box_input_fields'):
        for number, field in enumerate(list_columns):
            if list_info_columns[number][1] == 'integer':
                    dpg.add_input_int()
            else:
               dpg.add_input_text(hint=field)


def output_columns(sender, table_name):
    connection, cursor = dpg.get_item_user_data('auth')
    dpg.delete_item('output_columns_error')
    try:

        request = f"SELECT column_name, data_type, column_default, is_nullable, character_maximum_length  FROM information_schema.columns WHERE table_name='{table_name}';"
        cursor.execute(request)
        list_info_columns = cursor.fetchall()
        print(list_info_columns)
        list_columns = [column[0] for column in list_info_columns]
        dpg.configure_item('list_columns', items=list_columns, show=True, num_items=len(list_columns))
        print(f"Поля таблицы: {list_columns}")
        set_fields(list_columns, list_info_columns)
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
        dpg.add_text(tag='connect_success', before='send_auth', color=(0, 255, 0), default_value=f"База данных успешно подключена.")
        dpg.set_item_user_data('auth', [connection, cursor])
        output_tables(cursor)
    except (Exception, Error) as error:
        dpg.add_text(tag='connect_error', before='send_auth', color=(255, 0, 0), default_value=f"Ошибка при работе с PostgreSQL: {error}")


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
    dpg.add_listbox(tag='list_tables', callback=output_columns)
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_listbox(tag='list_columns')
        dpg.add_group(tag='box_input_fields')
    dpg.add_button(label='Добавить запись', callback=send_request)
    dpg.add_separator()
    dpg.add_table(tag='table_records')
    dpg.add_separator()
dpg.set_primary_window("Main", True)


########################################################################################################################
dpg.create_viewport(title='SQL CLIENT')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()