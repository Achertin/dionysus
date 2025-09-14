from ast import Tuple
import dearpygui.dearpygui as dpg
from dionysus.core.state import db
import numpy as np
from scipy.optimize import minimize

app_state = {
        'target': None,
        'recipe': None,
        }
# recipe calculator
def draw_recipe_bounds_table():
    if not app_state['target'] or not app_state['recipe']:
        dpg.hide_item('recipe_bounds_table')
        clear_bounds_table()
        return
    clear_bounds_table()
    bounds = db.recipe_bounds(app_state['target'], app_state['recipe'])

    for row in bounds:
        with dpg.table_row(parent='recipe_bounds_table'):
            with dpg.group(horizontal=True):
                dpg.add_button(label='X', user_data=row['food'], callback=on_remove_ingredient)
                dpg.add_text(row['food'])
            dpg.add_input_text(default_value='' if row['minimum'] is None else row['minimum'], 
                               user_data={'food': row['food'], 'column': 'minimum'}, on_enter=True, decimal=True, width=100, callback=on_bound_change)
            dpg.add_input_text(default_value='' if row['maximum'] is None else row['maximum'], 
                               user_data={'food': row['food'], 'column': 'maximum'}, on_enter=True, decimal=True, width=100, callback=on_bound_change)
            dpg.add_input_text(default_value='' if row['starting_amount'] is None else row['starting_amount'], 
                               user_data={'food': row['food'], 'column': 'starting_amount'}, on_enter=True, decimal=True, width=100, callback=on_bound_change)
    
    with dpg.table_row(parent='recipe_bounds_table'):
        with dpg.group(horizontal=True):
            dpg.add_text('Add food to recipe:')
            dpg.add_combo(items=db.food_list(), width=100, no_preview=True, tag='ingredient_add_combo', callback=on_add_ingredient)
    dpg.show_item('recipe_bounds_table')

def clear_bounds_table():
    rows = dpg.get_item_children('recipe_bounds_table', slot=1)
    if not rows:
        return
    for row in rows:
        dpg.delete_item(row)

def update_recipe_calculator():
    update_target_list()
    update_recipe_list()
    draw_recipe_bounds_table()
    update_recipe_results()

def on_target_change(sender, app_data, user_data):
    app_state['target'] = app_data
    update_recipe_calculator()

def on_recipe_change(sender, app_data, user_data):
    app_state['recipe'] = app_data
    update_recipe_calculator()

def update_target_list():
    dpg.configure_item('target_combo', items=db.target_names())

def update_recipe_list():
    recipes = db.recipes_by_target(app_state['target'])
    if app_state['recipe'] not in recipes:
        app_state['recipe'] = None
        dpg.set_value('recipe_combo', '')
    dpg.configure_item('recipe_combo', items=recipes)

def on_bound_change(sender, app_data, user_data):
    db.update_recipe_bounds(app_state['recipe'], app_state['target'], user_data['food'], user_data['column'], None if app_data == '' else app_data)
    update_recipe_calculator()

def on_add_ingredient(sender, app_data, user_data):
    if not app_state['target'] or not app_state['recipe']:
        return
    db.add_ingredient(app_state['target'], app_state['recipe'], app_data)
    update_recipe_calculator()

def on_remove_ingredient(sender, app_data, user_data):
    db.remove_ingredient(app_state['target'], app_state['recipe'], user_data)
    update_recipe_calculator()

def clear_calculation_results():
    nutri_rows = dpg.get_item_children('recipe_nutri_values', slot=1)
    weight_rows = dpg.get_item_children('recipe_weights', slot=1)
    if nutri_rows:
        for row in nutri_rows:
            dpg.delete_item(row)
    if weight_rows:
        for row in weight_rows:
            dpg.delete_item(row)

def draw_recipe_nutri_results(target, calculation_data, final_weights):
    columns = db.calculation_columns.split(',')
    columns.append('calcium')
    final_target = calculation_data[columns].mul(final_weights, axis=0).sum()
    for nutrient in columns:
        with dpg.table_row(parent='recipe_nutri_values'):
            dpg.add_text(nutrient)
            final_target_text = dpg.add_text(f'{final_target[nutrient]:.2f}')
            try:
                dpg.add_text(target[nutrient].squeeze())
            except:
                dpg.add_text('')
        if nutrient == 'saturated_fatty_acids':
            color = (251, 73, 52) if target[nutrient].squeeze() <= final_target[nutrient] else (184, 187, 38)
            dpg.configure_item(final_target_text, color=color)

def draw_recipe_weights(calculation_data, final_weights):
    weights = final_weights * 100
    for ingredient, weight in zip(calculation_data['food'], weights):
        with dpg.table_row(parent='recipe_weights'):
            dpg.add_text(ingredient)
            dpg.add_text(f'{weight:.2f}g')

def calculate_recipe(target, calculation_data) -> np.ndarray:
    nutrition_matrix = calculation_data[db.calculation_columns.split(',')].to_numpy().T
    bounds = calculation_data[['minimum', 'maximum']].to_numpy() / 100
    initial_weights = calculation_data[['minimum', 'starting_amount']].max(axis=1) / 100
    target = target.to_numpy()[0]
    loss_function = lambda w: np.linalg.norm(target - np.dot(nutrition_matrix, w)) ** 2
    res = minimize(loss_function, initial_weights, bounds=bounds)
    return res.x

def update_recipe_results():
    if not app_state['target'] or not app_state['recipe']:
        dpg.hide_item('calculation_results')
        clear_calculation_results()
        return
    target, calculation_data = db.calculation_data(app_state['target'], app_state['recipe'])
    if calculation_data.empty:
        return
    final_weights = calculate_recipe(target, calculation_data)
    clear_calculation_results()
    draw_recipe_nutri_results(target, calculation_data, final_weights)
    draw_recipe_weights(calculation_data, final_weights)
    dpg.show_item('calculation_results')

def center_recipe_popup(popup_id):
    main_widht = dpg.get_viewport_width() or 0
    main_height = dpg.get_viewport_height() or 0
    popup_width = dpg.get_item_width(popup_id) or 0
    popup_height = dpg.get_item_height(popup_id) or 0
    pos_x = (main_widht - popup_width) // 2
    pos_y = (main_height - popup_height) // 2
    dpg.set_item_pos(popup_id, pos=[pos_x, pos_y])

def on_copy_recipe(sender, app_data, user_data):
    with dpg.window(modal=True, popup=True, no_move=True, autosize=True, no_close=True) as popup_id:
        if not app_state['target']:
            dpg.add_text('No source target selected!')    
            dpg.add_button(label='Close', callback=lambda s, a, u: dpg.delete_item(popup_id))
        elif not app_state['recipe']:
            dpg.add_text('No source recipe selected!')    
            dpg.add_button(label='Close', callback=lambda s, a, u: dpg.delete_item(popup_id))
        else:
            copy_data = {
                    'new_target': None,
                    'new_name': app_state['recipe'],
                    }
            with dpg.group(horizontal=True):
                dpg.add_text('New target:     ')
                dpg.add_combo(items=db.target_names(), tag='new_recipe_target', callback=lambda s, a, u: copy_data.update({'new_target': a}))
            with dpg.group(horizontal=True):
                dpg.add_text('New recipe name:')
                dpg.add_input_text(default_value=app_state['recipe'], tag='new_recipe_name', callback=lambda s, a, u: copy_data.update({'new_name': a}))
            with dpg.group(horizontal=True):
                dpg.add_button(label='Copy', callback=lambda s, a, u: copy_recipe_confirm(copy_data, popup_id))
                dpg.add_button(label='Close', callback=lambda s, a, u: dpg.delete_item(popup_id))
    dpg.set_frame_callback(1, lambda: center_recipe_popup)

def copy_recipe_confirm(copy_data, popup_id):
    if not copy_data['new_target'] or not copy_data['new_name']:
        dpg.add_text('Make sure all fields are filled in', color=(251, 73, 52), parent=popup_id)
        return
    if copy_data['new_name'] in db.recipes_by_target(copy_data['new_target']):
        dpg.add_text('Recipe already exists for that target', color=(251, 73, 52), parent=popup_id)
        return
    db.copy_recipe(app_state['recipe'], app_state['target'], copy_data['new_target'], copy_data['new_name'])
    app_state['target'] = copy_data['new_target']
    app_state['recipe'] = copy_data['new_name']
    dpg.set_value('target_combo', app_state['target'])
    dpg.set_value('recipe_combo', app_state['recipe'])
    update_recipe_calculator()
    dpg.delete_item(popup_id)

def on_rename_recipe(sende, app_data, user_data):
    pass

def on_delete_recipe(sende, app_data, user_data):
    pass

def on_add_recipe(sende, app_data, user_data):
    pass

# nutritional table
def update_nutrition_table():
    try:
        scroll_x = dpg.get_x_scroll('nutritional_table')
        scroll_y = dpg.get_y_scroll('nutritional_table')
    except:
        scroll_x = 0
        scroll_y = 0
    dpg.delete_item('nutritional_data', children_only=True)
    rows = db.nutritional_data()
    nutritional_table(rows)
    with dpg.table_row(parent='nutritional_table'):
        with dpg.group(horizontal=True,):
            dpg.add_input_text(hint='Add new food', user_data='food', on_enter=True, width=300, callback=add_food_to_nutritional_table)

    dpg.set_x_scroll('nutritional_table', scroll_x)
    dpg.set_y_scroll('nutritional_table', scroll_y)

def nutritional_table(nutritional_rows):
    with dpg.table(header_row=True, row_background=True, borders_innerH=True, borders_innerV=True,
                   scrollX=True, resizable=True, hideable=True, scrollY=True, height=500, 
                   freeze_rows=1, parent='nutritional_data', tag='nutritional_table'):
        for header in nutritional_rows[0].keys():
            if header == 'id':
                continue
            dpg.add_table_column(label=header, width_fixed=True)
        for row in nutritional_rows:
            with dpg.table_row(filter_key=row['food']):
                for key in row.keys():
                    if key == 'id':
                        continue
                    if key == 'food':
                        with dpg.group(horizontal=True):
                            dpg.add_button(label='X', user_data=row['id'])
                            with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left) as remove_food:
                                dpg.add_text(f'Are you sure you want to remove {row['food']} from the table?')
                                with dpg.group(horizontal=True):
                                    dpg.add_button(label='Yes', user_data={'food_id': row['id'], 'popup_id': remove_food}, callback=delete_food_from_nutritional_data)
                                    dpg.add_button(label='Cancel', user_data=remove_food, callback=lambda s, a, u: dpg.configure_item(u, show=False))
                            dpg.add_input_text(default_value=row[key], user_data={'id': row['id'], 'column': key}, 
                                               on_enter=True, width=250, callback=update_nutrition_value)
                        continue
                    dpg.add_input_text(default_value=row[key], user_data={'id': row['id'], 'column': key}, 
                                       on_enter=True, width=100, decimal=True, callback=update_nutrition_value,
                                       auto_select_all=True)

def update_nutrition_value(sender, app_data, user_data):
    if app_data == '':
        update_nutrition_table()
        return
    db.update_nutritional_data(user_data['id'], user_data['column'], app_data)
    update_nutrition_table()
    filter_nutri_table('nutri_filter', None, 'nutritional_table')

def add_food_to_nutritional_table(sender, app_data, user_data):
    if app_data == '':
        return
    db.add_food_to_nutritional_data(app_data)
    update_nutrition_table()
    dpg.configure_item('add_ingredient_to_recipe', items=db.food_list())

def delete_food_from_nutritional_data(sender, app_data, user_data):
    db.remove_food_from_nutritional_data(user_data['food_id'])
    update_nutrition_table()
    dpg.configure_item(user_data['popup_id'], show=False)

def filter_nutri_table(sender, app_data, user_data):
    dpg.set_value(user_data, dpg.get_value(sender))
