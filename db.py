import sqlite3
from pathlib import Path
import threading

class Database:
    def __init__(self, db_path='./data/app.db'):
        self.lock = threading.Lock()
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def get_target_names(self):
        with self.lock:
            rows = self.conn.execute('SELECT name FROM targets ORDER BY name').fetchall()
            return [row['name'] for row in rows]

    def get_recipes_by_target(self, target_name):
        query = f'''
            SELECT DISTINCT recipes.recipe_name FROM recipes
            JOIN targets ON recipes.user_id=targets.id
            WHERE targets.name = ?
            ORDER BY recipes.recipe_name
        '''
        with self.lock:
            rows = self.conn.execute(query, (target_name,)).fetchall()
            return [row['recipe_name'] for row in rows]

    def get_recipe_bounds(self, target_name, recipe_name):
        query = f'''
            SELECT recipes.recipe_name, nutritional_data.food, recipes.minimum, recipes.maximum, recipes.starting_amount
            FROM recipes
            JOIN nutritional_data ON recipes.food_id=nutritional_data.id
            JOIN targets ON recipes.user_id=targets.id 
            WHERE targets.name = ? AND recipes.recipe_name = ?
        '''
        with self.lock:
            return self.conn.execute(query, (target_name, recipe_name,)).fetchall()

    def update_recipe_minimum(self, target_name, recipe_name, food, new_minimum):
        query = '''
            UPDATE recipes
            SET minimum=?
            WHERE recipe_name=?
            AND user_id = (SELECT id FROM targets WHERE name=?)
            AND food_id = (SELECT id FROM nutritional_data WHERE food=?)
        '''
        new_minimum = None if new_minimum == '' else new_minimum
        with self.lock:
            self.conn.execute(query, (new_minimum, recipe_name, target_name, food,))
            self.conn.commit()

    def update_recipe_maximum(self, target_name, recipe_name, food, new_maximum):
        query = '''
            UPDATE recipes
            SET maximum=?
            WHERE recipe_name=?
            AND user_id = (SELECT id FROM targets WHERE name=?)
            AND food_id = (SELECT id FROM nutritional_data WHERE food=?)
        '''
        new_maximum = None if new_maximum == '' else new_maximum
        with self.lock:
            self.conn.execute(query, (new_maximum, recipe_name, target_name, food, ))
            self.conn.commit()

    def update_recipe_starting_amount(self, target_name, recipe_name, food, new_starting_amount):
        query = '''
            UPDATE recipes
            SET starting_amount=?
            WHERE recipe_name=?
            AND user_id = (SELECT id FROM targets WHERE name=?)
            AND food_id = (SELECT id FROM nutritional_data WHERE food=?)
        '''
        new_starting_amount = None if new_starting_amount == '' else new_starting_amount
        with self.lock:
            self.conn.execute(query, (new_starting_amount, recipe_name, target_name, food,))
            self.conn.commit()
        

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = Database('./data/food.db')
    
    print(db.get_recipes_by_target('luki'))

    db.close()
