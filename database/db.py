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
            CONSTRAINT lessons_students_fk
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reschedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL,
            original_date TEXT NOT NULL,
            new_date TEXT,
            new_start TEXT,
            new_end TEXT,
            status TEXT NOT NULL CHECK(status IN ('moved', 'cancekked')),
                       
            FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
            UNIQUE(lesson_id, original_date)
            )
        """)