from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tg_bot_template.bot_lib.db_dispatcher import DbDispatcher
from tg_bot_template.config import settings

bot = Bot(token=settings.tg_bot_token)
if settings.environment.local_test:
    storage = MemoryStorage()
else:
    storage = RedisStorage2(settings.fsm_redis_host, db=settings.fsm_redis_db, password=settings.fsm_redis_pass)
dp = DbDispatcher(bot, storage=storage)
