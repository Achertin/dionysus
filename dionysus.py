from scipy.optimize import minimize
import numpy as np
import pandas as pd
import sqlite3

USER = 'alka'
RECIPE = 'ranajky bratislava'
CALCULATION_STRING = 'energy, protein, fatty_acids, carbohydrates, fibre'


db = sqlite3.connect("./food.db")
target = pd.read_sql_query(f'SELECT {CALCULATION_STRING}  FROM targets WHERE name="{USER}"', db).to_numpy()[0]
recipe_data = pd.read_sql_query(f"""SELECT *,COALESCE(minimum, 0) FROM recipes 
                                     INNER JOIN nutritional_data ON nutritional_data.id = recipes.food_id 
                                     WHERE recipes.recipe_name='{RECIPE}'""", db)
nutrition_matrix = recipe_data[CALCULATION_STRING.split(', ')].T
bounds = recipe_data[['COALESCE(minimum, 0)', 'maximum']].to_numpy()
initial_weights = bounds.T[0]

loss_function = lambda w: np.linalg.norm(target - np.dot(nutrition_matrix, w)) ** 2
res = minimize(loss_function, initial_weights, bounds=bounds)
final_weights = np.round(res.x, 2)
final_target = np.round(np.dot(nutrition_matrix, final_weights), 2)
calcium = np.round(np.inner(recipe_data['calcium'], final_weights))
saturated_fat = np.round(np.inner(recipe_data['saturated_fatty_acids'], final_weights))
percentage_saturated_fat = np.round(saturated_fat * 9 / final_target[0] * 100, 2)

print("-"*20)
print(f"Energy: {final_target[0]}|{target[0]} ", 
      f"Protein: {final_target[1]}|{target[1]} ",
      f"Fatty acids: {final_target[2]}|{target[2]} ",
      f"Carbohydrates: {final_target[3]}|{target[3]} ",
      f"Fibre: {final_target[4]}|{target[4]}")
print(f"Calcium: {calcium}mg")
print(f"Saturated fat: {saturated_fat} ({percentage_saturated_fat}%)")
print("-"*20)
for food, weight in zip(recipe_data['food'].values.tolist(), np.round(final_weights * 100, 2)):
    print(f'{food}: {weight}g'.capitalize())
print("-"*20)

db.close()
