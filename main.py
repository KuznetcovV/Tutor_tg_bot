import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from database.db import init_db
from handlers.students import router as students_router
from handlers.lessons import router as lessons_router
from handlers.commands import router as commands_router
from utils.bot_commands import set_commands


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():

    init_db()
    dp.include_routers(students_router,
                       lessons_router,
                       commands_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())