import sqlite3
from config import DB_NAME

DB_NAME = DB_NAME


def update_lesson_data(lessond_id, field, new_value):
    ALLOWED_FIELDS = {'weekday',
                      'timeinterval',
                      'student_id'}
    if field not in ALLOWED_FIELDS:
        raise ValueError('Недопустимое поле')

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        if field == 'timeinterval':
            sql = 'UPDATE lessons SET time_start = ?, time_end = ? WHERE id = ?'
            cursor.execute(sql, (new_value[0], new_value[1], lessond_id))
        else:
            sql = f'UPDATE lessons SET {field} = ? WHERE id = ?'
            cursor.execute(sql, (new_value, lessond_id))


def update_student_by_id(student_id, new_name=None, new_class=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        if new_name and new_class:
            cursor.execute("UPDATE students SET name = ?, class = ? WHERE id = ?", (new_name, new_class, student_id))
            return
        if new_name:
            cursor.execute("UPDATE students SET name = ? WHERE id = ?", (new_name, student_id))
            return
        cursor.execute("UPDATE students SET class = ? WHERE id = ?", (new_class, student_id))


def update_name_student_by_name(old_name, new_name, student_class):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET name = ? , class = ? WHERE name = ?',
                       (new_name, student_class, old_name))