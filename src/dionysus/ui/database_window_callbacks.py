from operator import call
import dearpygui.dearpygui as dpg
from dionysus.database.database import (
    get_food,
    get_food_details
)
from dionysus.constants import FOOD_METADATA


def on_search_food(sender, app_data, user_data):
    clear_database_table()
    food_data = get_food(app_data)
    database_columns = ["name"] + [column for column in FOOD_METADATA["Macronutrients"]]
    for food in food_data:
        with dpg.table_row(parent="food_database"):
            for column in database_columns:
                dpg.add_selectable(label=food[column], span_columns=True, user_data=food["id"], callback=on_display_food_detail)


def on_display_food_detail(sender, app_data, user_data):
    food_details = get_food_details(user_data)
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


def clear_database_table():
    rows = dpg.get_item_children("food_database", slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)
