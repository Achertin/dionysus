from operator import call
import dearpygui.dearpygui as dpg
from db import Database
import numpy as np
import pandas as pd
from scipy.optimize import minimize

db = Database("./data/test_db.db")

def recipe_bounds():
    dpg.delete_item('recipe_bounds', children_only=True)
    bounds = db.recipe_bounds(dpg.get_value('target'), dpg.get_value('recipe'))
    if bounds:
        bounds_table(bounds)
    else:
        with dpg.table(header_row=True, parent='recipe_bounds', row_background=True, borders_innerV=True,
                       borders_innerH=True, tag='bounds_table'):
            dpg.add_table_column()
    with dpg.table_row(parent='bounds_table'):
        with dpg.group(horizontal=True):
            dpg.add_text('Add food to recipe:')
            dpg.add_combo(items=db.food_list(), width=100, no_preview=True, callback=add_ingredient)

def bounds_table(bounds_rows: list):
    with dpg.table(header_row=True, parent='recipe_bounds', row_background=True, borders_innerV=True,
                   borders_innerH=True, tag='bounds_table'):
        for column in bounds_rows[0].keys():
            dpg.add_table_column(label=column)
        for row in bounds_rows:
            with dpg.table_row():
                with dpg.group(horizontal=True):
                    dpg.add_button(label='X', user_data=row['food'], callback=remove_ingredient)
                    dpg.add_text(row['food'])
                dpg.add_input_text(default_value='' if row['minimum'] is None else row['minimum'], 
                                   user_data={'food': row['food'], 'column': 'minimum'}, on_enter=True, decimal=True, width=100, callback=update_recipe_bounds)
                dpg.add_input_text(default_value='' if row['maximum'] is None else row['maximum'], 
                                   user_data={'food': row['food'], 'column': 'maximum'}, on_enter=True, decimal=True, width=100, callback=update_recipe_bounds)
                dpg.add_input_text(default_value='' if row['starting_amount'] is None else row['starting_amount'], 
                                   user_data={'food': row['food'], 'column': 'starting_amount'}, on_enter=True, decimal=True, width=100, callback=update_recipe_bounds)

def update_recipe_bounds(sender, app_data, user_data):
    recipe = dpg.get_value('recipe')
    target = dpg.get_value('target')
    db.update_recipe_bounds(recipe, target, user_data['food'], user_data['column'], None if app_data == '' else app_data)
    recipe_bounds()
    update_recipe_results()

def add_ingredient(sender, app_data, user_data):
    target = dpg.get_value('target')
    recipe = dpg.get_value('recipe')
    if target == '' or recipe == '':
        return
    db.add_ingredient(target, recipe, app_data)
    recipe_bounds()

def remove_ingredient(sender, app_data, user_data):
    target = dpg.get_value('target')
    recipe = dpg.get_value('recipe')
    
    db.remove_ingredient(target, recipe, user_data)
    recipe_bounds()

def update_recipe_selection(sender, app_data, user_data):
    dpg.delete_item('recipe_bounds', children_only=True)
    dpg.delete_item('recipe_results', children_only=True)
    available_recipes = db.recipes_by_target(app_data)
    dpg.configure_item('recipe', items=available_recipes,)
    dpg.set_value('recipe', '')

def show_bounds_and_calculate():
    recipe_bounds()
    update_recipe_results()

def calculate_recipe(target, calculation_data) -> np.ndarray:
    nutrition_matrix = calculation_data[db.calculation_columns.split(',')].to_numpy().T
    bounds = calculation_data[['minimum', 'maximum']].to_numpy() / 100
    initial_weights = calculation_data[['minimum', 'starting_amount']].max(axis=1) / 100
    target = target.to_numpy()[0]
    loss_function = lambda w: np.linalg.norm(target - np.dot(nutrition_matrix, w)) ** 2
    res = minimize(loss_function, initial_weights, bounds=bounds)
    return res.x

def update_recipe_results():
    dpg.delete_item('recipe_results', children_only=True)
    target, calculation_data = db.calculation_data(dpg.get_value('target'), dpg.get_value('recipe'))
    final_weights = calculate_recipe(target, calculation_data)

    with dpg.group(parent='recipe_results'):
        with dpg.table(tag='recipe_nutri_values', header_row=True):
            dpg.add_table_column(label='nutrient')
            dpg.add_table_column(label='final vlaue')
            dpg.add_table_column(label='target value')
        with dpg.table(tag='recipe_weights', header_row=True):
            dpg.add_table_column(label='ingredient')
            dpg.add_table_column(label='weight')
    result_values_table(target, calculation_data, final_weights)
    weights_table(calculation_data, final_weights)

def result_values_table(target, calculation_data, final_weights):
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
            color = (251, 73, 52) if target[nutrient].squeeze() < final_target[nutrient] else (184, 187, 38)
            dpg.configure_item(final_target_text, color=color)


def weights_table(calculation_data, final_weights):
    weights = final_weights * 100
    for ingredient, weight in zip(calculation_data['food'], weights):
        with dpg.table_row(parent='recipe_weights'):
            dpg.add_text(ingredient)
            dpg.add_text(f'{weight:.2f}g')

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
                            dpg.add_button(label='X', user_data=row['id'], callback=delete_food_from_nutritional_data)
                            dpg.add_text(row[key])
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

def add_food_to_nutritional_table(sender, app_data, user_data):
    if app_data == '':
        return
    db.add_food_to_nutritional_data(app_data)
    update_nutrition_table()

def delete_food_from_nutritional_data(sender, app_data, user_data):
    db.remove_food_from_nutritional_data(user_data)
    update_nutrition_table()

def new_recipe():
    dpg.set_value('recipe', dpg.get_value('new_recipe'))
    dpg.set_value('new_recipe', '')
    recipe_bounds()

def show_dionysus():
    with dpg.font_registry():
        default_font = dpg.add_font('./assets/JetBrainsMonoNL-Regular.ttf', 20)
    with dpg.window(tag='main'):
        dpg.bind_font(default_font)
        with dpg.group(horizontal=True):
            dpg.add_text('Target:')
            dpg.add_combo(items=db.target_names(), fit_width=True, tag='target', callback=update_recipe_selection)
            dpg.add_text('Recipe:')
            dpg.add_combo(items=(), fit_width=True, tag='recipe', callback=show_bounds_and_calculate)
        with dpg.group(horizontal=True):
            dpg.add_text('New recipe:')
            dpg.add_input_text(hint='Recipe name...', width=250, tag='new_recipe')
            dpg.add_button(label='Add recipe', callback=new_recipe)
            dpg.add_spacer(width=100)
            dpg.add_text('Copy recipe')
            dpg.add_combo(items=db.target_names(), fit_width=True, tag='copy_target', callback=update_recipe_selection)
            dpg.add_button(label='Copy')

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
