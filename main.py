import asyncio
import os
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, BotCommand, BotCommandScopeDefault, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from database import init_db, get_all_students, add_new_student, get_student_by_id, edit_student_by_id, delete_student_by_id, select_all_lessons, add_lesson

init_db()
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN)
router = Router()

SHORT_WEEKDAYS = ["Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб",
            "Вс"]


class AddStudent(StatesGroup):
    name = State()
    student_class = State()


class ChangeStudent(StatesGroup):
    сhoosing_field = State()
    waiting_new_value = State()


class AddLesson(StatesGroup):
    student_id = State()
    weekday = State()
    time_start = State()


@router.callback_query(F.data == 'add_lesson')
async def start_add_lesson(callback: CallbackQuery, state: FSMContext):
    students = get_all_students()
    keyboard = InlineKeyboardBuilder()
    for index, student in enumerate(students, 1):
        id_student, name, student_class = student
        keyboard.button(text=f'{index} - {name} - {student_class} класс.', callback_data=f'add_lesson_to_{id_student}')

    keyboard.adjust(1)

    await callback.message.edit_text(text='Выберите ученика, которому нужно добавить занятие', reply_markup=keyboard.as_markup())
    await state.set_state(AddLesson.student_id)

@router.callback_query(F.data.startswith('add_lesson_to_'), AddLesson.student_id)
async def choose_weekday_for_student(callback: CallbackQuery, state: FSMContext):
    await state.update_data(student_id=int(callback.data.split('_')[-1]))
    keyboard = InlineKeyboardBuilder()
    for i in range(7):
        keyboard.button(text=f'{WEEKDAYS[i]}', callback_data=f'add_weekday_{i}')

    keyboard.adjust(1)
    await callback.message.edit_text(text='Выберите день недели', reply_markup=keyboard.as_markup())
    await state.set_state(AddLesson.weekday)

@router.callback_query(F.data.startswith('add_weekday_'), AddLesson.weekday)
async def chose_time_interval(callback: CallbackQuery, state: FSMContext):
    await state.update_data(weekday=int(callback.data.split('_')[-1]))
    keyboard = InlineKeyboardBuilder()
    for i in range(12, 22):
        keyboard.button(text=f'{i:02}:00-{i + 1:02}:00', callback_data=f'add_timestart_{i}_{i+1}')

    keyboard.adjust(2)
    await callback.message.edit_text(text='Выберите время:', reply_markup=keyboard.as_markup())
    await state.set_state(AddLesson.time_start)


@router.callback_query(F.data.startswith('add_timestart_'), AddLesson.time_start)
async def end_of_add_new_lesson(callback: CallbackQuery, state: FSMContext):
    start_time, end_time = callback.data.split('_')[-2:]
    await state.update_data(time_start=start_time, time_end=end_time)
    lesson = await state.get_data()
    student_id = lesson.get('student_id')
    name_student, student_class = get_student_by_id(lesson.get('student_id'))
    weekday = lesson.get('weekday')
    time_start = lesson.get('time_start')
    time_end = lesson.get('time_end')
    add_lesson(student_id, weekday, time_start, time_end)
    text = f'Ученику {name_student}, который учится в {student_class} добавлено занятие в {SHORT_WEEKDAYS[weekday]}.\n Время: {time_start:02}:00 - {end_time:02}:00'
    await callback.message.edit_text(text=text)
    await print_all_lessons(callback.message)
    await state.clear()


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
    add_new_student(student.get('name'), student.get('student_class'))
    msg_text = (f"Ученик {student.get('name')}, который учится в {student.get('student_class')} классе добавлен")
    await message.answer(msg_text)
    await print_all_students(message)
    await state.clear()


@router.callback_query(F.data.startswith('change_name_'))
async def edit_name(callback: CallbackQuery, state: FSMContext):
    student_id = int(callback.data.split('_')[2])
    name, _ = get_student_by_id(student_id)

    await state.update_data(student_id=student_id, field='name')

    await callback.message.edit_text(f'Введите новое имя ученика\nСтарое - {name}:')

    await state.set_state(ChangeStudent.waiting_new_value)


@router.callback_query(F.data.startswith('change_class_'))
async def edit_class(callback: CallbackQuery, state: FSMContext):
    student_id = int(callback.data.split('_')[2])
    name, student_class = get_student_by_id(student_id)

    await state.update_data(student_id=student_id, field='class')

    await callback.message.edit_text(f'Введите новый класс для {name}\nСтарое значение - {student_class}:')

    await state.set_state(ChangeStudent.waiting_new_value)


@router.message(ChangeStudent.waiting_new_value)
async def save_new_value(message: Message, state: FSMContext):

    data = await state.get_data()

    student_id = data['student_id']
    field = data['field']
    new_value = message.text

    if field == 'name':
        edit_student_by_id(student_id, new_name=new_value)
    else:
        edit_student_by_id(student_id, new_class=new_value)

    await message.answer("Данные обновлены")
    await print_all_students(message)
    await state.clear()


@router.callback_query(F.data.startswith('student_'))
async def student_menu(callback: CallbackQuery):
    student_id = int(callback.data.split('_')[1])
    student = get_student_by_id(student_id)

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить', callback_data=f'edit_{student_id}')
    keyboard.button(text='Удалить', callback_data=f'delete_{student_id}')
    keyboard.button(text='Назад', callback_data='back_to_list')

    keyboard.adjust(1)

    await callback.message.edit_text(
        f'{student[0]} - {student[1]} класс\n\nВыберите действие:',
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data == 'back_to_list')
async def back_to_list_hendler(callback: CallbackQuery):
    await print_all_students(callback.message, edit=True)


@router.callback_query(F.data.startswith('delete_'))
async def delete_student(callback: CallbackQuery):
    student_id = int(callback.data.split('_')[1])
    name, student_class = get_student_by_id(student_id)
    delete_student_by_id(student_id)
    await callback.message.edit_text(text=f'{name}, который учится в {student_class} классе был удален.')
    await print_all_students(callback.message)


@router.callback_query(F.data.startswith('edit_'))
async def edit_student(callback: CallbackQuery):
    student_id = int(callback.data.split('_')[1])
    name, student_class = get_student_by_id(student_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f'Изменить имя для {name}', callback_data=f'change_name_{student_id}')
    keyboard.button(text=f'Изменить класс для {name}', callback_data=f'change_class_{student_id}')
    keyboard.button(text='Назад к списку действий', callback_data=f'student_{student_id}')

    keyboard.adjust(2)

    await callback.message.edit_text(text=f'{name} - {student_class} класс. \nИзменить имя или класс?', reply_markup=keyboard.as_markup())


async def set_commands():
    commands = [BotCommand(command='today', description='Дела на сегодня'),
                BotCommand(command='students', description='Список всех учеников'),
                BotCommand(command='all_lessons', description='Список всех занятий'),
                BotCommand(command='lessons_today', description='Список учеников сегодня'),
                BotCommand(command='payments', description='Оплаты за этот месяц'),
                BotCommand(command='transfers', description='Все переносы'),]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


@router.message(Command('today'))
async def cmd_today(message: Message):
    await message.answer('Вот твои дела на сегодня')


@router.message(Command('students'))
async def cmd_students(message: Message):
    await print_all_students(message)


@router.message(Command('all_lessons'))
async def all_lessons(message: Message):
    await print_all_lessons(message)


@router.message(Command('lessons_today'))
async def lessons_today(message: Message):
    pass


@router.message(Command('lessons_today'))
async def cmd_students_today(message: Message):
    await message.answer('Вот ученики, которые сегодня будут')


@router.message(Command('payments'))
async def cmd_payments(message: Message):
    await message.answer('Список оплат за этот месяц')


@router.message(Command('transfers'))
async def cmd_transfers(message: Message):
    await message.answer('Все переносы')


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')


async def print_all_students(message: Message, edit=False):
    students = get_all_students()
    keyboard = InlineKeyboardBuilder()
    if not students:
        text = 'Список пуст!!!'
        keyboard.button(text='Добавить ученика', callback_data='add_student')
    else:
        text = 'Список учеников:\n\n'
        text += 'Выберите ученика:'
        for student_index, student in enumerate(students, 1):
            student_id, name, student_class = student
            keyboard.button(
                text=f"{student_index}. {name} - {student_class} класс",
                callback_data=f"student_{student_id}"
            )
        keyboard.button(text='Добавить ученика', callback_data='add_student')
        keyboard.adjust(1)

    if edit:
        await message.edit_text(text, reply_markup=keyboard.as_markup())
        message.answer()
    else:
        await message.answer(text, reply_markup=keyboard.as_markup())


async def print_all_lessons(message: Message, edit=False):
    lessons = select_all_lessons()
    keyboard = InlineKeyboardBuilder()
    if not lessons:
        text = 'Список уроков пуст!'
        keyboard.button(text='Добавить урок', callback_data='add_lesson')
    else:
        text = 'Список всех уроков: \n\n'
        text += 'Выберите запись для изменения или удаления:'
        for lesson in lessons:
            lesson_id, name, student_class, weekday, time_start, time_end = lesson
            keyboard.button(
                text=f'{name} - {student_class}\n\n{SHORT_WEEKDAYS[weekday]}\n\n{time_start:02}:00 - {time_end:02}:00', callback_data=f'lesson_{lesson_id}'
            )
        keyboard.button(text='Добавить занятие', callback_data='add_lesson')
        keyboard.adjust(1)

    if edit:
        await message.edit_text(text, reply_markup=keyboard.as_markup())
        message.answer()
    else:
        await message.answer(text, reply_markup=keyboard.as_markup())


async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    await dp.start_polling(bot)    

if __name__ == '__main__':
    asyncio.run(main())