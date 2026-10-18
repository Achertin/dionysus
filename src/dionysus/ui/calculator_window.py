import dearpygui.dearpygui as dpg


def build_calculator():
    with dpg.tab(label="Calculator"), dpg.group(horizontal=True):
        with dpg.child_window(tag="calculator_recipe"):
            dpg.add_text('test 1')
        with dpg.child_window(tag="calculator_targets"):
            dpg.add_text('test 2')
