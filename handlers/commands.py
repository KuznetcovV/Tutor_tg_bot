from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from handlers.lessons import print_all_lessons
from handlers.students import print_all_students

from services.lessons_service import get_today_lessons_text

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')


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
    text = get_today_lessons_text()
    await message.answer(text)


@router.message(Command('payments'))
async def cmd_payments(message: Message):
    await message.answer('Список оплат за этот месяц')


@router.message(Command('transfers'))
async def cmd_transfers(message: Message):
    await message.answer('Все переносы')