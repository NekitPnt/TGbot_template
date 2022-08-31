from aiogram import types
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class Emojis:
    dangerous: str = "⚠️"
    on_off: tuple = ("🔴️", "🟢")
    none: str = "🚫"
    dog: str = "@"
    done: str = "✅"
    notes: str = "📝"
    t_me_link: str = "https://t.me/"


class Button(BaseModel):
    text: str


class Ftr(BaseModel):
    text: str = ""
    text2: str = ""
    about: str = ""
    help: str = ""
    emoji: str = ""
    slashed_command: str = ""
    slashed_command_descr: str = ""
    button: str = ""
    commands: list[str] = []
    keyboard: list[list[Button]] = []

    def find_triggers(self, message: types.Message):
        return message.text and any([i in message.text.lower() for i in self.triggers])

    @property
    def triggers(self):
        _triggers = []
        if self.slashed_command:
            _triggers.append(self.slashed_command)
        if self.button:
            _triggers.append(self.button)
        if self.commands:
            _triggers.extend(self.commands)
            for com in self.commands:
                _triggers.append(com.capitalize())
        return _triggers

    @property
    def kb(self):
        if not self.keyboard:
            return types.ReplyKeyboardRemove()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for row in self.keyboard:
            keyboard.row(*[str(btn.text) for btn in row])
        return keyboard

    def menu_line(self):
        return f"{self.emoji}{self.slashed_command} — {self.about}"


def text_cutter(text: str, text_size: int) -> list[str]:
    return [text[x:x + text_size] for x in range(0, len(text), text_size)]


def text_split(text: str) -> list[str]:
    return [mes for mes in text_cutter(text, 4096)]


def get_username(text: str) -> str:
    return text.replace(Emojis().dog, "").replace(Emojis().t_me_link, "")
