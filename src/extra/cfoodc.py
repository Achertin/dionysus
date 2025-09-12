import sqlite3
import pandas as pd
import numpy as np

ingredient_ids = [21,18,44]
ingredient_weights = [150,200,700]

sql = f"""
    SELECT * FROM nutritional_data
    WHERE id IN {tuple(ingredient_ids)}
"""

ingredient_ids = np.array(ingredient_ids)
ingredient_weights = np.array(ingredient_weights)
multiplier = ingredient_weights / 100
ingredient_weights = ingredient_weights / ingredient_weights.sum()


db = sqlite3.connect('./data/food.db')
df = pd.read_sql_query(sql, db, index_col='id')
df = df.drop(columns=['food'])
df = df.loc[ingredient_ids]

print(df.mul(ingredient_weights, axis=0).sum().round(2))


db.close()
