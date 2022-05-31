import os
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot_template.db import check_user_registered

CREATOR_ID = os.getenv("CREATOR_ID", None)


class AbsFilter(BoundFilter):
    key = 'key'

    def __init__(self, **kwargs):
        setattr(self, self.key, kwargs[self.key])

    async def check(self, msg: types.Message):
        return True


class CreatorFilter(AbsFilter):
    key = 'is_creator'

    async def check(self, msg: types.Message):
        return CREATOR_ID is None or str(msg.from_user.id) == CREATOR_ID


class RegistrationFilter(AbsFilter):
    key = 'is_registered'

    async def check(self, msg: types.Message):
        return await check_user_registered(msg.from_user.id)


class NonRegistrationFilter(AbsFilter):
    key = 'is_not_registered'

    async def check(self, msg: types.Message):
        return not await check_user_registered(msg.from_user.id)
