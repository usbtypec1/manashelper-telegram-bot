from aiogram.fsm.state import StatesGroup, State


class DailyMenuRatingCommentStates(StatesGroup):
    comment = State()
