import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

import key_board.test_keyboard as kb

TOKEN = '8373059069:AAFQdymiliVXviKBFxB-hmMHLK4QsJaWJI0'
dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}'
                         f'Кнопки!!!', reply_markup=kb.inlineKb2.as_markup())


@dp.callback_query()
async def check_callback(callback_data: CallbackQuery):
    if callback_data.data == 'Btn_7':
        await callback_data.message.answer('Вы нажали кнопку')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())