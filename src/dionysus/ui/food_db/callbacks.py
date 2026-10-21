import dearpygui.dearpygui as dpg

from dionysus.constants import FOOD_METADATA
from dionysus.database.database import (
    add_food,
    delete_food,
    search_foods,
    get_food,
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
    populate_table(state)
    populate_detail_panel(state.selected_food_id)
    populate_delete_popup(state.selected_food_id)
    populate_edit_popup(state.selected_food_id)


def populate_table(state: FoodDBState):
    food_data = search_foods(state.search_filter)
    database_columns = ["name"] + list(FOOD_METADATA["Macronutrients"])
    for food in food_data:
        with dpg.table_row(parent="food_database_table"):
            for column in database_columns:
                dpg.add_selectable(label=food[column], span_columns=True, user_data=(state, food["id"]), callback=on_food_selected)


def clear_table():
    rows = dpg.get_item_children("food_database_table", slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)


def clear_detail_panel():
    dpg.set_value(
        "detail_name",
        "Select food"
    )
    dpg.set_value(
        "edit_detail_name",
        ""
    )
    for section in FOOD_METADATA:
        for column, metadata in FOOD_METADATA[section].items():
            dpg.set_value(
                f"detail_{column}",
                "",
            )
            dpg.set_value(
                f"edit_detail_{column}",
                f"{metadata["label"]}:"
            )
            dpg.set_value(
                f"edit_detail_{column}_input",
                0.0
            )


def populate_detail_panel(food_id):
    food_details = get_food(food_id)
    dpg.set_value(
        "detail_name",
        food_details["name"]
    )

    for section in FOOD_METADATA:
        for column, metadata in FOOD_METADATA[section].items():
            dpg.set_value(
                f"detail_{column}",
                f"{metadata["label"]}: {food_details[column]} {metadata["unit"]}"
            )
            dpg.set_value(
                f"edit_detail_{column}",
                f"{metadata["label"]}:"
            )
            dpg.set_value(
                f"edit_detail_{column}_input",
                food_details[column]
            )


def populate_edit_popup(food_id):
    food_details = get_food(food_id)
    dpg.set_value(
        "edit_detail_name",
        food_details["name"]
    )


def populate_delete_popup(food_id):
    food_details = get_food(food_id)
    dpg.set_value(
        "delete_food_warning",
        f"Are you sure you want to delete {food_details["name"]} from the database?"
    )


def on_food_selected(sender, app_data, user_data):
    state, food_id = user_data
    state.selected_food_id = food_id
    refresh(state)


def on_edit_calcel_clicked(sender, app_data, user_data):
    state: FoodDBState = user_data
    refresh(state)
    dpg.configure_item("edit_detail_popup", show=False)


def read_edit_popup():
    new_data = {}
    for section in FOOD_METADATA:
        for column in FOOD_METADATA[section]:
            new_value = dpg.get_value(f"edit_detail_{column}_input")
            new_data[column] = new_value

    return new_data


def on_edit_save_clicked(sender, app_data, user_data):
    state: FoodDBState = user_data
    new_data = read_edit_popup()
    update_food(state.selected_food_id, new_data)
    refresh(state)
    dpg.configure_item("edit_detail_popup", show=False)


def on_delete_confirm_clicked(sender, app_data, user_data):
    state: FoodDBState = user_data
    delete_food(state.selected_food_id)
    state.selected_food_id = None
    state.search_filter = ""

    refresh(state)
    dpg.configure_item("delete_food_popup", show=False)


def on_add_confirm_clicked(sender, app_data, user_data):
    state: FoodDBState = user_data
    food_data = read_add_popup()
    food_id = add_food(food_data)
    state.selected_food_id = food_id
    state.search_filter = food_data["name"]

    refresh(state)
    dpg.configure_item("add_food_popup", show=False)


def read_add_popup():
    food_data = {
        "name": dpg.get_value("add_food_name_input")
    }
    for column in FOOD_METADATA["Macronutrients"]:
        food_data[column] = dpg.get_value(f"add_food_{column}_input")

    return food_data


def on_add_cancel_clicked(sender, app_data, user_data):
    pass
