from aiogram.fsm.state import State, StatesGroup


class AddLesson(StatesGroup):
    student_id = State()
    weekday = State()
    time_start = State()


class EditLesson(StatesGroup):
    waiting_weekday = State()
    waiting_student = State()
    waiting_time_interval = State()