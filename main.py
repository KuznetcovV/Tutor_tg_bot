import asyncio
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(token=TOKEN)
router = Router()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')


@dp.message(Command('today'))
async def cmd_today(message: Message):
    await message.answer('Вот твои дела на сегодня')


@dp.message(Command('students'))
async def cmd_students(message: Message):
    await message.answer('Список всех учеников, которые есть')


@dp.message(Command('students_today'))
async def cmd_students_today(message: Message):
    await message.answer('Вот ученики, которые сегодня будут')


@dp.message(Command('payments'))
async def cmd_payments(message: Message):
    await message.answer('Список оплат за этот месяц')


@dp.message(Command('transfers'))
async def cmd_transfers(message: Message):
    await message.answer('Все переносы')


async def set_commands():
    commands = [BotCommand(command='today', description='Дела на сегодня'),
                BotCommand(command='students', description='Список всех учеников'),
                BotCommand(command='students_today', description='Список учеников сегодня'),
                BotCommand(command='payments', description='Оплаты за этот месяц'),
                BotCommand(command='transfers', description='Все переносы'),]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    await dp.start_polling(bot)    

if __name__ == '__main__':
    asyncio.run(main())