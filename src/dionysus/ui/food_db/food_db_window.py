import dearpygui.dearpygui as dpg

from dionysus.constants import FOOD_METADATA
from dionysus.state import FoodDBState

from .callbacks import (
    on_add_confirm_clicked,
    on_delete_confirm_clicked,
    on_edit_cancel_clicked,
    on_edit_save_clicked,
    on_search_changed,
    populate_table,
)
from .food_db_tags import (
    ADD_BUTTON,
    ADD_NAME_INPUT,
    ADD_POPUP,
    DELETE_POPUP,
    DELETE_WARNING_TEXT,
    DETAIL_DELETE_BUTTON,
    DETAIL_EDIT_BUTTON,
    DETAIL_NAME_TEXT,
    DETAIL_WINDOW,
    EDIT_POPUP,
    EDIT_TITLE_TEXT,
    FOOD_TABLE,
    TABLE_WINDOW,
    add_value_input,
    detail_value_text,
    edit_value_input,
)


def build_food_db_screen():
    state = FoodDBState()
    with dpg.group(horizontal=True):
        with dpg.child_window(width=900, tag=TABLE_WINDOW):
            with dpg.group(horizontal=True):
                dpg.add_text("Search food:")
                dpg.add_input_text(width=300, callback=on_search_changed, user_data=state)
                dpg.add_button(label="Add food")
                build_add_popup(state)
            build_food_table(state)
        with dpg.child_window(width=-1, tag=DETAIL_WINDOW):
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
        tag=FOOD_TABLE,
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
            tag=DETAIL_NAME_TEXT
        )
        dpg.add_button(label="Edit", tag=DETAIL_EDIT_BUTTON)
        build_edit_popup(state)
        dpg.add_button(label="Delete", tag=DETAIL_DELETE_BUTTON)
        build_delete_popup(state)

    for section in FOOD_METADATA:
        dpg.add_text(section)
        dpg.add_separator()
        with dpg.table(header_row=False):
            dpg.add_table_column()
            dpg.add_table_column()
            for nutrient, metadata in FOOD_METADATA[section].items():
                with dpg.table_row():
                    dpg.add_text(metadata["label"])
                    dpg.add_text("", tag=detail_value_text(nutrient))


def build_edit_popup(state: FoodDBState):
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag=EDIT_POPUP):
        dpg.add_text(
            "",
            tag=EDIT_TITLE_TEXT
        )
        for section in FOOD_METADATA:
            dpg.add_text(section)
            dpg.add_separator()
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                for nutrient, metadata in FOOD_METADATA[section].items():
                    with dpg.table_row():
                        dpg.add_text(metadata["label"])
                        with dpg.group(horizontal=True):
                            dpg.add_input_double(tag=edit_value_input(nutrient), step=0)
                            dpg.add_text(metadata["unit"])

        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=on_edit_save_clicked, user_data=state)
            dpg.add_button(label="Cancel", callback=on_edit_cancel_clicked, user_data=state)


def build_delete_popup(state: FoodDBState):
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag=DELETE_POPUP):
        dpg.add_text(
            "",
            tag=DELETE_WARNING_TEXT
        )
        with dpg.group(horizontal=True):
            dpg.add_button(label="Delete", user_data=state, callback=on_delete_confirm_clicked)
            dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item(DELETE_POPUP, show=False))


def build_add_popup(state: FoodDBState):
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag=ADD_POPUP):
        dpg.add_text("Please enter details below:")
        with dpg.table(header_row=False):
            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row():
                dpg.add_text("Name")
                dpg.add_input_text(tag=ADD_NAME_INPUT)

            for nutrient, metadata in FOOD_METADATA["Macronutrients"].items():
                with dpg.table_row():
                    dpg.add_text(metadata["label"])
                    with dpg.group(horizontal=True):
                        dpg.add_input_double(tag=add_value_input(nutrient), step=0)
                        dpg.add_text(metadata["unit"])

        with dpg.group(horizontal=True):
            dpg.add_button(label="Add", user_data=state, callback=on_add_confirm_clicked)
            dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item("add_food_popup", show=False))
