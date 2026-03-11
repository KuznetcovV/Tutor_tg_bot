from datetime import datetime
from utils.constants import FULL_WEEKDAYS
from database.queries.selects import (select_lessons_for_weekday,
                                      select_all_students,
                                      select_all_lessons,
                                      select_occupied_intervals,
                                      select_student_by_id,
                                      select_lesson_by_id,
                                      select_occupied_intervals_by_lesson_id)
from database.queries.updates import update_lesson_data
from database.queries.inserts import add_lesson
from database.queries.deletes import delete_lesson_by_id


def get_lessons_to_weekday_text(weekday=datetime.now().weekday()):
    weekday_text = FULL_WEEKDAYS[weekday]
    lessons_today_list = select_lessons_for_weekday(weekday)
    if not lessons_today_list:
        text = f'{weekday_text}.\nЗанятий нет'
        return text
    text = f'{FULL_WEEKDAYS[weekday]}.\nСписок занятий:\n'
    for index, lesson in enumerate(lessons_today_list, 1):
        name, student_class, _, time_start, time_end = lesson
        text += (f'\n{index}. {name} {student_class} класс\n'
                 f'{time_start}:00 - {time_end}:00')
    return text


def get_all_lessons():
    lessons = select_all_lessons()
    return lessons


def get_students_for_lesson():
    return select_all_students()


def get_free_intervals_for_weekday(weekday):
    occupied_intervals = select_occupied_intervals(weekday)
    free_intervals = [(i, i + 1) for i in range(12, 22) if (i, i + 1) not in occupied_intervals]

    return free_intervals


def create_lesson_from_state(data):

    student_id = data['student_id']
    weekday = data['weekday']
    time_start = data['time_start']
    time_end = data['time_end']
    name_student, student_class = select_student_by_id(student_id)

    add_lesson(student_id, weekday, time_start, time_end)

    text = (
        f'Ученику {name_student}, который учится в {student_class} классе\n'
        f'добавлено занятие в {FULL_WEEKDAYS[weekday]}.\n'
        f'Время: {time_start:02}:00 - {time_end:02}:00'
    )

    return text


def get_lesson_info_text(lesson_id):
    lesson = select_lesson_by_id(lesson_id)

    name_student, weekday, time_start, time_end = lesson

    text = (f'{name_student}\n'
            f'{FULL_WEEKDAYS[weekday]}\n'
            f'{time_start}:00 - {time_end}:00\nВыберите действие:')

    return text


def delete_lesson_service(lesson_id):
    delete_lesson_by_id(lesson_id)
    return 'Запись о занятии удалена'


def get_free_intervals_for_edit(lesson_id):

    occupied_intervals = select_occupied_intervals_by_lesson_id(lesson_id)

    free_intervals = [(i, i + 1) for i in range(12, 22) if (str(i), str(i + 1)) not in occupied_intervals]

    return free_intervals


def update_lesson(lesson_id, field, new_value):
    update_lesson_data(lesson_id, field, new_value)

    return 'Изменения сохранены.'
    
