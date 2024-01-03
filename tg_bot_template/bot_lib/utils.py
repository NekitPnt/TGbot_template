from aiogram import types
from loguru import logger

from .aiogram_overloads import DbDispatcher
from .bot_feature import Feature


async def bot_safe_send_message(  # type: ignore[no-untyped-def]
    dp: DbDispatcher, social_id: int | None, text: str, **kwargs
) -> None:
    try:
        text_arr = Feature.tg_msg_text_split(text)
        for mes in text_arr:
            await dp.bot.send_message(social_id, mes, **kwargs)
    except Exception:
        logger.warning(f"User with {social_id = } did not receive the message.")


async def bot_safe_delete_message(dp: DbDispatcher, chat_id: int, message_id: int) -> None:
    try:
        await dp.bot.delete_message(chat_id, message_id)
    except Exception:
        logger.warning(f"Delete message {message_id} from chat {chat_id} failed.")


async def bot_safe_send_photo(  # type: ignore[no-untyped-def]
    dp: DbDispatcher, social_id: int, photo, **kwargs
) -> None:
    try:
        await dp.bot.send_photo(social_id, photo, **kwargs)
    except Exception as e:
        logger.warning(f"User with {social_id = } did not receive the photo.\nError: {e}")


async def bot_edit_callback_message(  # type: ignore[no-untyped-def]
    dp: DbDispatcher, callback: types.CallbackQuery, text: str | None, **kwargs
):
    try:
        await dp.bot.edit_message_text(text, callback.from_user.id, callback.message.message_id, **kwargs)
    except Exception as e:
        logger.warning(f"Cant edit callback message for {callback = }.\nError: {e}")
