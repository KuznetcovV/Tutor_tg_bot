import sqlite3
from config import DB_NAME

DB_NAME = DB_NAME


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            weekday INTEGER,
            time_start TEXT,
            time_end TEXT,
            FOREIGN KEY (student_id) REFERENCES students (id)
            )
        """)