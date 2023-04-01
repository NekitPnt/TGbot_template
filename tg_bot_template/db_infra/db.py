from datetime import datetime
from typing import Optional

from aiocache import cached
from aiocache.serializers import PickleSerializer
from loguru import logger

from tg_bot_template.bot_infra.states import UserFormData
from tg_bot_template.db_infra.models import conn, Users


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


async def create_user(*, user_social_id: int, username: str) -> None:
    await conn.create(Users, social_id=user_social_id, username=username, registration_date=datetime.now())
    logger.info(f"New user[{username}] registered")


async def update_user_info(*, social_id: int, user_form_data: UserFormData) -> None:
    user = await get_user(user_social_id=social_id)
    user.name = user_form_data.name
    user.info = user_form_data.info
    user.photo = user_form_data.photo
    await conn.update(user)


async def incr_user_taps(*, social_id: int) -> None:
    user = await get_user(user_social_id=social_id)
    user.taps += 1
    await conn.update(user)


async def get_all_users() -> list[Users]:
    return list(await conn.execute(Users.select().order_by(Users.taps.desc())))
