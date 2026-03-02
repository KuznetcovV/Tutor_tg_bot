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


def select_all_lessons():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""SELECT lessons.id, name, class, weekday, time_start, time_end
                          FROM lessons JOIN students
                          ON lessons.student_id = students.id
                          ORDER BY weekday, time_start""")
        lessons = cursor.fetchall()
        return lessons


def select_today_lessons(day_number):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""SELECT name, class, weekday, time_start, time_end
                          FROM lessons JOIN students
                          ON lessons.student_id = students.id
                          WHERE weekday = ?
                          ORDER BY time_start""", (day_number, ))
        lessons = cursor.fetchall()
        return lessons


def select_occupied_intervals_by_lesson_id(lesson_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT time_start, time_end
                          FROM lessons
                          WHERE weekday = (
                                SELECT weekday
                                FROM lessons
                                WHERE id = ?)
                          AND id != ?""", (lesson_id, lesson_id))
        intervals = cursor.fetchall()
        return [(int(start), int(end)) for start, end in intervals]


def select_occupied_intervals(day_number):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT time_start, time_end
                          FROM lessons
                          WHERE weekday = ?""", (day_number, ))
        intervals = cursor.fetchall()
        return intervals


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


def get_lesson_by_id(lesson_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT name, weekday, time_start, time_end
                          FROM lessons
                          JOIN students
                          ON students.id = lessons.student_id
                          WHERE lessons.id = ?""", (lesson_id, ))
        lesson = cursor.fetchone()
        return lesson


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


def edit_student_by_id(student_id, new_name=None, new_class=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        if new_name and new_class:
            cursor.execute("UPDATE students SET name = ?, class = ? WHERE id = ?", (new_name, new_class, student_id))
            return
        if new_name:
            cursor.execute("UPDATE students SET name = ? WHERE id = ?", (new_name, student_id))
            return
        cursor.execute("UPDATE students SET class = ? WHERE id = ?", (new_class, student_id))


def add_new_student(name, student_class):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, class) VALUES (?, ?)",
                       (name, student_class))


def delete_lesson_by_id(lesson_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id, ))


def delete_student_by_id(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (id, ))


def change_student(old_name, new_name, student_class):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET name = ? , class = ? WHERE name = ?',
                       (new_name, student_class, old_name))
