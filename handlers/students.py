from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from fsm_states.student_states import AddStudent, ChangeStudent
from keyboards.students_kb import (student_menu_kb,
                                   edit_student_kb,
                                   all_students_kb)
from services.students_service import (add_student_to_base,
                                       get_student_name_by_id,
                                       get_full_student_by_id,
                                       save_new_value_to_base,
                                       delete_student_from_base,
                                       get_all_students)

router = Router()


@router.callback_query(F.data == 'add_student')
async def start_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите имя ученика:')
    await state.set_state(AddStudent.name)


@router.message(F.text, AddStudent.name)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Отлично! Теперь напишите класс ученика: ')
    await state.set_state(AddStudent.student_class)


@router.message(F.text, AddStudent.student_class)
async def capture_student_class(message: Message, state: FSMContext):
    await state.update_data(student_class=message.text)
    student = await state.get_data()
    msg_text = add_student_to_base(student)
    await message.answer(msg_text)
    await print_all_students(message)
    await state.clear()


@router.callback_query(F.data.startswith('change_name_'))
async def edit_name(callback: CallbackQuery, state: FSMContext):
    student_id = int(callback.data.split('_')[2])
    name = get_student_name_by_id(student_id)

    await state.update_data(student_id=student_id, field='name')

    await callback.message.edit_text(
        f'Введите новое имя ученика\nСтарое - {name}:'
        )

    await state.set_state(ChangeStudent.waiting_new_value)


@router.callback_query(F.data.startswith('change_class_'))
async def edit_class(callback: CallbackQuery, state: FSMContext):
    student_id = int(callback.data.split('_')[2])
    name, student_class = get_full_student_by_id(student_id)

    await state.update_data(student_id=student_id, field='class')

    await callback.message.edit_text(
        f'Введите новый класс для {name}\nСтарое значение - {student_class}:'
        )

    await state.set_state(ChangeStudent.waiting_new_value)


@router.message(ChangeStudent.waiting_new_value)
async def save_new_value(message: Message, state: FSMContext):

    data = await state.get_data()
    new_value = message.text
    save_new_value_to_base(data, new_value)

    await message.answer("Данные обновлены")
    await print_all_students(message)
    await state.clear()


@router.callback_query(F.data.startswith('student_'))
async def student_menu(callback: CallbackQuery):
    student_id = int(callback.data.split('_')[1])
    student = get_full_student_by_id(student_id)

    kb = student_menu_kb(student_id)

    await callback.message.edit_text(
        f'{student[0]} - {student[1]} класс\n\nВыберите действие:',
        reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == 'back_to_list')
async def back_to_list_hendler(callback: CallbackQuery):
    await print_all_students(callback.message, edit=True)


@router.callback_query(F.data.startswith('delete_student_'))
async def delete_student(callback: CallbackQuery):
    student_id = int(callback.data.split('_')[-1])
    name, student_class = get_full_student_by_id(student_id)
    delete_student_from_base(student_id)
    await callback.message.edit_text(
        text=f'{name}, который учится в {student_class} классе был удален.'
        )
    await print_all_students(callback.message)


@router.callback_query(F.data.startswith('edit_student_'))
async def edit_student(callback: CallbackQuery):
    student_id = int(callback.data.split('_')[-1])
    name, student_class = get_full_student_by_id(student_id)
    kb = edit_student_kb(name, student_id)
    await callback.message.edit_text(text=f'{name} - {student_class} класс.'
                                          f'\nИзменить имя или класс?',
                                          reply_markup=kb)


async def print_all_students(message: Message, edit=False):

    students = get_all_students()
    kb = all_students_kb(students)
    text = 'Список учеников:\n\n'

    if edit:
        await message.edit_text(text, reply_markup=kb)
    else:
        await message.answer(text, reply_markup=kb)
