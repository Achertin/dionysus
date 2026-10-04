import dearpygui.dearpygui as dpg
from dionysus.database.database import (
    add_new_food,
    delete_food,
    get_food,
    get_food_detail,
    update_food_detail
)
from dionysus.constants import FOOD_METADATA
from dionysus.state import DatabaseState


def on_search_food(sender, app_data, user_data):
    clear_table()
    state: DatabaseState = user_data
    state.search_filter = app_data
    populate_table(state)


def populate_table(state: DatabaseState):
    food_data = get_food(state.search_filter)
    database_columns = ["name"] + [column for column in FOOD_METADATA["Macronutrients"]]
    for food in food_data:
        with dpg.table_row(parent="food_database_table"):
            for column in database_columns:
                dpg.add_selectable(label=food[column], span_columns=True, user_data=(state, food["id"]), callback=on_display_food_detail)


def clear_food_detail():
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


def populate_food_detail(food_id):
    food_details = get_food_detail(food_id)
    dpg.set_value(
        "detail_name", 
        food_details["name"]
    )
    dpg.set_value(
        "edit_detail_name", 
        f"Editing: {food_details["name"]}"
    )
    dpg.set_value(
        "delete_food_warning",
        f"Are you sure you want to delete {food_details["name"]} from the database?"
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


def on_display_food_detail(sender, app_data, user_data):
    state, food_id = user_data 
    state.selected_food_id = food_id
    clear_food_detail()
    populate_food_detail(food_id)


def on_cancel_edit_detail(sender, app_data, user_data):
    state: DatabaseState = user_data
    clear_food_detail()
    populate_food_detail(state.selected_food_id)
    dpg.configure_item("edit_detail_popup", show=False)


def get_new_edit_data():
    new_data = {}
    for section in FOOD_METADATA:
        for column in FOOD_METADATA[section].keys():
            new_value = dpg.get_value(f"edit_detail_{column}_input")
            new_data[column] = new_value

    return new_data


def on_save_edit_detail(sender, app_data, user_data):
    state: DatabaseState = user_data
    new_data = get_new_edit_data()
    clear_food_detail()
    clear_table()
    update_food_detail(state.selected_food_id, new_data)
    populate_table(state)
    populate_food_detail(state.selected_food_id)
    dpg.configure_item("edit_detail_popup", show=False)


def clear_table():
    rows = dpg.get_item_children("food_database_table", slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)


def on_delete_food(sender, app_data, user_data):
    state: DatabaseState = user_data
    delete_food(state.selected_food_id)
    state.selected_food_id = None
    state.search_filter = ""

    clear_food_detail()
    clear_table()
    populate_table(state)
    dpg.configure_item("delete_food_popup", show=False)


def on_add_food(sender, app_data, user_data):
    state: DatabaseState = user_data
    food_data = get_add_food_data()
    food_id = add_new_food(food_data)
    state.selected_food_id = food_id
    state.search_filter = food_data["name"]
    clear_table()
    clear_food_detail()
    populate_table(state)
    populate_food_detail(food_id)
    dpg.configure_item("add_food_popup", show=False)


def get_add_food_data():
    food_data = {
        "name": dpg.get_value("add_food_name_input")
    }
    for column in FOOD_METADATA["Macronutrients"]:
        food_data[column] = dpg.get_value(f"add_food_{column}_input")

    return food_data



def on_cancel_add_food(sender, app_data, user_data):
    pass
