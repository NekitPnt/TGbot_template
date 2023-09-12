from typing import Optional
from pydantic_settings import BaseSettings

SCHEDULE_HEALTHCHECK = "7:00"  # !!!UTC timezone!!!


class BotSettings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_dsn: str

    fsm_redis_host: Optional[str] = None
    fsm_redis_db: Optional[int] = None
    fsm_redis_pass: Optional[str] = None

    tg_bot_token: str
    # pay_token: str
    register_passphrase: Optional[str] = None
    creator_id: Optional[int] = None

    inline_kb_button_row_width: int = 2
    schedule_healthcheck: str = "7:00"  # !!!UTC timezone!!!

    class Config:
        env_file = ".env"
        require_by_default = False


settings = BotSettings()

KEYBOARD_ = {
    'FAST_FORWARD_BUTTON': '⏩',
    'FAST_REVERSE_BUTTON': '⏪',
    'INFORMATION': 'ℹ️',
    'RIGHT_ARROW_CURVING_LEFT': '↩️',
    'CROSS_MARK': '❌',
    'CHECK_MARK_BUTTON': '✅',
    'STOPWATCH': '⏱️',
    'RECYCLING_SYMBOL': '♻️',
    'SOS_BUTTON': '🆘',
    'UPWARDS_BUTTON': '🔼',
    'DOLLAR': '💵',
    'DIAMOND_WITH_A_DOT': '💠',
    'LINKED_PAPERCLIPS': '🖇️',
    'WARNING': '⚠️'
}
