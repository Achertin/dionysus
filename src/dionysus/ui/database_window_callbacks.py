import dearpygui.dearpygui as dpg
from dionysus.database.database import get_food

DISPLAY_COLUMNS = ["name", "energy", "protein", 
                   "fatty_acids", "saturated_fatty_acids", 
                   "carbohydrates", "fibre"]

def on_search_food(sender, app_data, user_data):
    clear_database_table()
    food_data = get_food(app_data)

    for food in food_data:
        with dpg.table_row(parent="food_database", user_data=food["id"]):
            for column in DISPLAY_COLUMNS:
                dpg.add_text(food[column])

def clear_database_table():
    rows = dpg.get_item_children("food_database", slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)
