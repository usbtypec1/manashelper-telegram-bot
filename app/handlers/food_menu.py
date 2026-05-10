from uuid import UUID

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.exceptions.food_menu import DailyMenuNotFoundException
from app.filters.callback_data.food_menu import (
    FoodMenuCallbackData,
    DailyMenuRatingCallbackData, DailyMenuCommentCallbackData,
    DailyMenuShowCommentsCallbackData,
)
from app.filters.states.food_menu import DailyMenuRatingCommentStates
from app.services.food_menu import FoodMenuService
from app.ui.views.base import (
    answer_media_group_view, answer_view,
    edit_message_by_view,
)
from app.ui.views.food_menu import (
    DailyMenuView, DailyMenuRateSuggestionView,
    DailyMenuRatedView, DailyMenuShowCommentsView, DailyMenuCommentListView,
)
from app.ui.views.menu import FoodMenuView


food_menu_router = Router(name=__name__)


@food_menu_router.callback_query(DailyMenuShowCommentsCallbackData.filter())
@inject
async def on_daily_menu_show_comments_callback_query(
    callback_query: CallbackQuery,
    callback_data: DailyMenuShowCommentsCallbackData,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    ratings = await food_menu_service.get_daily_menu_ratings_with_comments(
        daily_menu_id=callback_data.daily_menu_id,
    )
    view = DailyMenuCommentListView(ratings=ratings)
    await answer_view(callback_query.message, view)
    await callback_query.answer("")


@food_menu_router.message(F.text, StateFilter(DailyMenuRatingCommentStates.comment))
@inject
async def on_daily_menu_comment_message(
    message: Message,
    state: FSMContext,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    data = await state.get_data()
    score: int | None = data.get("score")
    daily_menu_id: str | None = data.get("daily_menu_id")
    if score is None or daily_menu_id is None:
        await message.reply("Произошла ошибка. Пожалуйста, попробуйте снова.")
        await state.clear()
        return
    daily_menu_id: UUID = UUID(daily_menu_id)

    await food_menu_service.update_daily_menu_rating(
        user_id=message.from_user.id,
        daily_menu_id=daily_menu_id,
        score=score,
        comment=message.text,
    )
    await message.answer("Спасибо за ваш отзыв! ❤️")
    await state.clear()


@food_menu_router.callback_query(DailyMenuCommentCallbackData.filter())
async def on_daily_menu_comment_callback_query(
    callback_query: CallbackQuery,
    callback_data: DailyMenuCommentCallbackData,
    state: FSMContext,
) -> None:
    await state.set_state(DailyMenuRatingCommentStates.comment)
    await state.update_data(score=callback_data.score)
    await state.update_data(daily_menu_id=str(callback_data.daily_menu_id))

    if callback_data.score <= 3:
        text = "Жаль, что вам не понравилось меню. Укажите пожалуйста, что именно вам не понравилось. 😊"
    else:
        text = "Рады, что вам понравилось меню! Укажите пожалуйста, что именно вам понравилось. 😄"
    await callback_query.message.answer(text=text)
    await callback_query.answer("")


@food_menu_router.callback_query(DailyMenuRatingCallbackData.filter())
@inject
async def on_daily_menu_rating_callback_query(
    callback_query: CallbackQuery,
    callback_data: DailyMenuRatingCallbackData,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    await food_menu_service.update_daily_menu_rating(
        user_id=callback_query.from_user.id,
        daily_menu_id=callback_data.daily_menu_id,
        score=callback_data.score,
    )
    await callback_query.answer(
        text="Спасибо за вашу оценку! ❤️",
        show_alert=True,
    )
    if callback_query.message.chat.type == ChatType.PRIVATE:
        view = DailyMenuRatedView(
            daily_menu_id=callback_data.daily_menu_id,
            score=callback_data.score,
        )
        await edit_message_by_view(callback_query.message, view)


@food_menu_router.callback_query(FoodMenuCallbackData.filter())
@inject
async def on_food_menu_callback_query(
    callback_query: CallbackQuery,
    callback_data: FoodMenuCallbackData,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    try:
        daily_menu = await food_menu_service.get_food_menu(
            days_to_skip=callback_data.days_to_skip,
        )
    except DailyMenuNotFoundException:
        await callback_query.answer(
            "Меню на этот день недоступно 😔",
            show_alert=True,
        )
        return

    view = DailyMenuView(daily_menu)
    await answer_media_group_view(message=callback_query.message, view=view)
    await callback_query.answer("")

    if daily_menu.has_comments:
        view = DailyMenuShowCommentsView(daily_menu_id=daily_menu.id)
        await answer_view(callback_query.message, view)

    is_private = callback_query.message.chat.type == ChatType.PRIVATE
    should_show: bool = True
    if is_private:
        should_show = not await food_menu_service.is_daily_menu_rated_by_user(
            user_id=callback_query.from_user.id,
            daily_menu_id=daily_menu.id,
        )

    if should_show:
        view = DailyMenuRateSuggestionView(daily_menu_id=daily_menu.id)
        await answer_view(callback_query.message, view)


@food_menu_router.message(Command("yemek"))
@inject
async def on_food_menu_command(
    message: Message,
    command: CommandObject,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    if not command.args:
        view = FoodMenuView()
        await answer_view(message, view)
        return

    word_to_days_count = {
        "today": 0,
        "tomorrow": 1,
    }

    if command.args in word_to_days_count:
        days_to_skip = word_to_days_count[command.args]
    elif command.args.isdigit():
        days_to_skip = int(command.args)
    else:
        await message.reply("Не могу распознать день 😔")
        return

    try:
        daily_menu = await food_menu_service.get_food_menu(
            days_to_skip=days_to_skip,
        )
    except DailyMenuNotFoundException:
        await message.answer(
            "Меню на этот день недоступно 😔",
            show_alert=True,
        )
        return

    view = DailyMenuView(daily_menu)
    await answer_media_group_view(message=message, view=view)

    if daily_menu.has_comments:
        view = DailyMenuShowCommentsView(daily_menu_id=daily_menu.id)
        await answer_view(message, view)

    is_private = message.chat.type == ChatType.PRIVATE
    should_show: bool = True
    if is_private:
        should_show = not await food_menu_service.is_daily_menu_rated_by_user(
            user_id=message.from_user.id,
            daily_menu_id=daily_menu.id,
        )

    if should_show:
        view = DailyMenuRateSuggestionView(daily_menu_id=daily_menu.id)
        await answer_view(message, view)
