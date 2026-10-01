from pathlib import Path
from platformdirs import user_data_dir

APP_NAME = "Dionysus"
APP_VERSION = "0.1.0"

DATA_DIR = Path(user_data_dir(APP_NAME))
DATABASE_PATH = DATA_DIR / "food.db"
