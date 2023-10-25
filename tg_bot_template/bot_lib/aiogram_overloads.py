from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
from peewee_async import Manager


class DbDispatcher(Dispatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db_conn: Manager | None = None

    def set_db_conn(self, conn: Manager) -> None:
        self._db_conn = conn

    def get_db_conn(self) -> Manager:
        return self._db_conn


class AbsFilter(BoundFilter):
    key = "key"

    def __init__(self, **kwargs):
        setattr(self, self.key, kwargs[self.key])

    async def check(self, msg: types.Message):
        return True
