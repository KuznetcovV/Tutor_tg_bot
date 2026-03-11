import sqlite3
from config import DB_NAME

DB_NAME = DB_NAME


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


def select_lessons_for_weekday(day_number):
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
        intervals = [(int(start), int(end)) for start, end in intervals]
        return [(int(start), int(end)) for start, end in intervals]


def select_all_students():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return students


def select_student_by_id(student_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, class FROM students WHERE id = ?", (student_id, ))
        return cursor.fetchone()


def select_lesson_by_id(lesson_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT name, weekday, time_start, time_end
                          FROM lessons
                          JOIN students
                          ON students.id = lessons.student_id
                          WHERE lessons.id = ?""", (lesson_id, ))
        lesson = cursor.fetchone()
        return lesson
