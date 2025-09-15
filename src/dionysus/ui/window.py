from turtle import width
import dearpygui.dearpygui as dpg
import dionysus.ui.callbacks as ds
from dionysus.core.state import db
from dionysus.core.state import app_data_path
import os
from pathlib import Path

def show_dionysus():
    with dpg.font_registry():
        default_font = dpg.add_font(os.path.expandvars(app_data_path + '/assets/JetBrainsMonoNL-Regular.ttf'), 20)
    with dpg.window(tag='main'):
        dpg.bind_font(default_font)
        with dpg.group(tag='recipe_calculator'):
            with dpg.group(horizontal=True):
                dpg.add_text('Target:')
                dpg.add_combo(items=db.target_names(), fit_width=True, tag='target_combo', callback=ds.on_target_change)
                dpg.add_text('Recipe:')
                dpg.add_combo(fit_width=True, tag='recipe_combo', callback=ds.on_recipe_change)
            with dpg.group(horizontal=True):
                dpg.add_button(label='Add recipe', callback=ds.on_add_recipe)
                dpg.add_button(label='Rename recipe', callback=ds.on_rename_recipe)
                dpg.add_button(label='Copy recipe', callback=ds.on_copy_recipe)
                dpg.add_button(label='Delete recipe', callback=ds.on_delete_recipe)

        dpg.add_separator()
        with dpg.group(tag='recipe_bounds'):
            with dpg.table(header_row=True, row_background=True, borders_innerV=True, borders_innerH=True, tag='recipe_bounds_table', resizable=True, show=False):
                dpg.add_table_column(label='ingredient')
                dpg.add_table_column(label='minimum')
                dpg.add_table_column(label='maximum')
                dpg.add_table_column(label='starting amount')

        dpg.add_separator()
        with dpg.group(tag='calculation_results', show=False):
            with dpg.table(tag='recipe_nutri_values', header_row=True):
                dpg.add_table_column(label='nutrient')
                dpg.add_table_column(label='final vlaue')
                dpg.add_table_column(label='target value')
            with dpg.table(tag='recipe_weights', header_row=True):
                dpg.add_table_column(label='ingredient')
                dpg.add_table_column(label='weight')

        with dpg.collapsing_header(label='Nutritional Data'):
            with dpg.group(horizontal=True):
                dpg.add_text('Filter food:')
                dpg.add_input_text(width=300, user_data='nutritional_data_table', tag='nutri_filter', callback=ds.on_filter_nutri_table)
                dpg.add_button(label='Add food', callback=ds.on_add_food_to_nutri_table)
            with dpg.table(header_row=True, row_background=True, borders_innerH=True, borders_innerV=True, scrollX=True, resizable=True, hideable=True, scrollY=True, height=600, freeze_rows=1, tag='nutritional_data_table'):
                for column in db.nutritional_data_columns():
                    if column == 'id':
                        continue
                    dpg.add_table_column(label=column, width_fixed=True)
            ds.draw_nutri_table()

            with dpg.group(tag='nutritional_data'):
                pass
