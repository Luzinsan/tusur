from settings import *


def insert_record():
    pass


def output_request(cursor):
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
    values = [
        ('59', '492749', 'Атомный gdf', 'Зеленогорск', 'Хорова', '46', '491'),
    ]
    insert = sql.SQL(
        'INSERT INTO t_address (id, post_code, region, city, street, house, apartment) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )
    cursor.execute(insert)
    cursor.execute("SELECT * FROM t_address;")
    print(cursor.fetchall())


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
        with closing(psycopg2.connect(user=auth_data['user'],
                                      password=auth_data['password'],
                                      host=auth_data['host'],
                                      port=auth_data['port'],
                                      database=auth_data['database'])) as connection:
            # Распечатать сведения о PostgreSQL
            print(connection.get_dsn_parameters())
            # Инициализация курсора для выполнения операций с базой данных
            cursor = connection.cursor(cursor_factory=DictCursor)
            dpg.add_text(tag='connect_success', before='send_auth', color=(0, 255, 0), default_value=f"База данных успешно подключена.")
            dpg.set_item_user_data('auth', [connection, cursor])
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
    dpg.add_separator()
dpg.set_primary_window("Main", True)


########################################################################################################################
dpg.create_viewport(title='SQL CLIENT')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()