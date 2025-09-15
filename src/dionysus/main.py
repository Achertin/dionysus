import dearpygui.dearpygui as dpg
from dionysus.core.state import db
from dionysus.ui.window import show_dionysus

def main():
    dpg.create_context()
    dpg.create_viewport(title='Dionysus', width=600, height=300)

    show_dionysus()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window('main', True)
    dpg.start_dearpygui()
    dpg.destroy_context()

    db.close()

if __name__ == '__main__':
    main()
