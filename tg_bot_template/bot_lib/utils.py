from aiogram import types
from loguru import logger

from .db_dispatcher import DbDispatcher
from .bot_feature import Feature


async def bot_safe_send_message(dp: DbDispatcher, social_id: int, text: str, **kwargs):
    try:
        text_arr = Feature.tg_msg_text_split(text)
        for mes in text_arr:
            await dp.bot.send_message(social_id, mes, **kwargs)
    except Exception:
        logger.warning(f"User with {social_id = } did not receive the message.")


async def bot_safe_send_photo(dp: DbDispatcher, social_id: int, photo, **kwargs):
    try:
        await dp.bot.send_photo(social_id, photo, **kwargs)
    except Exception as e:
        logger.warning(f"User with {social_id = } did not receive the photo.\nError: {e}")


async def bot_edit_callback_message(dp: DbDispatcher, callback: types.CallbackQuery, text: str, **kwargs):
    try:
        await dp.bot.edit_message_text(text, callback.from_user.id, callback.message.message_id, **kwargs)
    except Exception as e:
        logger.warning(f"Cant edit callback message for {callback = }.\nError: {e}")
