import dearpygui.dearpygui as dpg

from .users_window_callbacks import (
    populate_users_table,
    on_search_user
)
from dionysus.state import UsersState
from dionysus.constants import USER_METADATA


def build_users_window():
    state = UsersState()
    with dpg.group(horizontal=True):
        with dpg.child_window(tag="users_window"):
            with dpg.group(horizontal=True):
                dpg.add_text("Search user:")
                dpg.add_input_text(width=200, user_data=state, callback=on_search_user)
                dpg.add_button(label="Add user")
                dpg.add_button(label="Remove user")
            build_users_table(state)
        with dpg.child_window(tag="targets_window"):
            with dpg.group(horizontal=True):
                dpg.add_text("Targets for:")
                dpg.add_text("", tag="selected_user")
                dpg.add_button(label="Add target")
                dpg.add_button(label="Remove target")
            build_targets_table(state)


def build_users_table(state: UsersState):
    with dpg.table(
        header_row=True,
        row_background=True,
        borders_innerH=True,
        borders_innerV=True,
        scrollX=True,
        hideable=True,
        scrollY=True,
        freeze_rows=1,
        tag="users_table"
    ):
        display_columns = [column_name["label"] for column_name in USER_METADATA["User Data"].values()]
        for column_name in display_columns:
            dpg.add_table_column(label=column_name, width_stretch=True)
        populate_users_table(state)


def build_targets_table(state: UsersState):
    with dpg.table(
        header_row=True,
        row_background=True,
        borders_innerH=True,
        borders_innerV=True,
        scrollX=True,
        hideable=True,
        scrollY=True,
        freeze_rows=1,
        tag="targets_table",
        resizable=True,
        policy=dpg.mvTable_SizingStretchProp
    ):
        display_columns = [column_name["label"] for column_name in USER_METADATA["Target Data"].values()]
        for column_name in display_columns:
            dpg.add_table_column(label=column_name)


def build_add_user_modal(state: UsersState):
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag="add_user_popup"):
        dpg.add_text("Adding new user")
