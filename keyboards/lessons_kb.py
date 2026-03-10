from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.constants import FULL_WEEKDAYS, SHORT_WEEKDAYS


def print_all_lessons_kb(lessons):
    keyboard = InlineKeyboardBuilder()
    if not lessons:
        keyboard.button(text='Добавить урок', callback_data='add_lesson')
        keyboard.adjust(1)
    else:
        for lesson in lessons:
            lesson_id, name, student_class, weekday, time_start, time_end = lesson
            keyboard.button(
                text=f'{name} - {student_class}\n\n{SHORT_WEEKDAYS[weekday]}\n\n{time_start:02}:00 - {time_end:02}:00', callback_data=f'lesson_{lesson_id}'
            )
        keyboard.button(text='Добавить занятие', callback_data='add_lesson')
        keyboard.adjust(1)

    return keyboard.as_markup()


def start_add_lesson_kb(students):
    keyboard = InlineKeyboardBuilder()
    for index, student in enumerate(students, 1):
        id_student, name, student_class = student
        keyboard.button(
            text=f'{index} - {name} - {student_class} класс.',
            callback_data=f'add_lesson_to_{id_student}')
    keyboard.button(text='Отмена', callback_data='back_to_lessons_list')
    keyboard.adjust(1)
    return keyboard.as_markup()


def choose_weekday_for_student_kb():
    keyboard = InlineKeyboardBuilder()
    for i in range(7):
        keyboard.button(text=f'{FULL_WEEKDAYS[i]}',
                        callback_data=f'add_weekday_{i}')
    keyboard.button(text='Назад', callback_data='fsm_back_lessons')
    keyboard.button(text='Отмена', callback_data='back_to_lessons_list')

    keyboard.adjust(1)
    return keyboard.as_markup()


def choose_time_interval_kb(free_intervals):
    keyboard = InlineKeyboardBuilder()
    for interval in free_intervals:
        start, end = interval
        keyboard.button(text=f'{start:02}:00-{end:02}:00',
                        callback_data=f'add_timestart_{start}_{end}')
    keyboard.button(text='Назад', callback_data='fsm_back_lessons')
    keyboard.button(text='Отмена', callback_data='back_to_lessons_list')

    keyboard.adjust(2)
    return keyboard.as_markup()


def lesson_menu_kb(lesson_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить', callback_data=f'edit_lesson_{lesson_id}')
    keyboard.button(text='Удалить', callback_data=f'delete_lesson_{lesson_id}')
    keyboard.button(text='Отмена', callback_data='back_to_lessons_list')

    keyboard.adjust(2)
    return keyboard.as_markup()


def edit_lesson_student_kb(students):
    keyboard = InlineKeyboardBuilder()
    for student_index, student in enumerate(students, 1):
        student_id, name, student_class = student
        keyboard.button(
            text=f"{student_index}. {name} - {student_class} класс",
            callback_data=f"end_edit_lesson_student_{student_id}"
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def edit_weekday_kb():
    keyboard = InlineKeyboardBuilder()
    for i, day in enumerate(FULL_WEEKDAYS):
        keyboard.button(text=day, callback_data=f'end_edit_lesson_weekday_{i}')
    keyboard.button(text='Назад', callback_data='add_lesson_back')

    keyboard.adjust(1)
    return keyboard.as_markup()


def edit_timeinterval_kb(free_intervals):
    keyboard = InlineKeyboardBuilder()
    for interval in free_intervals:
        start, end = interval
        keyboard.button(text=f'{start}:00-{end}:00',
                        callback_data=f'end_edit_lesson_time_{start}_{end}')
    keyboard.adjust(2)
    return keyboard.as_markup()


def edit_lesson_kb(lesson_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить день',
                    callback_data=f'edit_weekday_{lesson_id}')
    keyboard.button(text='Изменить время',
                    callback_data=f'edit_timeinterval_{lesson_id}')
    keyboard.button(text='Изменить ученика',
                    callback_data=f'edit_lesson_student_{lesson_id}')
    keyboard.button(text='Назад', callback_data='fsm_back_lessons')

    keyboard.adjust(1)
    return keyboard.as_markup()


def all_weekdays_kb():
    keyboard = InlineKeyboardBuilder()
    for i in range(len(FULL_WEEKDAYS)):
        keyboard.button(text=f'{FULL_WEEKDAYS[i]}',
                        callback_data=f'print_lessons_for_weekday_{i}')
    keyboard.adjust(1)
    return keyboard.as_markup()


def cancel_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Отмена', callback_data='back_to_lessons_list')
    return keyboard.as_markup()


def back_cancel_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Отмена', callback_data='back_to_lessons_list')
    keyboard.button(text='Назад', callback_data='fsm_back_lessons')
    return keyboard.as_markup()