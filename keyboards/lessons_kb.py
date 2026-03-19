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
    keyboard = students_list_kb(keyboard,
                                students,
                                'add_lesson_to')
    keyboard = cancel_back_template_kb(keyboard,
                                       cancel=True,
                                       cancel_callback='back_to_lessons_list')
    keyboard.adjust(1)
    return keyboard.as_markup()


def choose_time_interval_kb(free_intervals):
    keyboard = InlineKeyboardBuilder()
    keyboard = free_intervals_kb(keyboard,
                                 free_intervals,
                                 'add_timestart')
    keyboard = cancel_back_template_kb(keyboard,
                                       cancel=True,
                                       back=True,
                                       cancel_callback='back_to_lessons_list',
                                       back_callback='fsm_back_lessons')
    keyboard.adjust(2)
    return keyboard.as_markup()


def lesson_menu_kb(lesson_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить', callback_data=f'edit_lesson_{lesson_id}')
    keyboard.button(text='Удалить', callback_data=f'delete_lesson_{lesson_id}')
    keyboard = cancel_back_template_kb(keyboard,
                                       cancel=True,
                                       cancel_callback='back_to_lessons_list')
    keyboard.adjust(2)
    return keyboard.as_markup()


def edit_lesson_student_kb(students):
    keyboard = InlineKeyboardBuilder()
    keyboard = students_list_kb(keyboard, students, 'end_edit_lesson_student')
    for student_index, student in enumerate(students, 1):
        student_id, name, student_class = student
        keyboard.button(
            text=f"{student_index}. {name} - {student_class} класс",
            callback_data=f"end_edit_lesson_student_{student_id}"
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def edit_timeinterval_kb(free_intervals):
    keyboard = InlineKeyboardBuilder()
    keyboard = free_intervals_kb(keyboard,
                                 free_intervals,
                                 'end_edit_lesson_time')
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
    keyboard = cancel_back_template_kb(keyboard,
                                       back=True,
                                       back_callback='fsm_back_lessons')
    keyboard.adjust(1)
    return keyboard.as_markup()


def choose_weekday_for_student_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard = weekdays_list_kb(keyboard, 'add_weekday')
    keyboard = cancel_back_template_kb(keyboard,
                                       cancel=True,
                                       back=True,
                                       cancel_callback='back_to_lessons_list',
                                       back_callback='fsm_back_lessons')
    keyboard.adjust(1)
    return keyboard.as_markup()


def edit_weekday_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard = weekdays_list_kb(keyboard, 'end_edit_lesson_weekday')
    keyboard = cancel_back_template_kb(keyboard,
                                       back=True,
                                       back_callback='add_lesson_back')
    keyboard.adjust(1)
    return keyboard.as_markup()


def all_weekdays_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard = weekdays_list_kb(keyboard, 'print_lessons_for_weekday')
    keyboard.adjust(1)
    return keyboard.as_markup()


def weekdays_list_kb(keyboard, callback_prefix):
    for i in range(7):
        keyboard.button(text=f'{FULL_WEEKDAYS[i]}',
                        callback_data=f'{callback_prefix}_{i}')
    return keyboard


def cancel_back_template_kb(keyboard,
                            cancel=False,
                            back=False,
                            cancel_callback=None,
                            back_callback=None):
    if cancel:
        keyboard.button(text='Отмена',
                        callback_data=cancel_callback)
    if back:
        keyboard.button(text='Назад',
                        callback_data=back_callback)
    return keyboard


def free_intervals_kb(keyboard, free_intervals, callback_prefix):
    for interval in free_intervals:
        start, end = interval
        keyboard.button(text=f'{start:02}:00-{end:02}:00',
                        callback_data=f'{callback_prefix}_{start}_{end}')
    return keyboard


def students_list_kb(keyboard, students, prefix_callback):
    for student_index, student in enumerate(students, 1):
        student_id, name, student_class = student
        keyboard.button(
            text=f"{student_index}. {name} - {student_class} класс",
            callback_data=f"{prefix_callback}_{student_id}"
        )
    return keyboard


def back_to_weekdays_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard = cancel_back_template_kb(keyboard,
                                       back=True,
                                       back_callback='back_to_weekdays')
    return keyboard.as_markup()
