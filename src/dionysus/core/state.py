from dionysus.core.db import Database
from platformdirs import user_data_dir
import os

appname = 'dionysus'
app_data_path = user_data_dir(appname, None)
os.makedirs(app_data_path, exist_ok=True)
db = Database(app_data_path + '/food.db')
