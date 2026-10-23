import dearpygui.dearpygui as dpg

from .calculator_window import build_calculator
from .food_db.food_db_window import build_food_db_screen
from .food_db.food_db_tags import TABLE_WINDOW, DETAIL_WINDOW
from .users.users_window import build_users_window


def start_main_window():
    dpg.create_context()
    dpg.create_viewport(title='Dionysus', resizable=True)
    dpg.set_viewport_resize_callback(on_viewport_change)

    with dpg.window(
        tag="main_window",
        no_title_bar=True,
    ):
        dpg.set_primary_window("main_window", value=True)
        with dpg.tab_bar():
            build_calculator()
            with dpg.tab(label="Food database"):
                build_food_db_screen()
            with dpg.tab(label="Users & Targets"):
                build_users_window()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def on_viewport_change():
    main_window_width = dpg.get_item_width("main_window")
    assert main_window_width is not None
    set_ratio_width(TABLE_WINDOW, DETAIL_WINDOW, main_window_width, 0.6)
    set_ratio_width("users_window", "targets_window", main_window_width, 0.5)

def set_ratio_width(tag1, tag2, main_window_width, ratio):
    window_one_width = int(main_window_width * ratio)
    window_two_width = main_window_width - window_one_width
    dpg.set_item_width(tag1, window_one_width)
    dpg.set_item_width(tag2, window_two_width)
