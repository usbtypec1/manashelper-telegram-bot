import datetime
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.models.users import UsersStatistics
from app.ui.views.base import TextView


class AboutWhyCredentialsView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="about",
                ),
            ],
        ],
    )

    def __init__(self, users_statistics: UsersStatistics):
        self.__users_statistics = users_statistics

    def get_text(self) -> str:
        users_with_credentials_percentage = 0
        if self.__users_statistics.total_users_count > 0:
            users_with_credentials_percentage = (
                self.__users_statistics.users_with_credentials_count
                * 100
                // self.__users_statistics.total_users_count
            )
        return (
            "<b>Зачем боту нужен пароль от <code>OBIS</code>?</b>\n\n"

            "Чтобы бот мог:\n"
            "• 📊 получать ваши оценки\n"
            "• 🔔 уведомлять об их изменениях\n\n"
            "ему необходим доступ к вашей учетной записи в <code>OBIS</code>.\n\n"

            "<b>Безопасность данных</b>\n"
            "Ваши логин и пароль:\n"
            "• 🔐 хранятся <b>в зашифрованном виде</b>\n"
            "• ❌ не передаются третьим лицам\n"
            "• ✅ используются <u>только</u> для работы с <code>OBIS</code> "
            "от вашего имени\n\n"

            "<b>Немного статистики</b>\n"
            f"• 👥 {self.__users_statistics.users_with_credentials_count} из "
            f"{self.__users_statistics.total_users_count} пользователей "
            f"(<b>{users_with_credentials_percentage}%</b>) уже доверили боту свои данные."
        )


class AboutHowItWorksView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="about",
                ),
            ],
        ],
    )
    text = (
        "<b>Как работает бот (технически)</b>\n\n"

        "Бот состоит из <b>двух частей</b>:\n\n"

        "🤖 <b>Telegram-бот (frontend)</b>\n"
        "Написан на <b>Python</b> с использованием библиотеки <code>Aiogram</code>. "
        "Он отвечает за взаимодействие с пользователем: кнопки, сообщения, уведомления.\n\n"

        "⚙️ <b>Backend</b>\n"
        "Реализован на <b>Java</b> с использованием <code>Spring Boot</code>. "
        "Backend работает с данными, OBIS и бизнес-логикой.\n\n"

        "🔗 <b>Связь между частями</b>\n"
        "Telegram-бот общается с backend’ом через <b>REST API</b>.\n\n"

        "📂 <b>Открытый исходный код</b>\n"
        "• Telegram-бот: "
        "<a href='https://github.com/usbtypec1/manashelper-telegram-bot'>GitHub</a>\n"
        "• Backend: "
        "<a href='https://github.com/usbtypec1/manashelper'>GitHub</a>\n\n"

        "<i>Любой желающий может изучить код и убедиться, как именно работает бот.</i>"
    )


def get_course(now: datetime.datetime, enrollment_year: int) -> str:
    academic_year = now.year
    if now.month < 7:
        academic_year -= 1
    course_number = academic_year - enrollment_year + 1
    if course_number <= 4:
        return f"студент {course_number} курса"
    return "выпускник"


class AboutDeveloperView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="about",
                ),
            ],
        ],
    )

    def get_text(self) -> str:
        timezone = ZoneInfo("Asia/Bishkek")
        now = datetime.datetime.now(timezone)
        course = get_course(now, enrollment_year=2023)
        return (
            "<b>Кто сделал этого бота?</b>\n\n"

            "Меня зовут <b>Элдос Бактыбек уулу</b>, "
            f"я {course} Кыргызско-Турецкого Университета Манас, веб-разработчик и энтузиаст технологий.\n\n"

            "Я создал этого бота, чтобы помочь студентам "
            "легче справляться с учебными задачами и быть в курсе всех изменений.\n\n"

            "Если у тебя есть вопросы или предложения, или вы нашли ошибку в работе бота, можете связаться со мной:\n"
            "• 📨 Telegram: @usbtypec\n"
            "• 📧 Email: eldos.baktybekov@gmail.com"
        )


class AboutView(TextView):
    text = (
        "<b>Привет друг 👋</b>\n\n"
        "Этот бот создан специально для студентов "
        "<b>Кыргызско-Турецкого Университета Манас</b>.\n\n"
        "<b>Что умеет бот:</b>\n"
        "• 📊 <b>Йоклама и экзамены</b> — просмотр оценок и йокламы\n"
        "• 🔔 <b>Уведомления</b> об изменениях йокламы\n"
        "• 📝 <b>Оценки экзаменов</b> — узнавай сразу после выставления\n"
        "• 🍽 <b>Меню йемекханы</b> — актуальное меню на день\n"
        "• ⭐ <b>Оценка еды</b> — ставь и смотри рейтинги блюд\n"
        "• 📅 <b>Расписание занятий</b> и уведомления об изменениях"
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Зачем боту пароль от OBIS?",
                    callback_data="about:why_credentials",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Как работает бот? (Для задротов)",
                    callback_data="about:how_it_works",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Кто сделал этого бота?",
                    callback_data="about:developer",
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
