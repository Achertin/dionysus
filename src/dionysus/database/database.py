import sqlite3
from dionysus.config import DATABASE_PATH
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection():
    conn =  sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    schema = SCHEMA_PATH.read_text()

    with get_connection() as conn:
        conn.executescript(schema)


def get_food(search_text):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT
                id,
                name,
                energy,
                protein,
                fatty_acids,
                saturated_fatty_acids,
                carbohydrates,
                fibre
            FROM nutritional_data
            WHERE name LIKE ?
            ORDER BY name
            """,
            (f"%{search_text}%",)
        ).fetchall()

    return [dict(row) for row in rows]


def get_food_detail(food_id):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            """
            SELECT *
            FROM nutritional_data
            WHERE id = ?
            """,
            (food_id,)
        ).fetchone()

    return row


def update_food_detail(food_id, new_data):
    assignments = ", ".join(
        f"{column} = ? "
        for column in new_data
    )

    query = f"""
        UPDATE nutritional_data
        SET {assignments}
        WHERE id = ?
    """

    values = tuple(new_data.values()) + (food_id,)
    with get_connection() as conn:
        conn.execute(query, values)


def delete_food(food_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM nutritional_data WHERE id = ?",
            (food_id,)
        )
