from aiogram.fsm.state import State, StatesGroup


class AddStudent(StatesGroup):
    name = State()
    student_class = State()


class ChangeStudent(StatesGroup):
    сhoosing_field = State()
    waiting_new_value = State()