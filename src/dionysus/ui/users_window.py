import dearpygui.dearpygui as dpg
from .users_window_callbacks import (
    populate_table
)


def build_users_window():
    with dpg.group(horizontal=True):
        with dpg.child_window(tag="users_window"):
            with dpg.group(horizontal=True):
                dpg.add_text("Search user:")
                dpg.add_input_text(width=300)
                dpg.add_button(label="Add user")
            build_users_table()
        with dpg.child_window(tag="targets_window"):
            dpg.add_text("Placeholder")


def build_users_table():
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
        display_columns = ["Name", "Age", "Sex", "Weight", "Height"]
        for column_name in display_columns:
            dpg.add_table_column(label=column_name, width_fixed=True)
        populate_table()
