import dearpygui.dearpygui as dpg

from .food_db_tags import *
from dionysus.constants import FOOD_METADATA
from dionysus.database.database import (
    add_food,
    delete_food,
    get_food,
    search_foods,
    update_food,
)
from dionysus.state import FoodDBState


def on_search_changed(sender, app_data, user_data):
    state: FoodDBState = user_data
    state.search_filter = app_data
    refresh(state)


def refresh(state: FoodDBState):
    clear_table()
    clear_detail_panel()
    clear_edit_popup()
    populate_table(state)
    populate_detail_panel(state.selected_food_id)
    populate_delete_popup(state.selected_food_id)
    populate_edit_popup(state.selected_food_id)


def populate_table(state: FoodDBState):
    food_data = search_foods(state.search_filter)
    database_columns = ["name", *list(FOOD_METADATA["Macronutrients"])]
    for food in food_data:
        with dpg.table_row(parent=TABLE):
            for column in database_columns:
                dpg.add_selectable(label=food[column], span_columns=True, user_data=(state, food["id"]), callback=on_food_selected)


def clear_table():
    rows = dpg.get_item_children(TABLE, slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)


def clear_detail_panel():
    dpg.set_value(
        DETAIL_NAME_TEXT,
        "Select food"
    )
    for section in FOOD_METADATA:
        for nutrient, metadata in FOOD_METADATA[section].items():
            dpg.set_value(
                detail_value_text(nutrient),
                "",
            )


def clear_edit_popup():
    dpg.set_value(
        EDIT_TITLE_TEXT,
        ""
    )
    for section in FOOD_METADATA:
        for nutrient, metadata in FOOD_METADATA[section].items():
            dpg.set_value(
                edit_label_text(nutrient),
                f"{metadata["label"]}:"
            )
            dpg.set_value(
                edit_value_input(nutrient),
                0.0
            )


def populate_detail_panel(food_id):
    food_details = get_food(food_id)
    dpg.set_value(
        DETAIL_NAME_TEXT,
        food_details["name"]
    )

    for section in FOOD_METADATA:
        for nutrient, metadata in FOOD_METADATA[section].items():
            dpg.set_value(
                detail_value_text(nutrient),
                f"{metadata["label"]}: {food_details[nutrient]} {metadata["unit"]}"
            )


def populate_edit_popup(food_id):
    food_details = get_food(food_id)
    dpg.set_value(
        EDIT_TITLE_TEXT,
        food_details["name"]
    )

    for section in FOOD_METADATA:
        for nutrient, metadata in FOOD_METADATA[section].items():
            dpg.set_value(
                edit_label_text(nutrient),
                f"{metadata["label"]}:"
            )
            dpg.set_value(
                edit_value_input(nutrient),
                food_details[nutrient]
            )



def populate_delete_popup(food_id):
    food_details = get_food(food_id)
    dpg.set_value(
        DELETE_WARNING_TEXT,
        f"Are you sure you want to delete {food_details["name"]} from the database?"
    )


def on_food_selected(sender, app_data, user_data):
    state, food_id = user_data
    state.selected_food_id = food_id
    refresh(state)


def on_edit_calcel_clicked(sender, app_data, user_data):
    state: FoodDBState = user_data
    refresh(state)
    dpg.configure_item(EDIT_POPUP, show=False)


def read_edit_popup():
    new_data = {}
    for section in FOOD_METADATA:
        for nutrient in FOOD_METADATA[section]:
            new_value = dpg.get_value(edit_value_input(nutrient))
            new_data[nutrient] = new_value

    return new_data


def on_edit_save_clicked(sender, app_data, user_data):
    state: FoodDBState = user_data
    new_data = read_edit_popup()
    update_food(state.selected_food_id, new_data)
    refresh(state)
    dpg.configure_item(EDIT_POPUP, show=False)


def on_delete_confirm_clicked(sender, app_data, user_data):
    state: FoodDBState = user_data
    delete_food(state.selected_food_id)
    state.selected_food_id = None
    state.search_filter = ""

    refresh(state)
    dpg.configure_item(DELETE_POPUP, show=False)


def on_add_confirm_clicked(sender, app_data, user_data):
    state: FoodDBState = user_data
    food_data = read_add_popup()
    food_id = add_food(food_data)
    state.selected_food_id = food_id
    state.search_filter = food_data["name"]

    refresh(state)
    dpg.configure_item(ADD_POPUP, show=False)


def read_add_popup():
    food_data = {
        "name": dpg.get_value(ADD_NAME_INPUT)
    }
    for nutrient in FOOD_METADATA["Macronutrients"]:
        food_data[nutrient] = dpg.get_value(add_value_input(nutrient))

    return food_data


def on_add_cancel_clicked(sender, app_data, user_data):
    pass
