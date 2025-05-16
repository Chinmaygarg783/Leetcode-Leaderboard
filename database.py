import sqlite3
from pathlib import Path

DB_PATH = "leaderboard.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db_exists = Path(DB_PATH).exists()
    conn = get_db()
    cursor = conn.cursor()

    # Create users table (stores all usernames)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY
        );
    """)

    # Create stats table (date-based history for each user)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            username TEXT,
            date TEXT,
            solved INTEGER,
            PRIMARY KEY (username, date),
            FOREIGN KEY (username) REFERENCES users(username)
        );
    """)

    conn.commit()
    conn.close()

    if not db_exists:
        print("Database created and initialized.")
    else:
        print("Database already exists and is initialized.")


if __name__ == "__main__":
    init_db()
