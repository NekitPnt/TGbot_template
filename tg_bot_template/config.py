from typing import Optional
from pydantic import BaseSettings

SCHEDULE_HEALTHCHECK = "7:00"  # !!!UTC timezone!!!


class BotSettings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    fsm_redis_host: Optional[str]
    fsm_redis_db: Optional[int]
    fsm_redis_pass: Optional[str]

    tg_bot_token: str
    register_passphrase: Optional[str]
    creator_id: Optional[int]

    inline_kb_button_row_width: int = 2
    schedule_healthcheck: str = "7:00"  # !!!UTC timezone!!!

    class Config:
        env_file = ".env"


settings = BotSettings()
