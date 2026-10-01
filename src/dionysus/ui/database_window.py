import dearpygui.dearpygui as dpg
from .database_window_callbacks import (
    on_close_food_detail,
    on_search_food, 
    populate_table
)
from dionysus.constants import FOOD_METADATA
from dionysus.state import DatabaseState


def build_food_database_window():
    with dpg.group(horizontal=True):
        with dpg.child_window(width=600):
            with dpg.group(horizontal=True):
                dpg.add_text("Search food:")
                dpg.add_input_text(width=300, callback=on_search_food)
                dpg.add_button(label="Add food")
            build_food_table()
        with dpg.child_window(width=-1):
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
        tag="food_database_table"
    ):
        display_columns = ["Name"] + [macro_nutrient["label"] for macro_nutrient in FOOD_METADATA["Macronutrients"].values()]
        for column_name in display_columns:
            dpg.add_table_column(label=column_name, width_fixed=True)
        populate_table()

def build_food_detail():
    with dpg.group(horizontal=True):
        dpg.add_text(
            "Select a food",
            tag="detail_name"
        )
        dpg.add_button(label="Edit", tag="details_edit_button")
        build_edit_modal()
        dpg.add_button(label="Delete", tag="details_delete_button")

    for section in FOOD_METADATA:
        dpg.add_text(section)
        dpg.add_separator()
        for nutrient in FOOD_METADATA[section].keys():
            dpg.add_text(
                "",
                tag=f"detail_{nutrient}"
            )


def build_edit_modal():
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag="edit_detail_popup"):
        dpg.add_text(
            "",
            tag="edit_detail_name"
        )
        for section in FOOD_METADATA:
            dpg.add_text(section)
            dpg.add_separator()
            for nutrient, metadata in FOOD_METADATA[section].items():
                with dpg.group(horizontal=True):
                    dpg.add_text(
                        "",
                        tag=f"edit_detail_{nutrient}"
                    )
                    dpg.add_input_float(tag=f"edit_detail_{nutrient}_input", step=0)
                    dpg.add_text(metadata["unit"])

        with dpg.group(horizontal=True):
            dpg.add_button(label="Save")
            dpg.add_button(label="Cancel", callback=on_close_food_detail, show=False)
