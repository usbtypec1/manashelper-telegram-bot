from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from ui.views.base import TextView


class MainMenuView(TextView):
    text = "Главное меню"
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Йемек"),
                KeyboardButton(text="OBIS"),
            ],
            [
                KeyboardButton(text="Расписание")
            ],
        ],
    )


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
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🕕 Сегодня"),
                KeyboardButton(text="🕒 Завтра"),
            ],
            [
                KeyboardButton(text="Назад"),
            ],
        ],
    )


class ObisMenuView(TextView):
    text = "Меню OBIS"
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Йоклама"),
                KeyboardButton(text="Экзамены"),
            ],
            [
                KeyboardButton(text="Назад"),
            ]
        ],
    )
