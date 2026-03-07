import sqlite3
from config import DB_NAME

DB_NAME = DB_NAME


def add_new_student(name, student_class):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, class) VALUES (?, ?)",
                       (name, student_class))


def add_lesson(student_id, weekday, time_start, time_end):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
        INSERT INTO lessons (
            student_id, weekday, time_start, time_end
            )
            VALUES (?, ?, ?, ?)
        """, (student_id, weekday, time_start, time_end))