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
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return students


def get_student_by_id(student_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, class FROM students WHERE id = ?", (student_id, ))
        return cursor.fetchone()


def edit_student_by_id(student_id, new_name=None, new_class=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        if new_name and new_class:
            cursor.execute("UPDATE students SET name = ?, class = ? WHERE ID = ?", (new_name, new_class, student_id))
            return
        if new_name:
            cursor.execute("UPDATE students SET name = ? WHERE ID = ?", (new_name, student_id))
            return
        cursor.execute("UPDATE students SET class = ? WHERE ID = ?", (new_class, student_id))


def add_new_student(name, student_class):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, class) VALUES (?, ?)",
                       (name, student_class))


def delete_student_by_id(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (id, ))


def change_student(old_name, new_name, student_class):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET name = ? , class = ? WHERE name = ?' ,
                       (new_name, student_class, old_name))
