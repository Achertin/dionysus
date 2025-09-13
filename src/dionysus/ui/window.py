import dearpygui.dearpygui as dpg
import dionysus.ui.callbacks as ds
from dionysus.core.state import db

def show_dionysus():
    with dpg.font_registry():
        default_font = dpg.add_font('../assets/JetBrainsMonoNL-Regular.ttf', 20)
    with dpg.window(tag='main'):
        dpg.bind_font(default_font)
        with dpg.group(tag='recipe_calculator'):
            with dpg.group(horizontal=True):
                dpg.add_text('Target:')
                dpg.add_combo(items=db.target_names(), fit_width=True, tag='target_combo', callback=ds.on_target_change)
                dpg.add_text('Recipe:')
                dpg.add_combo(fit_width=True, tag='recipe_combo', callback=ds.on_recipe_change)
                dpg.add_spacer(width=100)
                dpg.add_button(label='Copy recipe')
                with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag='copy_recipe_popup'):
                    dpg.add_text('Copying current recipe to')
                    with dpg.group(horizontal=True):
                        dpg.add_text('Target:  ')
                        dpg.add_combo(tag='copy_target')
                    with dpg.group(horizontal=True):
                        dpg.add_text('New name:')
                        dpg.add_input_text(hint='Enter new name here...', tag='copy_new_name', auto_select_all=True)
                    dpg.add_text('Warning!', show=False, tag='copy_warning', color=(251, 73, 52))
                    with dpg.group(horizontal=True):
                        dpg.add_button(label='Copy', width=75)
                        dpg.add_button(label='Cancel', width=75)
            with dpg.group(horizontal=True):
                dpg.add_text('New recipe:')
                dpg.add_input_text(hint='Recipe name...', width=250, tag='new_recipe')
                dpg.add_button(label='Add recipe')
                dpg.add_spacer(width=100)

        dpg.add_separator()
        with dpg.group(tag='recipe_bounds'):
            with dpg.table(header_row=True, row_background=True, borders_innerV=True, borders_innerH=True, tag='recipe_bounds_table', show=True):
                dpg.add_table_column(label='ingredient')
                dpg.add_table_column(label='minimum')
                dpg.add_table_column(label='maximum')
                dpg.add_table_column(label='starting amount')

        dpg.add_separator()
        with dpg.group(tag='calculation_results'):
            pass

        with dpg.collapsing_header(label='Nutritional Data'):
            with dpg.group(horizontal=True):
                dpg.add_text('Filter food:')
                dpg.add_input_text(width=500, user_data='nutritional_table', tag='nutri_filter')
            with dpg.group(tag='nutritional_data'):
                pass
