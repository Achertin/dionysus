import dearpygui.dearpygui as dpg
from .database_window_callbacks import (
    on_add_food,
    on_cancel_edit_detail,
    on_delete_food,
    on_save_edit_detail,
    on_search_food, 
    populate_table
)
from dionysus.constants import FOOD_METADATA
from dionysus.state import DatabaseState


def build_food_database_window():
    state = DatabaseState()
    with dpg.group(horizontal=True):
        with dpg.child_window(width=900):
            with dpg.group(horizontal=True):
                dpg.add_text("Search food:")
                dpg.add_input_text(width=300, callback=on_search_food, user_data=state)
                dpg.add_button(label="Add food")
                build_add_food_modal(state)
            build_food_table(state)
        with dpg.child_window(width=-1):
            build_food_detail(state)


def build_food_table(state: DatabaseState):
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
        populate_table(state)


def build_food_detail(state: DatabaseState):
    with dpg.group(horizontal=True):
        dpg.add_text(
            "Select a food",
            tag="detail_name"
        )
        dpg.add_button(label="Edit", tag="details_edit_button")
        build_edit_modal(state)
        dpg.add_button(label="Delete", tag="details_delete_button")
        build_delete_modal(state)

    for section in FOOD_METADATA:
        dpg.add_text(section)
        dpg.add_separator()
        for nutrient in FOOD_METADATA[section].keys():
            dpg.add_text(
                "",
                tag=f"detail_{nutrient}"
            )


def build_edit_modal(state: DatabaseState):
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
            dpg.add_button(label="Save", callback=on_save_edit_detail, user_data=state)
            dpg.add_button(label="Cancel", callback=on_cancel_edit_detail, user_data=state)


def build_delete_modal(state: DatabaseState):
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag="delete_food_popup"):
        dpg.add_text(
            "",
            tag="delete_food_warning"
        )
        with dpg.group(horizontal=True):
            dpg.add_button(label="Delete", user_data=state, callback=on_delete_food)
            dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item("delete_food_popup", show=False))


def build_add_food_modal(state: DatabaseState):
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag="add_food_popup"):
        dpg.add_text("Please enter details below:")
        with dpg.group(horizontal=True):
            dpg.add_text("Name")
            dpg.add_input_text(tag=f"add_food_name_input")
        for nutrient, metadata in FOOD_METADATA["Macronutrients"].items():
            with dpg.group(horizontal=True):
                dpg.add_text(metadata["label"])
                dpg.add_input_float(tag=f"add_food_{nutrient}_input", step=0)
                dpg.add_text(metadata["unit"])
        with dpg.group(horizontal=True):
            dpg.add_button(label="Add", user_data=state, callback=on_add_food)
            dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item("add_food_popup", show=False))
