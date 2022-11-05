import asyncio
import os
import aioschedule
from loguru import logger

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

from tg_bot_template.config import SCHEDULE_HEALTHCHECK
from tg_bot_template.bot_content import features
from tg_bot_template.db_infra import db
from tg_bot_template.bot_infra.filters import RegistrationFilter, NonRegistrationFilter, CreatorFilter

bot = Bot(token=os.getenv("TG_BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# filters binding
dp.filters_factory.bind(CreatorFilter)
dp.filters_factory.bind(RegistrationFilter)
dp.filters_factory.bind(NonRegistrationFilter)


# -------------------------------------------- HANDLERS --------------------------------------------
@dp.message_handler(lambda message: features.ping_ftr.find_triggers(message))
async def ping(msg: types.Message):
    await bot_safe_send_message(msg.from_user.id, features.ping_ftr.text)


@dp.message_handler(Text(equals=["creator"], ignore_case=True), creator=True)
async def creator_filter_check(msg: types.Message):
    await msg.answer("*Master?*", parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(Text(equals=features.start_ftr.triggers, ignore_case=True), registered=True)
async def start(msg: types.Message):
    await msg.answer(features.start_ftr.text, reply_markup=features.start_ftr.kb)


@dp.message_handler(Text(equals=features.help_ftr.triggers, ignore_case=True), registered=True)
async def help_feature(msg: types.Message):
    await msg.answer(features.help_ftr.text, reply_markup=features.empty.kb)


@dp.message_handler(Text(equals=features.cancel_ftr.triggers, ignore_case=True), state="*")
async def cancel_command(msg: types.Message, state: FSMContext):
    await msg.answer(features.cancel_ftr.text)
    await msg.answer(features.start_ftr.text, reply_markup=features.start_ftr.kb)

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()


@dp.callback_query_handler(Text(equals=features.cancel_ftr.triggers, ignore_case=True), state="*")
async def cancel_callback(callback: types.CallbackQuery, state: FSMContext):
    await bot_edit_callback_message(callback, features.cancel_ftr.text)
    await bot_safe_send_message(callback.from_user.id, features.start_ftr.text, reply_markup=features.start_ftr.kb)

    if await state.get_state() is not None:
        await state.finish()


@dp.message_handler(content_types=["any"], not_registered=True)
async def registration(msg: types.Message):
    if features.register_ftr.find_triggers(msg):
        if msg.from_user.username:
            await db.create_user(user_social_id=msg.from_user.id, username=msg.from_user.username)
            await msg.answer(features.register_ftr.text)
            await msg.answer(features.start_ftr.text, reply_markup=features.start_ftr.kb)
        else:
            await msg.answer(features.register_failed)
    else:
        await msg.answer(features.please_register, reply_markup=features.empty.kb)


@dp.message_handler(content_types=["any"], registered=True)
async def handle_wrong_text_msg(msg: types.Message):
    await msg.answer(features.text_error)


async def bot_safe_send_message(social_id: int, text: str, **kwargs):
    try:
        text_arr = features.Feature.tg_msg_text_split(text)
        for mes in text_arr:
            await bot.send_message(social_id, mes, **kwargs)
    except Exception:
        logger.warning(f"User with {social_id = } did not receive the message.")


async def bot_safe_send_photo(social_id: int, photo, **kwargs):
    try:
        await bot.send_photo(social_id, photo, **kwargs)
    except Exception as e:
        logger.warning(f"User with {social_id = } did not receive the photo.\nError: {e}")


async def bot_edit_callback_message(callback: types.CallbackQuery, text: str, **kwargs):
    try:
        await bot.edit_message_text(text, callback.from_user.id, callback.message.message_id, **kwargs)
    except Exception as e:
        logger.warning(f"Cant edit callback message for {callback = }.\nError: {e}")


# ---------------------------------------- SCHEDULED FEATURES ---------------------------------------
async def healthcheck():
    logger.info(features.ping_ftr.text2)
    if (creator_id := os.getenv("CREATOR_ID", None)) is not None:
        await bot_safe_send_message(int(creator_id), features.ping_ftr.text2)


# -------------------------------------------- BOT SETUP --------------------------------------------
async def bot_scheduler():
    logger.info("Scheduler is up")
    aioschedule.every().day.at(SCHEDULE_HEALTHCHECK).do(healthcheck)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    logger.info("Bot is up")

    # bot commands setup
    cmds = features.BOT_COMMAND_FEATURES_LIST
    bot_commands = [types.BotCommand(ftr.slashed_command, ftr.slashed_command_descr) for ftr in cmds]
    await dispatcher.bot.set_my_commands(bot_commands)

    # scheduler startup
    asyncio.create_task(bot_scheduler())


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
