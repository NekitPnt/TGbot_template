from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
from peewee_async import Manager


class DbDispatcher(Dispatcher):  # type: ignore[misc]
    def __init__(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self._db_conn: Manager | None = None

    def set_db_conn(self, conn: Manager) -> None:
        self._db_conn = conn

    def get_db_conn(self) -> Manager:
        return self._db_conn


class AbsFilter(BoundFilter):  # type: ignore[misc]
    key = "key"

    def __init__(self, **kwargs):  # type: ignore[no-untyped-def]
        setattr(self, self.key, kwargs[self.key])

    async def check(self, msg: types.Message) -> bool:
        return True
