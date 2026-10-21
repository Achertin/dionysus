from dataclasses import dataclass


@dataclass
class FoodDBState:
    selected_food_id: int | None = None
    search_filter: str = ""

@dataclass
class UsersState:
    selected_user_id: int | None = None
    search_filter: str = ""
