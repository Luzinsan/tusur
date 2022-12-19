import psycopg2
from psycopg2 import Error,  sql
from contextlib import closing
from psycopg2.extras import DictCursor

import dearpygui.dearpygui as dpg

DEFAULT_USER = "postgres"
DEFAULT_PASSWORD = "52981073"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = "5432"
DEFAULT_DATABASE = "subscription"

dpg.create_context()


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
dpg.bind_theme(global_theme)

with dpg.font_registry():
    with dpg.font(f'/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 20, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")


def on_exit():
    connection, cursor = dpg.get_item_user_data('auth')
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")


dpg.set_global_font_scale(1.25)
dpg.set_exit_callback(on_exit)