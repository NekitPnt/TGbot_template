from typing import Optional
from pydantic import BaseSettings
from enum import Enum


class Envs(Enum):
    local_test = "local_test"
    stage = "stage"
    prod = "prod"


class BotSettings(BaseSettings):
    tg_bot_token: str

    postgres_db: Optional[str]
    postgres_user: Optional[str]
    postgres_password: Optional[str]
    postgres_host: Optional[str]

    fsm_redis_host: Optional[str]
    fsm_redis_db: Optional[int]
    fsm_redis_pass: Optional[str]

    register_passphrase: Optional[str]
    creator_id: Optional[int]

    environment: Envs = Envs.local_test

    inline_kb_button_row_width: int = 2
    schedule_healthcheck: str = "7:00"  # !!!UTC timezone!!!

    class Config:
        env_file = ".env"


settings = BotSettings()
