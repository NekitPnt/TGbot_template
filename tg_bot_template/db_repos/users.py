from tg_bot_template.db_repos.base import BaseRepository
from tg_bot_template.db_repos.tables import users_table

from aiocache import cached
from aiocache.serializers import PickleSerializer


class UsersRepository(BaseRepository):
    table = users_table

    @cached(ttl=0.2, serializer=PickleSerializer())
    async def check_user_registered(*, user_social_id: int) -> bool:
        user = await get_user(user_social_id=user_social_id)
        logger.info(f"Checked user db id = {user}, registration is {bool(user)}")
        return bool(user)

    async def get_user(*, user_social_id: int) -> Optional[Users]:
        try:
            user = await conn.get(Users, social_id=user_social_id)
            return user
        except Exception:
            return None
    async def add(self, delivery_tracking_item: DeliveryTrackingItem) -> None:
        insert_query = self.table.insert().values(**delivery_tracking_item.dict())

        async with self._connection() as connection:
            await connection.execute(insert_query)
