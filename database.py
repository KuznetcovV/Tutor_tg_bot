import sqlite3

DB_NAME = 'ALL_STUDENTS'


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


def get_all_students():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, class FROM students")
        students = cursor.fetchall()
        return students


def add_new_student(name, student_class):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, class) VALUES (?, ?)",
                       (name, student_class))


def delete_student(name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, class FROM students WHERE name = ?", (name, ))
        student = cursor.fetchone()
        cursor.execute("DELETE FROM students WHERE name = ?", (name, ))
        return student


def change_student(old_name, new_name, student_class):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET name = ? , class = ? WHERE name = ?' ,
                       (new_name, student_class, old_name))
