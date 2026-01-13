from aiogram.fsm.state import StatesGroup, State


class ObisCredentialsStates(StatesGroup):
    accept_terms = State()
    student_number = State()
    password = State()
