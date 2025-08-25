import dearpygui.dearpygui as dpg
from db import Database

db = Database("./data/food.db")

def show_dionysus():
    with dpg.font_registry():
        default_font = dpg.add_font('./assets/JetBrainsMonoNL-Regular.ttf', 18)
    with dpg.window(tag='main'):
        dpg.bind_font(default_font)
        with dpg.group(horizontal=True):
            def update_recipe_selection(sender, app_data, user_data):
                available_recipes = db.get_recipes_by_target(app_data)
                dpg.configure_item('recipe', items=available_recipes)
            def update_recipe_bounds(sender, app_data, user_data):
                dpg.delete_item('recipe_bounds', children_only=True)
                target_name=dpg.get_value('target')
                recipe_name=dpg.get_value('recipe')
                bounds = db.get_recipe_bounds(target_name, recipe_name)
                with dpg.table(header_row=True, parent='recipe_bounds', row_background=True, borders_innerV=True,
                               borders_innerH=True):
                    dpg.add_table_column(label='Food')
                    dpg.add_table_column(label='Minimum')
                    dpg.add_table_column(label='Maximum')
                    dpg.add_table_column(label='Starting amount')
                    for row in bounds:
                        with dpg.table_row():
                            dpg.add_text(row['food'])
                            dpg.add_input_text(default_value='' if row['minimum'] is None else row['minimum'], on_enter=True, decimal=True, width=50)
                            dpg.add_input_text(default_value='' if row['maximum'] is None else row['maximum'], on_enter=True, decimal=True, width=50)
                            dpg.add_input_text(default_value='' if row['starting_amount'] is None else row['starting_amount'], on_enter=True, decimal=True, width=50)

            dpg.add_text('Target:')
            target = dpg.add_combo(items=db.get_target_names(), fit_width=True, tag='target', callback=update_recipe_selection)
            dpg.add_text('Recipe:')
            recipe = dpg.add_combo(items=(), fit_width=True, tag='recipe', callback=update_recipe_bounds)

        dpg.add_separator()
        with dpg.group(tag='recipe_bounds'):
            pass
        dpg.add_separator()
        with dpg.group(tag='recipe_results'):
            pass
        


dpg.create_context()
dpg.create_viewport(title='Dionysus', width=600, height=300)

show_dionysus()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('main', True)
dpg.start_dearpygui()
dpg.destroy_context()

db.close()
