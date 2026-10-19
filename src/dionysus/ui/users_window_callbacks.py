import dearpygui.dearpygui as dpg

from dionysus.constants import FOOD_METADATA
from dionysus.database.database import get_users, get_targets, get_user_name
from dionysus.state import UsersState


def populate_users_table(state: UsersState):
    user_data = get_users(state.search_filter)
    users_columns = ["name", "age", "sex", "weight", "height"]
    for user in user_data:
        with dpg.table_row(parent="users_table"):
            for column in users_columns:
                dpg.add_selectable(label=user[column], span_columns=True, user_data=(state, user["id"]), callback=on_select_user)


def populate_targets_table(state: UsersState):
    target_data = get_targets(state.selected_user_id)
    targets_columns = ["name"] + list(FOOD_METADATA["Macronutrients"]) + ["pal"]
    for target in target_data:
        with dpg.table_row(parent="targets_table"):
            for column in targets_columns:
                dpg.add_selectable(label=target[column], span_columns=True, user_data=(state, target["id"]))


def clear_users_table():
    rows = dpg.get_item_children("users_table", slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)


def clear_targets_table():
    rows = dpg.get_item_children("targets_table", slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)


def on_search_user(sender, app_data, user_data):
    clear_users_table()
    state: UsersState = user_data
    state.search_filter = app_data
    populate_users_table(state)


def on_select_user(sender, app_data, user_data):
    clear_targets_table()
    state, user_id = user_data
    state.selected_user_id = user_id
    dpg.set_value("selected_user", get_user_name(user_id))
    populate_targets_table(state)


def on_add_user(sender, app_data, user_data):
    pass
