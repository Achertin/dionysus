import os

from dionysus.database.database import init_db
from dionysus.ui.main_window import start_main_window

from .config import DATA_DIR


def run():
    os.makedirs(DATA_DIR, exist_ok=True)
    init_db()
    start_main_window()
