import dearpygui.dearpygui as dpg
from .database_window_callbacks import on_search_food
from dionysus.constants import FOOD_METADATA


def build_food_database_window():
    with dpg.group(horizontal=True):
        with dpg.child_window(label="food_database", width=600):
            with dpg.group(horizontal=True):
                dpg.add_text("Search food:")
                dpg.add_input_text(width=300, callback=on_search_food)
                dpg.add_button(label="Add food")
            build_food_table()
        with dpg.child_window(label="detailed_food_data", width=-1):
            build_food_detail()


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
        display_columns = ["Name"] + [macro_nutrient["label"] for macro_nutrient in FOOD_METADATA["Macronutrients"].values()]
        for column_name in display_columns:
            dpg.add_table_column(label=column_name, width_fixed=True)


def build_food_detail():
    dpg.add_text(
        "Select a food",
        tag="detail_name"
    )

    for section in FOOD_METADATA:
        dpg.add_text(section)
        dpg.add_separator()
        for nutrient in FOOD_METADATA[section].keys():
            dpg.add_text(
                "",
                tag=f"detail_{nutrient}"
            )
