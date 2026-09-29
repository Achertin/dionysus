import dearpygui.dearpygui as dpg
from .calculator_window import build_calculator

def start_main_window():
    dpg.create_context()
    dpg.create_viewport(title='Dionysus', resizable=True)

    with dpg.window(
        tag="main_window",
        no_title_bar=True,
    ):
        with dpg.tab_bar():
            build_calculator()
            database = dpg.add_tab(label="Database")
            targets = dpg.add_tab(label="Targets")
            users = dpg.add_tab(label="Users")

    dpg.set_primary_window("main_window", value=True)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
