from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot_template.config import settings
from tg_bot_template.db_infra.db import check_user_registered


class AbsFilter(BoundFilter):
    key = "key"

    def __init__(self, **kwargs):
        setattr(self, self.key, kwargs[self.key])

    async def check(self, msg: types.Message):
        return True


class CreatorFilter(AbsFilter):
    key = "creator"

    async def check(self, msg: types.Message):
        return settings.creator_id is None or msg.from_user.id == settings.creator_id


class RegistrationFilter(AbsFilter):
    key = "registered"

    async def check(self, msg: types.Message):
        return await check_user_registered(user_social_id=msg.from_user.id)


class NonRegistrationFilter(AbsFilter):
    key = "not_registered"

    async def check(self, msg: types.Message):
        return not await check_user_registered(user_social_id=msg.from_user.id)
