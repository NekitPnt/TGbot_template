import asyncio
import os

import aioschedule
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from tg_bot_template import messages, db
from tg_bot_template.filters import RegistrationFilter, NonRegistrationFilter, CreatorFilter
from tg_bot_template.utils import create_logger

bot_logger = create_logger("bot_logs")
TOKEN = os.getenv("TG_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# filters binding
dp.filters_factory.bind(CreatorFilter)
dp.filters_factory.bind(RegistrationFilter)
dp.filters_factory.bind(NonRegistrationFilter)


# -------------------------------------------- HANDLERS --------------------------------------------
@dp.message_handler(lambda message: messages.ping_ftr.find_triggers(message))
async def ping(msg: types.Message):
    await msg.answer(messages.ping_ftr.text)


@dp.message_handler(Text(equals=["creator"], ignore_case=True), is_creator=True)
async def creator_filter_check(msg: types.Message):
    await msg.answer("Master?")


@dp.message_handler(Text(equals=messages.start_ftr.triggers, ignore_case=True), is_registered=True)
async def start(msg: types.Message):
    await msg.answer(messages.start_ftr.text, reply_markup=messages.start_ftr.kb)


@dp.message_handler(Text(equals=messages.help_ftr.triggers, ignore_case=True), is_registered=True)
async def help_feature(msg: types.Message):
    await msg.answer(messages.help_ftr.text, reply_markup=messages.empty.kb)


@dp.message_handler(content_types=['any'], is_not_registered=True)
async def registration(msg: types.Message):
    if messages.register_ftr.find_triggers(msg):
        if msg.from_user.username:
            await db.create_user(user_social_id=msg.from_user.id, username=msg.from_user.username)
            await msg.answer(messages.register_ftr.text)
            await msg.answer(messages.start_ftr.text, reply_markup=messages.start_ftr.kb)
        else:
            await msg.answer(messages.register_failed)
    else:
        await msg.answer(messages.please_register, reply_markup=messages.empty.kb)


@dp.message_handler(content_types=['any'], is_registered=True)
async def handle_wrong_text_msg(msg: types.Message):
    await msg.answer(messages.text_error)


# ---------------------------------------- SCHEDULED FEATURES ---------------------------------------
async def healthcheck():
    bot_logger.info(messages.ping_ftr.text2)
    if creator_id := os.getenv("CREATOR_ID", None) is not None:
        await bot.send_message(creator_id, messages.ping_ftr.text2)


# -------------------------------------------- BOT SETUP --------------------------------------------
async def bot_scheduler():
    bot_logger.info('Scheduler is up')
    aioschedule.every().day.at("10:00").do(healthcheck)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    bot_logger.info('Bot is up')

    # bot commands setup
    cmds = [messages.start_ftr, messages.help_ftr]
    bot_commands = [types.BotCommand(ftr.slashed_command, ftr.slashed_command_descr) for ftr in cmds]
    await dispatcher.bot.set_my_commands(bot_commands)

    # scheduler startup
    asyncio.create_task(bot_scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
