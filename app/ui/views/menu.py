from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.filters.callback_data.food_menu import FoodMenuCallbackData
from app.ui.views.base import TextView


class MainMenuView(TextView):
    text = "Главное меню"
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍉 Йемек",
                    callback_data="food_menu",
                ),
                InlineKeyboardButton(
                    text="🔐 OBIS",
                    callback_data="obis_menu",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🗓️ Расписание",
                    callback_data="timetable_menu",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ О боте",
                    callback_data="about",
                ),
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


class ObisMenuView(TextView):
    text = "Меню OBIS"
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✋ Йоклама",
                    callback_data="attendance",
                ),
                InlineKeyboardButton(
                    text="💯 Экзамены",
                    callback_data="exams",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔑 Ввести данные от OBIS",
                    callback_data="obis_credentials",
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


class UserHasNoCredentialsView(TextView):
    text = "Пожалуйста, введите ваши данные от OBIS."
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔑 Ввести данные от OBIS",
                    callback_data="obis_credentials",
                ),
            ],
        ],
    )


class AcceptTermsView(TextView):
    text = "Пожалуйста, примите условия использования бота, чтобы продолжить."
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Условия использования",
                    url="https://graph.org/Polzovatelskoe-soglashenie-manas-helper-bot-01-13",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Принять условия",
                    callback_data="accept_terms",
                ),
            ],
        ],
    )
