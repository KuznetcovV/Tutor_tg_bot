from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from fsm_states.student_states import AddStudent, ChangeStudent
from keyboards.students_kb import (student_menu_kb,
                                   edit_student_kb,
                                   all_students_kb,
                                   cancel_kb,
                                   student_class_list_kb)
from services.students_service import (add_student_to_base,
                                       get_student_name_by_id,
                                       get_full_student_by_id,
                                       save_new_value_to_base,
                                       delete_student_from_base,
                                       get_all_students,
                                       calculate_all_prices_for_students)

router = Router()


@router.callback_query(F.data == 'fsm_back_students')
async def fsm_back(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    history = data.get('history', [])

    if not history:
        await callback.answer()
        return

    prev_state = history.pop()

    await state.update_data(history=history)

    screen = STATE_SCREENS.get(prev_state)

    if screen:
        await screen(callback.message, state)

    await callback.answer()


@router.callback_query(F.data == 'add_student')
async def start_add(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await show_name_screen(callback.message, state)

    await callback.answer()


@router.message(AddStudent.name)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    current_state = await state.get_state()
    await state.update_data(prev_state=current_state)

    await show_class_screen(message, state)


@router.callback_query(F.data.startswith('add_class_'), AddStudent.student_class)
async def capture_student_class(callback: CallbackQuery, state: FSMContext):
    await state.update_data(student_class=int(callback.data.split('_')[-1]))
    student = await state.get_data()
    msg_text = add_student_to_base(student)
    await callback.message.edit_text(msg_text)
    await print_all_students(callback.message)
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


@router.callback_query(F.data == 'back_to_students_list')
async def back_to_list_hendler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
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


async def show_name_screen(message: Message, state: FSMContext):
    kb = cancel_kb()

    await message.answer('Введите имя ученика:',
                         reply_markup=kb)

    await push_state(state, AddStudent.name)


async def show_class_screen(message: Message, state: FSMContext):
    kb = student_class_list_kb()

    await message.answer('Отлично! Теперь выберите класс ученика:',
                         reply_markup=kb)

    await push_state(state, AddStudent.student_class)


async def push_state(state: FSMContext, new_state):
    data = await state.get_data()
    history = data.get('history', [])
    current_state = await state.get_state()

    if current_state:
        history.append(current_state)

    await state.update_data(history=history)

    await state.set_state(new_state)


async def all_payments_on_this_month(message: Message):
    text = 'Оплаты за этот месяц:\n\n'
    for name, price in calculate_all_prices_for_students():
        text += f'Ученик {name}: {price} руб.\n'
    await message.answer(text)


STATE_SCREENS = {AddStudent.name.state: show_name_screen,
                 AddStudent.student_class.state: show_class_screen}
