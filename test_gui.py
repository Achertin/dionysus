import dearpygui.dearpygui as dpg

def show_dionysus():
    with dpg.window(tag="main"):
        with dpg.group():
            dpg.add_text("Hello world!")

dpg.create_context()
dpg.create_viewport(title='Dionysus', width=600, height=300)

show_dionysus()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()
