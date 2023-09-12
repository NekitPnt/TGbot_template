from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiopg.sa import Engine, SAConnection
from sqlalchemy import Table


class BaseRepository:

    engine: Engine
    table: Table

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    @asynccontextmanager
    async def _connection(self) -> AsyncGenerator[SAConnection, None]:
        async with self.engine.acquire() as connection:
            yield connection
