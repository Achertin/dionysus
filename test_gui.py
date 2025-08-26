from operator import call
import dearpygui.dearpygui as dpg
from db import Database

db = Database("./data/test_db.db")

def update_minimum(sender, app_data, user_data):
    target = dpg.get_value('target')
    recipe = dpg.get_value('recipe')
    db.update_recipe_minimum(target, recipe, user_data, app_data)

def update_maximum(sender, app_data, user_data):
    target = dpg.get_value('target')
    recipe = dpg.get_value('recipe')
    db.update_recipe_minimum(target, recipe, user_data, app_data)

def update_starting_amount(sender, app_data, user_data):
    target = dpg.get_value('target')
    recipe = dpg.get_value('recipe')
    db.update_recipe_minimum(target, recipe, user_data, app_data)

def update_recipe_bounds():
    dpg.delete_item('recipe_bounds', children_only=True)
    target = dpg.get_value('target')
    recipe = dpg.get_value('recipe')
    bounds = db.get_recipe_bounds(target, recipe)
    with dpg.table(header_row=True, parent='recipe_bounds', row_background=True, borders_innerV=True,
                   borders_innerH=True):
        dpg.add_table_column(label='Food')
        dpg.add_table_column(label='Minimum')
        dpg.add_table_column(label='Maximum')
        dpg.add_table_column(label='Starting amount')
        for row in bounds:
            with dpg.table_row():
                with dpg.group(horizontal=True):
                    dpg.add_button(label='X', user_data=row['food'], callback=remove_food_from_recipe)
                    dpg.add_text(row['food'])
                dpg.add_input_text(default_value='' if row['minimum'] is None else row['minimum'], user_data=row['food'], on_enter=True, decimal=True, width=100, callback=update_minimum)
                dpg.add_input_text(default_value='' if row['maximum'] is None else row['maximum'], user_data=row['food'], on_enter=True, decimal=True, width=100, callback=update_maximum)
                dpg.add_input_text(default_value='' if row['starting_amount'] is None else row['starting_amount'], user_data=row['food'], on_enter=True, decimal=True, width=100, callback=update_starting_amount)
        with dpg.table_row():
            with dpg.group(horizontal=True):
                dpg.add_text('Add food to recipe:')
                dpg.add_combo(items=db.get_food_list(), width=100, no_preview=True, callback=add_food_to_recipe)

def add_food_to_recipe(sender, app_data, user_data):
    target = dpg.get_value('target')
    recipe = dpg.get_value('recipe')
    if target == '' or recipe == '':
        return
    db.add_food_to_recipe(target, recipe, app_data)
    update_recipe_bounds()

def remove_food_from_recipe(sender, app_data, user_data):
    target = dpg.get_value('target')
    recipe = dpg.get_value('recipe')
    
    db.remove_food_from_recipe(target, recipe, user_data)
    update_recipe_bounds()


def update_recipe_selection(sender, app_data, user_data):
    available_recipes = db.get_recipes_by_target(app_data)
    dpg.configure_item('recipe', items=available_recipes)

def update_nutrition_table():
    try:
        scroll_x = dpg.get_x_scroll('nutritional_table')
        scroll_y = dpg.get_y_scroll('nutritional_table')
    except:
        scroll_x = 0
        scroll_y = 0
    dpg.delete_item('nutritional_data', children_only=True)
    rows = db.get_nutritional_data()
    
    with dpg.table(header_row=True, row_background=True, borders_innerH=True, borders_innerV=True,
                   scrollX=True, resizable=True, hideable=True, scrollY=True, height=500, 
                   freeze_rows=1, parent='nutritional_data', tag='nutritional_table'):
        for header in rows[0].keys():
            if header == 'id':
                continue
            dpg.add_table_column(label=header, width_fixed=True)
        for row in rows:
            with dpg.table_row(filter_key=row['food']):
                for key in row.keys():
                    if key == 'id':
                        continue
                    if key == 'food':
                        with dpg.group(horizontal=True):
                            dpg.add_button(label='X', user_data=row['id'], callback=delete_food_from_nutritional_data)
                            dpg.add_text(row[key])
                        continue
                    dpg.add_input_text(default_value=row[key], user_data={'id': row['id'], 'column': key}, 
                                       on_enter=True, width=100, decimal=True, callback=update_nutrition_value,
                                       auto_select_all=True)
        with dpg.table_row():
            with dpg.group(horizontal=True,):
                dpg.add_input_text(hint='Add new food', user_data='food', on_enter=True, width=300, callback=add_food_to_nutritional_table)

    dpg.set_x_scroll('nutritional_table', scroll_x)
    dpg.set_y_scroll('nutritional_table', scroll_y)

def update_nutrition_value(sender, app_data, user_data):
    if app_data == '':
        update_nutrition_table()
        return
    db.update_nutritional_data(user_data['id'], user_data['column'], app_data)
    update_nutrition_table()

def add_food_to_nutritional_table(sender, app_data, user_data):
    if app_data == '':
        return
    db.add_food_to_nutritional_data(app_data)
    update_nutrition_table()

def delete_food_from_nutritional_data(sender, app_data, user_data):
    db.delete_food_from_nutritional_data(user_data)
    update_nutrition_table()

def show_dionysus():
    with dpg.font_registry():
        default_font = dpg.add_font('./assets/JetBrainsMonoNL-Regular.ttf', 20)
    with dpg.window(tag='main'):
        dpg.bind_font(default_font)
        with dpg.group(horizontal=True):
            dpg.add_text('Target:')
            dpg.add_combo(items=db.get_target_names(), fit_width=True, tag='target', callback=update_recipe_selection)
            dpg.add_text('Recipe:')
            dpg.add_combo(items=(), fit_width=True, tag='recipe', callback=update_recipe_bounds)

        dpg.add_separator()
        with dpg.group(tag='recipe_bounds'):
            pass

        dpg.add_separator()
        with dpg.group(tag='recipe_results'):
            pass

        with dpg.collapsing_header(label='Nutritional Data'):
            with dpg.group(horizontal=True):
                dpg.add_text('Filter food:')
                dpg.add_input_text(width=500, user_data='nutritional_table', callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)))
            with dpg.group(tag='nutritional_data'):
                update_nutrition_table()

        with dpg.collapsing_header(label='Targets'):
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
