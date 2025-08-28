import sqlite3
from pathlib import Path
import threading
import pandas as pd
import numpy as np


class Database:
    def __init__(self, db_path='./data/app.db'):
        self.lock = threading.Lock()
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.calculation_columns = 'energy, protein, fatty_acids, saturated_fatty_acids, carbohydrates, fibre'

    def target_names(self) -> list[str]:
        with self.lock:
            rows = self.conn.execute('SELECT name FROM targets ORDER BY name').fetchall()
            return [row['name'] for row in rows]

    def recipes_by_target(self, target) -> list[str]:
        query = f'''
            SELECT DISTINCT recipes.recipe FROM recipes
            JOIN targets ON recipes.target_id=targets.id
            WHERE targets.name = ?
            ORDER BY recipes.recipe
        '''
        with self.lock:
            rows = self.conn.execute(query, (target,)).fetchall()
            return [row['recipe'] for row in rows]

    def recipe_bounds(self, target, recipe) -> list:
        query = f'''
            SELECT nutritional_data.food, recipes.minimum, recipes.maximum, recipes.starting_amount
            FROM recipes
            JOIN nutritional_data ON recipes.food_id=nutritional_data.id
            JOIN targets ON recipes.target_id=targets.id 
            WHERE targets.name = ? AND recipes.recipe = ?
        '''
        with self.lock:
            return self.conn.execute(query, (target, recipe)).fetchall()

    def update_recipe_bounds(self, recipe, target, food, column, new_value):
        query = f'''
            UPDATE recipes
            SET {column} = ?
            WHERE recipe = ?
            AND target_id = (SELECT id FROM targets WHERE name = ?)
            AND food_id = (SELECT id FROM nutritional_data WHERE food = ?)
        '''
        with self.lock:
            self.conn.execute(query, (new_value, recipe, target, food))
            self.conn.commit()

    def add_ingredient(self, target, recipe, food):
        query = '''
            INSERT INTO recipes (target_id, recipe, food_id)
            VALUES (
                (SELECT id FROM targets WHERE name = ?),
                ?,
                (SELECT id FROM nutritional_data WHERE food = ?)
            )
        '''
        with self.lock:
            self.conn.execute(query, (target, recipe, food))
            self.conn.commit()

    def remove_ingredient(self, target, recipe, food):
        query = '''
            DELETE FROM recipes
            WHERE recipe = ?
            AND target_id = (SELECT id FROM targets WHERE name = ?)
            AND food_id = (SELECT id FROM nutritional_data WHERE food = ?)
        '''
        with self.lock:
            self.conn.execute(query, (recipe, target, food))
            self.conn.commit()

    
    def food_list(self) -> list[str]:
        with self.lock:
            rows = self.conn.execute('SELECT food FROM nutritional_data ORDER BY food').fetchall()
            return [row['food'] for row in rows]

    def update_nutritional_data(self, id, column, value):
        query = f'''
            UPDATE nutritional_data
            SET {column} = ?
            WHERE id = ?
        '''
        with self.lock:
            self.conn.execute(query, (value, id))
            self.conn.commit()

    def nutritional_data(self) -> list:
        with self.lock:
            return self.conn.execute('SELECT * FROM nutritional_data ORDER BY food').fetchall()

    def add_food_to_nutritional_data(self, food):
        with self.lock:
            self.conn.execute('INSERT INTO nutritional_data (food) VALUES (?)', (food,))
            self.conn.commit()

    def remove_food_from_nutritional_data(self, id):
        with self.lock:
            self.conn.execute('DELETE FROM nutritional_data WHERE id = ?', (id,))
            self.conn.commit()
        
    def target_values(self, target) -> np.ndarray:
        query = f'''
            SELECT {self.calculation_columns} FROM targets
            WHERE name = {target}
        '''
        with self.lock:
            return pd.read_sql_query(query, self.conn).to_numpy()[0]

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = Database('./data/test_db.db')
    
    print(db.recipes_by_target('luki'))
    db.add_food_to_nutritional_data('vinegar')

    db.close()
