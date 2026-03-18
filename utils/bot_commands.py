from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot):
    commands = [BotCommand(command='main_menu', description='Главное меню')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())