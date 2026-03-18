from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from handlers.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')


@router.message(Command('main_menu'))
async def cmd_main_menu(message: Message):
    await main_menu(message)