import dearpygui.dearpygui as dpg

from dionysus.constants import FOOD_METADATA
from dionysus.state import FoodDBState

from .callbacks import (
    on_add_confirm_clicked,
    on_edit_calcel_clicked,
    on_delete_confirm_clicked,
    on_edit_save_clicked,
    on_search_changed,
    populate_table,
)


def build_food_db_screen():
    state = FoodDBState()
    with dpg.group(horizontal=True):
        with dpg.child_window(width=900, tag="database_food_table"):
            with dpg.group(horizontal=True):
                dpg.add_text("Search food:")
                dpg.add_input_text(width=300, callback=on_search_changed, user_data=state)
                dpg.add_button(label="Add food")
                build_add_popup(state)
            build_food_table(state)
        with dpg.child_window(width=-1, tag="database_food_detail"):
            build_detail_panel(state)


def build_food_table(state: FoodDBState):
    with dpg.table(
        header_row=True,
        row_background=True,
        borders_innerH=True,
        borders_innerV=True,
        scrollX=True,
        hideable=True,
        scrollY=True,
        freeze_rows=1,
        tag="food_database_table",
        resizable=True,
        policy=dpg.mvTable_SizingStretchProp
    ):
        display_columns = ["Name"] + [macro_nutrient["label"] for macro_nutrient in FOOD_METADATA["Macronutrients"].values()]
        for column_name in display_columns:
            dpg.add_table_column(label=column_name)
        populate_table(state)


def build_detail_panel(state: FoodDBState):
    with dpg.group(horizontal=True):
        dpg.add_text(
            "Select a food",
            tag="detail_name"
        )
        dpg.add_button(label="Edit", tag="details_edit_button")
        build_edit_popup(state)
        dpg.add_button(label="Delete", tag="details_delete_button")
        build_delete_popup(state)

    for section in FOOD_METADATA:
        dpg.add_text(section)
        dpg.add_separator()
        for nutrient in FOOD_METADATA[section]:
            dpg.add_text(
                "",
                tag=f"detail_{nutrient}"
            )


def build_edit_popup(state: FoodDBState):
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
            dpg.add_button(label="Save", callback=on_edit_save_clicked, user_data=state)
            dpg.add_button(label="Cancel", callback=on_edit_calcel_clicked, user_data=state)


def build_delete_popup(state: FoodDBState):
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag="delete_food_popup"):
        dpg.add_text(
            "",
            tag="delete_food_warning"
        )
        with dpg.group(horizontal=True):
            dpg.add_button(label="Delete", user_data=state, callback=on_delete_confirm_clicked)
            dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item("delete_food_popup", show=False))


def build_add_popup(state: FoodDBState):
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag="add_food_popup"):
        dpg.add_text("Please enter details below:")
        with dpg.group(horizontal=True):
            dpg.add_text("Name")
            dpg.add_input_text(tag="add_food_name_input")
        for nutrient, metadata in FOOD_METADATA["Macronutrients"].items():
            with dpg.group(horizontal=True):
                dpg.add_text(metadata["label"])
                dpg.add_input_float(tag=f"add_food_{nutrient}_input", step=0)
                dpg.add_text(metadata["unit"])
        with dpg.group(horizontal=True):
            dpg.add_button(label="Add", user_data=state, callback=on_add_confirm_clicked)
            dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item("add_food_popup", show=False))
