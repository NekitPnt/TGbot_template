from pydantic import BaseModel
from aiogram import types


class Ftr(BaseModel):
    text: str = ''
    text2: str = ''
    slashed_command: str = ''
    slashed_command_descr: str = ''
    commands: list[str] = []
    buttons: list[list[str]] = []

    def find_triggers(self, message: types.Message):
        return message.text and any([i in message.text.lower() for i in self.triggers])

    @property
    def triggers(self):
        _triggers = []
        if self.slashed_command:
            _triggers.append(self.slashed_command)
        if self.commands:
            _triggers.extend(self.commands)
            for com in self.commands:
                _triggers.append(com.capitalize())
        return _triggers

    @property
    def kb(self):
        if not self.buttons:
            return types.ReplyKeyboardRemove()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for row in self.buttons:
            keyboard.row(*[str(btn) for btn in row])
        return keyboard


ping_ftr = Ftr(
    commands=["ping", "health", "healthcheck"],
    text="200 pong",
    text2="Bot is alive",
)
empty = Ftr()
start_ftr = Ftr(
    slashed_command="/start",
    slashed_command_descr="start bot",
    text="Hello there",
)
help_ftr = Ftr(
    slashed_command="/help",
    slashed_command_descr="bot help",
    text="Here will be help anytime",
)
register_ftr = Ftr(
    commands=["bot"],
    text=f"Welcome to bot"
)
register_failed = "Для регистрации заполните, пожалуйста, Имя пользователя в своем профиле, иначе вас не смогут найти" \
                  " другие участники!"
please_register = "Enter passphrase for register in bot:"
text_error = "What? Dont understand."
