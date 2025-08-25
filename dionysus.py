from scipy.optimize import minimize
import numpy as np
import pandas as pd
import sqlite3

USER = 'luki'
RECIPE = 'rindfleisch obed'

CALCULATION_STRING = 'energy, protein, fatty_acids, saturated_fatty_acids, carbohydrates, fibre'
sql1 = f"""
    SELECT {CALCULATION_STRING} FROM targets
    WHERE name='{USER}';
"""
sql2 = f"""
    SELECT nutritional_data.*, 
    recipes.minimum, 
    recipes.maximum,
    recipes.starting_amount 
    FROM nutritional_data
    JOIN recipes ON nutritional_data.id=recipes.food_id
    JOIN targets ON recipes.user_id=targets.id
    WHERE recipes.recipe_name='{RECIPE}'
    AND targets.name='{USER}';
"""

# prepare data
db = sqlite3.connect("./data/food.db")
target = pd.read_sql_query(sql1, db).to_numpy()[0]
recipe_data = pd.read_sql_query(sql2, db)
recipe_data['energy'] -= recipe_data['protein'] * (1 - recipe_data['protein_digestibility']) * 4
recipe_data['protein'] *= recipe_data['protein_digestibility']
recipe_data.loc[recipe_data['minimum'].isna(), 'minimum'] = 0
recipe_data.loc[recipe_data['maximum'].isna(), 'maximum'] = np.inf
recipe_data.loc[recipe_data['starting_amount'].isna(), 'starting_amount'] = 0
nutrition_matrix = recipe_data[CALCULATION_STRING.split(', ')].to_numpy().T
bound = recipe_data[['minimum', 'maximum']].to_numpy() / 100
initial_weights = recipe_data[['minimum', 'starting_amount']].max(axis=1)

# calculate weights
loss_function = lambda w: np.dot((target - np.dot(nutrition_matrix, w)).T, target - np.dot(nutrition_matrix, w))
res = minimize(loss_function, initial_weights, bounds=bound, method='L-BFGS-B')
final_weights = res.x
final_target = np.dot(nutrition_matrix, final_weights)
calcium = np.inner(recipe_data['calcium'], final_weights)
saturated_fat = np.inner(recipe_data['saturated_fatty_acids'], final_weights)
percentage_saturated_fat = saturated_fat * 9 / final_target[0] * 100

# print results
print(f"{USER + ' ' + RECIPE:-^50} ")
for value, i in zip(CALCULATION_STRING.split(', '), range(len(target))):
    print(f"{value:<21}{final_target[i]:>6.2f} | {target[i]:.2f}")
print(f"{'calcium':<21}{calcium:>6.2f}")
print("-"*50)
for food, weight in zip(recipe_data['food'].values.tolist(), final_weights * 100):
    print(f'{food:<21}{weight:>6.2f}g')
print("-"*50)

db.close()
