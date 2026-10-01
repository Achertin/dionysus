from operator import call
import dearpygui.dearpygui as dpg
from dionysus.database.database import (
    get_food,
    get_food_detail
)
from dionysus.constants import FOOD_METADATA


def on_search_food(sender, app_data, user_data):
    clear_database_table()
    populate_table(app_data)


def populate_table(filter=""):
    food_data = get_food(filter)
    database_columns = ["name"] + [column for column in FOOD_METADATA["Macronutrients"]]
    for food in food_data:
        with dpg.table_row(parent="food_database_table"):
            for column in database_columns:
                dpg.add_selectable(label=food[column], span_columns=True, user_data=food["id"], callback=on_display_food_detail)


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


def on_display_food_detail(sender, app_data, user_data):
    clear_food_detail()
    populate_food_detail(user_data)

def on_close_food_detail(sender, app_data, user_data):
    clear_food_detail()
    dpg.configure_item("edit_details_popup", show=False)


def clear_database_table():
    rows = dpg.get_item_children("food_database_table", slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)
