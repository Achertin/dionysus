from scipy.optimize import minimize
import numpy as np
import pandas as pd
import sqlite3

USER = 'alka'
RECIPE = 'ranajky bratislava'

CALCULATION_STRING = 'energy, protein, fatty_acids, carbohydrates, fibre'
sql1 = f"""
    SELECT {CALCULATION_STRING} FROM targets
    WHERE name='{USER}';
"""
sql2 = f"""
    SELECT nutritional_data.*, 
    COALESCE(0, recipes.minimum) AS minimum, maximum FROM nutritional_data
    JOIN recipes ON nutritional_data.id=recipes.food_id
    JOIN targets ON recipes.user_id=targets.id
    WHERE recipes.recipe_name='{RECIPE}'
    AND targets.name='{USER}';
"""

# prepare data
db = sqlite3.connect("./data/food.db")
target = pd.read_sql_query(sql1, db).to_numpy()[0]
recipe_data = pd.read_sql_query(sql2, db)
recipe_data['protein'] *= recipe_data['protein_digestibility']
nutrition_matrix = recipe_data[CALCULATION_STRING.split(', ')].to_numpy().T
bounds = recipe_data[['minimum', 'maximum']].to_numpy()
initial_weights = bounds.T[0]

# calculate weights
loss_function = lambda w: np.linalg.norm(target - np.dot(nutrition_matrix, w)) ** 2
res = minimize(loss_function, initial_weights, bounds=bounds)
final_weights = res.x
final_target = np.dot(nutrition_matrix, final_weights)
calcium = np.inner(recipe_data['calcium'], final_weights)
saturated_fat = np.inner(recipe_data['saturated_fatty_acids'], final_weights)
percentage_saturated_fat = saturated_fat * 9 / final_target[0] * 100

# print results
print("-"*50)
for value, i in zip(CALCULATION_STRING.split(', '), range(len(target))):
    print(f"{value:<16}{final_target[i]:>6.2f} | {target[i]:.2f}")
print(f"{'calcium':<16}{calcium:>6.2f}")
print(f"{'saturated fat':<16}{saturated_fat:>6.2f} ({percentage_saturated_fat:.2f}%)")
print("-"*50)
for food, weight in zip(recipe_data['food'].values.tolist(), np.round(final_weights * 100, 2)):
    print(f'{food:<16}{weight:>6.2f}g')
print("-"*50)

db.close()
