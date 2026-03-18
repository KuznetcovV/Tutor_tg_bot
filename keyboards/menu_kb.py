from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Занятия сегодня', callback_data='lessons_today')
    keyboard.button(text='Расписание на неделю', callback_data='weekday_schedule')
    keyboard.button(text='Дела на сегодня', callback_data='today')
    keyboard.button(text='Оплаты на месяц', callback_data='payments_this_month')
    keyboard.button(text='Список всех занятий', callback_data='all_lessons')
    keyboard.button(text='Список всех учеников', callback_data='all_students')
    keyboard.button(text='Переносы в этом месяце', callback_data='transfers')
    keyboard.adjust(1)
    return keyboard.as_markup()


def back_tom_main_menu_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Назад к меню', callback_data='back_to_main_menu')
    keyboard.adjust(1)
    return keyboard.as_markup()