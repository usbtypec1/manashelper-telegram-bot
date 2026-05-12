from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.filters.callback_data.food_menu import FoodMenuCallbackData
from app.ui.views.base import TextView


class FoodMenuView(TextView):
    text = (
        "<b>🤤 Просмотр меню в йемекхане:</b>\n\n"
        "🍏 На сегодня:\n"
        "<code>/yemek today</code>\n\n"
        "🍏 На завтра:\n"
        "<code>/yemek tomorrow</code>\n\n"
        "<b>🧐 Так же можно просматривать на N дней вперёд:</b>\n"
        "<code>/yemek {N}</code>\n\n"
        "Например👇\n"
        "🍎 На послезавтра - <code>/yemek 2</code>\n"
        "🍎 10 дней вперёд - <code>/yemek 10</code>"
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🕕 Сегодня",
                    callback_data=FoodMenuCallbackData(days_to_skip=0).pack(),
                ),
                InlineKeyboardButton(
                    text="🕒 Завтра",
                    callback_data=FoodMenuCallbackData(days_to_skip=1).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🕒 Послезавтра",
                    callback_data=FoodMenuCallbackData(days_to_skip=2).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="main_menu",
                ),
            ],
        ],
    )
