from pathlib import Path
import sqlite3

DB_PATH = Path("data/db/nifty100.db")
SCHEMA_PATH = Path("db/schema.sql")


def create_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        with open(SCHEMA_PATH, encoding="utf-8") as file:
            schema = file.read()

        conn.executescript(schema)

    print(f"Database created successfully: {DB_PATH}")


if __name__ == "__main__":
    create_database()