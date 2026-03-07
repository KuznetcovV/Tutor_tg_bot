from aiogram.utils.keyboard import InlineKeyboardBuilder


def student_menu_kb(student_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить',
                    callback_data=f'edit_student_{student_id}')
    keyboard.button(text='Удалить',
                    callback_data=f'delete_student_{student_id}')
    keyboard.button(text='Назад',
                    callback_data='back_to_list')

    keyboard.adjust(1)

    return keyboard.as_markup()


def edit_student_kb(name, student_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f'Изменить имя для {name}',
                    callback_data=f'change_name_{student_id}')
    keyboard.button(text=f'Изменить класс для {name}',
                    callback_data=f'change_class_{student_id}')
    keyboard.button(text='Назад к списку действий',
                    callback_data=f'student_{student_id}')

    keyboard.adjust(2)

    return keyboard.as_markup()


def all_students_kb(students):
    keyboard = InlineKeyboardBuilder()
    for student in students:
        student_id, name, student_class = student

        keyboard.button(text=f'{name} - {student_class} класс',
                        callback_data=f'student_{student_id}')
    keyboard.button(text='Добавить ученика', callback_data='add_student')

    keyboard.adjust(1)
    return keyboard.as_markup()
