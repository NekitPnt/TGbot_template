from typing import Union, Optional

from aiogram import types
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class Emojis:
    dangerous: str = "⚠️"
    on_off: tuple = ("🔴️", "🟢")
    on: str = "🟢"
    off: str = "🔴️"
    none: str = "🚫"
    reload: str = "🔄"
    dog: str = "@"
    done: str = "✅"
    deny: str = "⛔️"
    pair: str = "👥"
    notes: str = "📝"
    gift: str = "🎁"
    t_me_link: str = "https://t.me/"


class Button(BaseModel):
    text: str


class InlineButton(BaseModel):
    text: str
    callback_data: Optional[str]


class Feature(BaseModel):
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
    one_time_keyboard: bool = False
    inline_keyboard: list[list[InlineButton]] = []
    callback_action: str = ""
    data_key: str = ""

    def find_triggers(self, message: types.Message):
        return message.text and any([i in message.text.lower() for i in self.triggers])

    @property
    def triggers(self) -> list[str]:
        _triggers = []
        if self.slashed_command:
            _triggers.append(self.slashed_command)
        if self.button:
            _triggers.append(self.button.lower())
        if self.commands:
            _triggers.extend(self.commands)
            for com in self.commands:
                _triggers.append(com.capitalize())
        return _triggers

    @property
    def kb(self) -> Union[types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove]:
        return self.create_tg_kb(self.keyboard, self.one_time_keyboard)

    @property
    def inline_kb(self) -> Union[types.InlineKeyboardMarkup]:
        return self.create_tg_inline_kb(self.inline_keyboard)

    @staticmethod
    def create_tg_kb(
            input_kb: list[list[Button]],
            one_time_keyboard: bool = False
    ) -> Union[types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove]:
        if not input_kb:
            return types.ReplyKeyboardRemove()
        res_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)
        for row in input_kb:
            res_kb.row(*[str(btn.text) for btn in row])
        return res_kb

    @staticmethod
    def create_tg_inline_kb(input_kb: list[list[InlineButton]]) -> Union[types.InlineKeyboardMarkup]:
        res_kb = types.InlineKeyboardMarkup()
        for row in input_kb:
            res_kb.row(*[types.InlineKeyboardButton(btn.text, callback_data=btn.callback_data) for btn in row])
        return res_kb

    def menu_line(self) -> str:
        return f"{self.emoji}{self.slashed_command} — {self.about}"


def text_cutter(text: str, text_size: int) -> list[str]:
    return [text[x:x + text_size] for x in range(0, len(text), text_size)]


def text_split(text: str) -> list[str]:
    return [mes for mes in text_cutter(text, 4096)]


def get_username(text: str) -> str:
    return text.replace(Emojis().dog, "").replace(Emojis().t_me_link, "")
