from abc import ABC

from aiogram import Bot
from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    Message,
)
from aiogram.utils.media_group import MediaType, MediaGroupBuilder


type ReplyMarkup = (
    InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply
)


class MediaGroupView(ABC):
    medias: list[MediaType] | None = None
    caption: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_caption(self) -> str | None:
        return self.caption

    def get_medias(self) -> list[MediaType] | None:
        return self.medias

    def as_media_group(self) -> list[MediaType]:
        media_group_builder = MediaGroupBuilder(
            media=self.get_medias(),
            caption=self.get_caption(),
        )
        return media_group_builder.build()

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


class PhotoView(ABC):
    photo: str | None = None
    caption: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_photo(self) -> str | None:
        return self.photo

    def get_caption(self) -> str | None:
        return self.caption

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


class TextView(ABC):
    text: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


type View = TextView | PhotoView | MediaGroupView


async def answer_text_view(message: Message, view: TextView) -> Message:
    return await message.answer(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def answer_photo_view(message: Message, view: PhotoView) -> Message:
    return await message.answer_photo(
        photo=view.get_photo(),
        caption=view.get_caption(),
        reply_markup=view.get_reply_markup(),
    )


async def answer_media_group_view(
    message: Message,
    view: MediaGroupView,
) -> list[Message]:
    return await message.answer_media_group(
        media=view.as_media_group(),
    )


async def answer_view(message: Message, view: View) -> Message | list[Message]:
    match view:
        case TextView():
            return await answer_text_view(message=message, view=view)
        case PhotoView():
            return await answer_photo_view(message=message, view=view)
        case MediaGroupView():
            return await answer_media_group_view(message=message, view=view)


async def edit_message_by_view(
    message: Message,
    view: TextView,
) -> Message:
    return await message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def send_text_view(
    bot: Bot,
    chat_id: int,
    view: TextView,
) -> Message:
    return await bot.send_message(
        chat_id=chat_id,
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def send_photo_view(
    bot: Bot,
    chat_id: int,
    view: PhotoView,
) -> Message:
    return await bot.send_photo(
        chat_id=chat_id,
        photo=view.get_photo(),
        caption=view.get_caption(),
        reply_markup=view.get_reply_markup(),
    )


async def send_media_group_view(
    bot: Bot,
    chat_id: int,
    view: MediaGroupView,
) -> list[Message]:
    return await bot.send_media_group(
        chat_id=chat_id,
        media=view.as_media_group(),
    )


async def send_view(
    bot: Bot,
    chat_id: int,
    view: View,
) -> list[Message] | Message:
    match view:
        case TextView():
            return await send_text_view(bot=bot, chat_id=chat_id, view=view)
        case PhotoView():
            return await send_photo_view(bot=bot, chat_id=chat_id, view=view)
        case MediaGroupView():
            return await send_media_group_view(
                bot=bot,
                chat_id=chat_id,
                view=view,
            )
