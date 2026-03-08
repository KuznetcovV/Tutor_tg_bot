from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from fsm_states.lesson_states import AddLesson, EditLesson
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest
from keyboards.lessons_kb import (start_add_lesson_kb,
                                  choose_time_interval_kb,
                                  choose_weekday_for_student_kb,
                                  lesson_menu_kb,
                                  edit_lesson_student_kb,
                                  edit_weekday_kb,
                                  edit_timeinterval_kb,
                                  edit_lesson_kb,
                                  print_all_lessons_kb,
                                  all_weekdays_kb)
from services.lessons_service import (get_students_for_lesson,
                                      get_free_intervals_for_weekday,
                                      create_lesson_from_state,
                                      get_lesson_info_text,
                                      delete_lesson_service,
                                      get_free_intervals_for_edit,
                                      update_lesson,
                                      get_all_lessons,
                                      get_lessons_to_weekday_text)


router = Router()


@router.callback_query(F.data == 'add_lesson')
async def start_add_lesson(callback: CallbackQuery, state: FSMContext):
    students = get_students_for_lesson()
    kb = start_add_lesson_kb(students)
    await callback.message.edit_text(
        text='Выберите ученика, которому нужно добавить занятие',
        reply_markup=kb)
    await state.set_state(AddLesson.student_id)
    await state.update_data(history=[])


@router.callback_query(F.data.startswith('add_lesson_to_'),
                       AddLesson.student_id)
async def choose_weekday_for_student(callback: CallbackQuery,
                                     state: FSMContext):
    await state.update_data(student_id=int(callback.data.split('_')[-1]))
    kb = choose_weekday_for_student_kb()
    await callback.message.edit_text(text='Выберите день недели',
                                     reply_markup=kb)
    current_state = await state.get_state()
    data = await state.get_data()

    history = data.get('history', [])
    history.append(current_state)

    await state.update_data(history=history)
    await state.set_state(AddLesson.weekday)


@router.callback_query(F.data.startswith('add_weekday_'), AddLesson.weekday)
async def chose_time_interval(callback: CallbackQuery, state: FSMContext):
    weekday = int(callback.data.split('_')[-1])
    await state.update_data(weekday=weekday)
    free_intervals = get_free_intervals_for_weekday(weekday)
    if not free_intervals:
        await callback.answer('Свободного времени в этот день недели нет',
                              show_alert=True)
        return
    kb = choose_time_interval_kb(free_intervals)
    await callback.message.edit_text(text='Выберите время:', reply_markup=kb)
    current_state = await state.get_state()
    data = await state.get_data()

    history = data.get('history', [])
    history.append(current_state)

    await state.update_data(history=history)
    await state.set_state(AddLesson.time_start)


@router.callback_query(F.data.startswith('add_timestart_'),
                       AddLesson.time_start)
async def end_of_add_new_lesson(callback: CallbackQuery, state: FSMContext):
    start_time, end_time = callback.data.split('_')[-2:]
    await state.update_data(time_start=start_time, time_end=end_time)
    lesson_data = await state.get_data()

    text = create_lesson_from_state(lesson_data)

    await callback.message.edit_text(text=text)
    await print_all_lessons(callback.message)
    await state.clear()


@router.callback_query(F.data.startswith('lesson_'))
async def lesson_menu(callback: CallbackQuery):
    lesson_id = int(callback.data.split('_')[-1])
    text = get_lesson_info_text(lesson_id)
    kb = lesson_menu_kb(lesson_id)
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data.startswith('delete_lesson_'))
async def delete_lesson(callback: CallbackQuery):
    lesson_id = int(callback.data.split('_')[-1])
    text = delete_lesson_service(lesson_id)
    await callback.message.edit_text(text)
    await print_all_lessons(callback.message)


@router.callback_query(F.data == 'back_to_list_lessons')
async def back_to_lessons(callback: CallbackQuery):
    await print_all_lessons(callback.message, edit=True)


@router.callback_query(F.data.startswith('edit_lesson_student_'))
async def edit_lesson_student(callback: CallbackQuery, state: FSMContext):
    lesson_id = int(callback.data.split('_')[-1])
    await state.update_data(lesson_id=lesson_id, field="student_id")
    students = get_students_for_lesson()
    text = 'Список учеников:\n\n'
    text += 'Выберите ученика:'
    kb = edit_lesson_student_kb(students)
    try:
        await callback.message.edit_text(text='Выберите нового ученика:',
                                         reply_markup=kb)
    except TelegramBadRequest as e:
        if 'message is not modified' in str(e):
            pass
        else:
            raise
    await state.set_state(EditLesson.waiting_student)
    await callback.answer()


@router.callback_query(F.data.startswith('edit_weekday_'))
async def edit_weekday(callback: CallbackQuery, state: FSMContext):
    lesson_id = int(callback.data.split('_')[-1])
    await state.update_data(lesson_id=lesson_id, field="weekday")
    kb = edit_weekday_kb()
    try:
        await callback.message.edit_text(text='Выберите новый день:',
                                         reply_markup=kb)
    except TelegramBadRequest as e:
        if 'message is not modified' in str(e):
            pass
        else:
            raise
    await state.set_state(EditLesson.waiting_weekday)
    await callback.answer()


@router.callback_query(F.data.startswith('edit_timeinterval_'))
async def edit_timeinterval(callback: CallbackQuery, state: FSMContext):
    lesson_id = int(callback.data.split('_')[-1])
    await state.update_data(lesson_id=lesson_id, field='timeinterval')
    free_intervals = get_free_intervals_for_edit(lesson_id)
    if not free_intervals:
        await callback.answer('Свободного времени в этот день недели нет',
                              show_alert=True)
        return
    kb = edit_timeinterval_kb(free_intervals)
    try:
        await callback.message.edit_text(text='Выберите время: ',
                                         reply_markup=kb)
    except TelegramBadRequest as e:
        if 'message is not modified' in str(e):
            pass
        else:
            raise
    await state.set_state(EditLesson.waiting_time_interval)
    await callback.answer()


@router.callback_query(F.data.startswith('edit_lesson_'))
async def edit_lesson(callback: CallbackQuery, state: FSMContext):
    lesson_id = int(callback.data.split('_')[-1])
    kb = edit_lesson_kb(lesson_id)
    try:
        await callback.message.edit_text(text='Выберите изменение: ',
                                         reply_markup=kb)
    except TelegramBadRequest as e:
        if 'message is not modified' in str(e):
            pass
        else:
            raise


@router.callback_query(F.data.startswith('end_edit_lesson_'),
                       StateFilter(EditLesson.waiting_weekday,
                                   EditLesson.waiting_student,
                                   EditLesson.waiting_time_interval))
async def set_new_weekday(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lesson_id = data.get('lesson_id')
    field = data.get('field')

    if field == 'timeinterval':
        start, end = callback.data.split('_')[-2:]
        new_value = (start, end)
    else:
        new_value = int(callback.data.split('_')[-1])

    text = update_lesson(lesson_id, field, new_value)
    await callback.message.answer(text)
    await print_all_lessons(callback.message)
    await state.clear()


@router.callback_query(F.data.startswith('print_lessons_for_weekday_'))
async def print_lessons_for_weekday(callback: CallbackQuery):
    weekday = int(callback.data.split('_')[-1])
    text = get_lessons_to_weekday_text(weekday)
    await callback.message.edit_text(text)


async def print_all_lessons(message: Message, edit=False):
    lessons = get_all_lessons()
    if not lessons:
        text = 'Список уроков пуст!'
    else:
        text = 'Список всех уроков: \n\n'
        text += 'Выберите запись для изменения или удаления:'

    kb = print_all_lessons_kb(lessons)

    if edit:
        await message.edit_text(text, reply_markup=kb)
    else:
        await message.answer(text, reply_markup=kb)


async def print_all_weekdays(message: Message):
    text = 'Выберите день недели:'
    kb = all_weekdays_kb()
    await message.answer(text, reply_markup=kb)