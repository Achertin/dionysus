"""Widget tags for the food database screen.

Naming convention: <screen>.<component>.<element>_<kind>

Only widgets that other code needs to look up get a tag here.
Widgets that are created once and never touched again stay untagged.
"""

from dionysus.constants import FOOD_METADATA

_SCREEN = "food_db"

_ALL_NUTRIENTS = {
    nutrient
    for section in FOOD_METADATA.values()
    for nutrient in section
}


def _nutrient_tag(component: str, nutrient: str, kind: str) -> str:
    """Build a tag for a per-nutrient widget, rejecting unknown nutrients."""
    if nutrient not in _ALL_NUTRIENTS:
        raise ValueError(f"Unknown nutrient {nutrient!r}; check FOOD_METADATA")
    return f"{_SCREEN}.{component}.{nutrient}_{kind}"


# --- Layout -----------------------------------------------------------------

TABLE_WINDOW = f"{_SCREEN}.table_window"
DETAIL_WINDOW = f"{_SCREEN}.detail_window"


# --- Search bar -------------------------------------------------------------

SEARCH_INPUT = f"{_SCREEN}.search.text_input"
ADD_BUTTON = f"{_SCREEN}.search.add_button"


# --- Food table -------------------------------------------------------------

TABLE = f"{_SCREEN}.table"


# --- Detail panel -----------------------------------------------------------

DETAIL_NAME_TEXT = f"{_SCREEN}.detail.name_text"
DETAIL_EDIT_BUTTON = f"{_SCREEN}.detail.edit_button"
DETAIL_DELETE_BUTTON = f"{_SCREEN}.detail.delete_button"


def detail_value_text(nutrient: str) -> str:
    """Text showing one nutrient's value in the detail panel."""
    return _nutrient_tag("detail", nutrient, "text")


# --- Edit popup -------------------------------------------------------------

EDIT_POPUP = f"{_SCREEN}.edit_popup"
EDIT_TITLE_TEXT = f"{_SCREEN}.edit_popup.title_text"


def edit_label_text(nutrient: str) -> str:
    """Label next to one nutrient's input in the edit popup."""
    return _nutrient_tag("edit_popup", nutrient, "label_text")


def edit_value_input(nutrient: str) -> str:
    """Input field for one nutrient's value in the edit popup."""
    return _nutrient_tag("edit_popup", nutrient, "input")


# --- Delete popup -----------------------------------------------------------

DELETE_POPUP = f"{_SCREEN}.delete_popup"
DELETE_WARNING_TEXT = f"{_SCREEN}.delete_popup.warning_text"


# --- Add popup --------------------------------------------------------------

ADD_POPUP = f"{_SCREEN}.add_popup"
ADD_NAME_INPUT = f"{_SCREEN}.add_popup.name_input"


def add_value_input(nutrient: str) -> str:
    """Input field for one nutrient's value in the add popup."""
    return _nutrient_tag("add_popup", nutrient, "input")
