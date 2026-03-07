import sqlite3
from config import DB_NAME

DB_NAME = DB_NAME


def delete_lesson_by_id(lesson_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id, ))


def delete_student_by_id(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (id, ))