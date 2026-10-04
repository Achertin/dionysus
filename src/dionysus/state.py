from dataclasses import dataclass

@dataclass
class DatabaseState:
    selected_food_id: int | None = None
    search_filter: str = ""
