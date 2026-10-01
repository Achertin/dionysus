import dearpygui.dearpygui as dpg
from .database_window_callbacks import on_search_food

FOOD_DATABASE_COLUMNS = ["Name", "Energy", "Protein", 
                         "Fatty acids", "Saturated fatty acids", 
                         "Carbohydrates", "Fibre"]

def build_food_database_window():
    with dpg.group(horizontal=True):
        with dpg.child_window(label="food_database", width=550):
            with dpg.group(horizontal=True):
                dpg.add_text("Search food:")
                dpg.add_input_text(width=300, callback=on_search_food)
                dpg.add_button(label="Add food")
            build_food_table()
        with dpg.child_window(label="detailed_food_data", width=-1):
            dpg.add_text("Placeholder text")


def build_food_table():
    with dpg.table(
        header_row=True,
        row_background=True,
        borders_innerH=True,
        borders_innerV=True,
        scrollX=True,
        hideable=True,
        scrollY=True,
        freeze_rows=1,
        tag="food_database"
    ):
        for column_name in FOOD_DATABASE_COLUMNS:
            dpg.add_table_column(label=column_name, width_fixed=True)
