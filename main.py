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
from database import init_db, get_all_students, add_new_student, delete_student, change_student, get_student_by_id

init_db()
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN)
router = Router()


class AddStudent(StatesGroup):
    name = State()
    student_class = State()


class DeleteStudent(StatesGroup):
    name = State()


class ChangeStudent(StatesGroup):
    old_name = State()
    new_name = State()
    student_class = State()


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

@router.callback_query(F.data == 'change_student')
async def start_change(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите имя ученика, информацию о котором хотите изменить: ')
    await state.set_state(ChangeStudent.old_name)

@router.message(F.text, ChangeStudent.old_name)
async def capture_old_name(message: Message, state: FSMContext):
    await state.update_data(old_name=message.text)
    await message.answer('Введите новое имя для ученика')
    await state.set_state(ChangeStudent.new_name)

@router.message(F.text, ChangeStudent.new_name)
async def capture_new_name(message: Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    await message.answer('Введите новый класс для ученика: ')
    await state.set_state(ChangeStudent.student_class)

@router.message(F.text, ChangeStudent.student_class)
async def capture_new_class(message: Message, state: FSMContext):
    await state.update_data(student_class=message.text)
    new_student = await state.get_data()
    change_student(new_student.get('old_name'), new_student.get('new_name'), new_student.get('student_class'))
    msg_text = (f"Запись об ученике {new_student.get('old_name')} изменена:"
                f"{new_student.get('new_name')} учится в {new_student.get('student_class')} классе")
    await message.answer(msg_text)
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


@router.callback_query(F.data == 'back_to_list')
async def back_to_list_hendler(callback: CallbackQuery):
    await print_all_students(callback.message, edit=True)


@router.callback_query(F.data == 'delete_student')
async def start_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите имя ученика')
    await state.set_state(DeleteStudent.name)


@router.message(F.text, DeleteStudent.name)
async def result_of_delete(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    student = await state.get_data()
    deleted_student = delete_student(student.get('name'))
    if not delete_student:
        await message.answer('Ученик не найден')
        await state.clear()
        return
    student_name, student_class = deleted_student
    msg_text = (f"Ученик {student_name}, который учится в {student_class} классе удален")
    await message.answer(msg_text)
    await print_all_students(message)
    await state.clear()


async def set_commands():
    commands = [BotCommand(command='today', description='Дела на сегодня'),
                BotCommand(command='students', description='Список всех учеников'),
                BotCommand(command='students_today', description='Список учеников сегодня'),
                BotCommand(command='payments', description='Оплаты за этот месяц'),
                BotCommand(command='transfers', description='Все переносы'),]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


@router.message(Command('today'))
async def cmd_today(message: Message):
    await message.answer('Вот твои дела на сегодня')


@router.message(Command('students'))
async def cmd_students(message: Message):
    await print_all_students(message)


@router.message(Command('students_today'))
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


async def print_all_students(message: Message,edit=False):
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
    else:
        await message.answer(text, reply_markup=keyboard.as_markup())


async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    await dp.start_polling(bot)    

if __name__ == '__main__':
    asyncio.run(main())