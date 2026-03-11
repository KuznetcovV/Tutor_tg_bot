from database.queries.inserts import add_new_student
from database.queries.updates import update_student_by_id
from database.queries.deletes import delete_student_by_id
from database.queries.selects import (select_student_by_id,
                                      select_all_students,
                                      select_all_lessons_day_for_student)
import calendar
from datetime import datetime


def get_all_students():
    students = select_all_students()
    return students


def count_weekday_in_month(weekday):
    year = datetime.now().year
    month = datetime.now().month
    return sum(1 for week in calendar.monthcalendar(year, month) if week[weekday] != 0)


def calculate_price_for_student(student_id, price=1000):
    total_lessons = 0

    for weekday in select_all_lessons_day_for_student(student_id):
        total_lessons += count_weekday_in_month(weekday)
    total_price = total_lessons * price

    return total_price


def calculate_all_prices_for_students():
    result = list()
    for student in select_all_students():
        student_id, name, *_ = student
        payment = calculate_price_for_student(student_id)
        result.append((name, payment))
    return result


def add_student_to_base(data):
    name = data['name']
    student_class = data['student_class']
    add_new_student(name, student_class)
    text = (f'Ученик {name},'
            f'который учится в {student_class} классе добавлен')
    return text


def get_student_name_by_id(student_id):
    name, _ = select_student_by_id(student_id)
    return name


def get_full_student_by_id(student_id):
    name, student_class = select_student_by_id(student_id)
    return name, student_class


def save_new_value_to_base(data, new_value):
    student_id = data['student_id']
    field = data['field']

    if field == 'name':
        update_student_by_id(student_id, new_name=new_value)
    else:
        update_student_by_id(student_id, new_class=new_value)


def delete_student_from_base(student_id):
    delete_student_by_id(student_id)