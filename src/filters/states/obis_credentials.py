from aiogram.fsm.state import StatesGroup, State


class ObisCredentialsStates(StatesGroup):
    student_number = State()
    password = State()
