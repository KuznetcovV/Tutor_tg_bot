from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from keyboards.menu_kb import main_menu_kb
from services.lessons_service import get_lessons_to_weekday_text
from handlers.lessons import print_all_weekdays, print_all_lessons
from handlers.students import all_payments_on_this_month, print_all_students

router = Router()


async def main_menu(message: Message, edit=False):
    kb = main_menu_kb()
    if edit:
        await message.edit_text(text='Главное меню', reply_markup=kb)
    else:
        await message.answer(text='Главное меню', reply_markup=kb)


@router.callback_query(F.data == 'lessons_today')
async def lessons_today(callback: CallbackQuery):
    text = get_lessons_to_weekday_text()
    await callback.message.edit_text(text)


@router.callback_query(F.data == 'weekday_schedule')
async def weekday_schedule(callback: CallbackQuery):
    await print_all_weekdays(callback.message)


@router.callback_query(F.data == 'today')
async def today(callback: CallbackQuery):
    await callback.message.edit_text('Вот твои дела на сегодня')


@router.callback_query(F.data == 'payments_this_month')
async def payments_this_month(callback: CallbackQuery):
    await all_payments_on_this_month(callback.message)


@router.callback_query(F.data == 'all_lessons')
async def all_lessons(callback: CallbackQuery):
    await print_all_lessons(callback.message)


@router.callback_query(F.data == 'all_students')
async def all_students(callback: CallbackQuery):
    await print_all_students(callback.message)


@router.callback_query(F.data == 'transfers')
async def all_transfers(callback: CallbackQuery):
    await callback.message.edit_text('Вот переносы в этом месяце')


@router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(callback: CallbackQuery):
    await main_menu(callback.message, edit=True)
