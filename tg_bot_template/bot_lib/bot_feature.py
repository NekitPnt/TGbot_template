from __future__ import annotations

from dataclasses import dataclass

from aiogram import types
from pydantic import BaseModel


class ClassWithRepr:
    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={repr(v)}" for k, v in self.__dict__.items() if v is not None)
        return f"{type(self).__name__}({attrs})"


@dataclass
class TgUtils:
    dog: str = "@"
    t_me_link: str = "https://t.me/"


class TgUser(BaseModel):
    tg_id: int
    username: str | None


class Button(BaseModel):
    text: str


class InlineButton(BaseModel):
    text: str
    callback_data: str | None


@dataclass
class FeatureMenu:
    grid: list[list[Feature]]
    text: str | None = None


class Feature(ClassWithRepr):
    commands_to_set: list[Feature] = []

    def __init__(
        self,
        *,
        text: str | None = None,
        text2: str | None = None,
        about: str | None = None,
        error: str | None = None,
        help_text: str | None = None,
        emoji: str | None = None,
        slashed_command: str | None = None,
        slashed_command_descr: str | None = None,
        button: str | None = None,
        commands: list[str] | None = None,
        keyboard: list[list[Button]] | None = None,
        inline_keyboard: list[list[InlineButton]] | None = None,
        one_time_keyboard: bool = False,
        callback_action: str | None = None,
        data_key: str | None = None,
        menu: FeatureMenu | None = None,  # need attrs: self.button, self.slashed_command and self.about
        set_to_bot_commands: bool = False,  # need attrs: self.slashed_command and self.slashed_command_descr
    ):
        self.text = text
        self.text2 = text2
        self.about = about
        self.error = error
        self.help_text = help_text
        self.emoji = emoji if emoji is not None else ""
        self.slashed_command = slashed_command
        self.slashed_command_descr = slashed_command_descr
        self.button = button
        self.commands = commands
        self.keyboard = keyboard
        self.one_time_keyboard = one_time_keyboard
        self.inline_keyboard = inline_keyboard
        self.callback_action = callback_action
        self.data_key = data_key
        self.menu = menu

        if self.menu is not None:
            if self.keyboard is not None:
                raise AttributeError("Only one attribute may be set: keyboard or menu_grid")
            self.keyboard = [[Button(text=ftr.button) for ftr in row] for row in self.menu.grid]
            self.menu.text = "\n".join(f"{ftr.menu_line()}" for row in self.menu.grid for ftr in row)

        if set_to_bot_commands:
            if not (self.slashed_command and self.slashed_command_descr):
                raise AttributeError("slashed_command and slashed_command_descr fields must be set")
            self.commands_to_set.append(self)

    def find_triggers(self, message: types.Message) -> bool:
        return message.text and any(i in message.text.lower() for i in self.triggers)

    def menu_line(self) -> str:
        if self.slashed_command is None or self.about is None:
            raise AttributeError("Menu line need attrs: slashed_command and about")
        return f"{self.emoji}{self.slashed_command} — {self.about}"

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
    def kb(self) -> types.ReplyKeyboardMarkup | types.ReplyKeyboardRemove:
        return self.create_tg_kb(self.keyboard, self.one_time_keyboard)

    @property
    def inline_kb(self) -> types.InlineKeyboardMarkup:
        if self.inline_keyboard is None:
            raise AttributeError(
                'Argument 1 "self.inline_keyboard" to "create_tg_inline_kb" of "Feature" has incompatible type '
                '"list[list[InlineButton]] | None"; expected "list[list[InlineButton]]"'
            )
        return self.create_tg_inline_kb(self.inline_keyboard)

    @staticmethod
    def create_tg_kb(
        input_kb: list[list[Button]] | None, one_time_keyboard: bool = False
    ) -> types.ReplyKeyboardMarkup | types.ReplyKeyboardRemove:
        if not input_kb:
            return types.ReplyKeyboardRemove()
        res_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)
        for row in input_kb:
            res_kb.row(*[str(btn.text) for btn in row])
        return res_kb

    @staticmethod
    def create_tg_inline_kb(input_kb: list[list[InlineButton]]) -> types.InlineKeyboardMarkup:
        res_kb = types.InlineKeyboardMarkup()
        for row in input_kb:
            res_kb.row(*[types.InlineKeyboardButton(btn.text, callback_data=btn.callback_data) for btn in row])
        return res_kb

    @staticmethod
    def text_cutter(text: str, text_size: int) -> list[str]:
        return [text[x : x + text_size] for x in range(0, len(text), text_size)]

    @classmethod
    def tg_msg_text_split(cls, text: str) -> list[str]:
        return cls.text_cutter(text, 4096)

    @staticmethod
    def tg_get_username(text: str) -> str:
        return text.replace(TgUtils.dog, "").replace(TgUtils.t_me_link, "")
