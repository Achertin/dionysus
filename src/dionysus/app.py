import os
from .config import (
    DATA_DIR,
    DATABASE_PATH
)
from dionysus.ui.main_window import start_main_window
from dionysus.database.database import init_db

def run():
    os.makedirs(DATA_DIR, exist_ok=True)
    init_db()
    start_main_window()
