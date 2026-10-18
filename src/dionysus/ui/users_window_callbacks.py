import dearpygui.dearpygui as dpg

from dionysus.database.database import get_users
from dionysus.state import UsersState


def populate_table(state: UsersState):
    user_data = get_users(state.search_filter)
    users_columns = ["name", "age", "sex", "weight", "height"]
    for user in user_data:
        with dpg.table_row(parent="users_table"):
            for column in users_columns:
                dpg.add_selectable(label=user[column], span_columns=True, user_data=user["id"])


def clear_table():
    rows = dpg.get_item_children("users_table", slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)


def on_search_user(sender, app_data, user_data):
    clear_table()
    state: UsersState = user_data
    state.search_filter = app_data
    populate_table(state)


def on_add_user(sender, app_data, user_data):
    pass
