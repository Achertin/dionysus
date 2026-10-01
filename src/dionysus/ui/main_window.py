import dearpygui.dearpygui as dpg
from .calculator_window import build_calculator
from .database_window import build_food_database_window

def start_main_window():
    dpg.create_context()
    dpg.create_viewport(title='Dionysus', resizable=True)

    with dpg.window(
        tag="main_window",
        no_title_bar=True,
    ):
        dpg.set_primary_window("main_window", value=True)
        with dpg.tab_bar():
            build_calculator()
            with dpg.tab(label="Food database"):
                build_food_database_window()
            targets = dpg.add_tab(label="Targets")
            users = dpg.add_tab(label="Users")


    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
