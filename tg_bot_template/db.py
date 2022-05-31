from datetime import datetime
from typing import Optional
from aiocache import cached
from aiocache.serializers import PickleSerializer

from tg_bot_template.models import conn, Users, db_logger


@cached(ttl=0.2, serializer=PickleSerializer())
async def check_user_registered(user_social_id: int):
    user = await get_user(user_social_id)
    db_logger.info(f"Checked user db id = {user}, registration is {bool(user)}")
    return bool(user)


async def get_user(user_social_id: int) -> Optional[Users]:
    try:
        user = await conn.get(Users, social_id=user_social_id)
        return user
    except Exception:
        return None


async def create_user(*, user_social_id: int, username: str):
    await conn.create(Users, social_id=user_social_id, username=username, registration_date=datetime.now())
    db_logger.info(f"New user[{username}] registered")
